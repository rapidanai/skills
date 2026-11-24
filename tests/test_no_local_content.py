"""Guard: published skills carry no machine-local content and no committed profiles.

The repo is public and runtime-neutral. A skill may describe how to work; it may not
name this machine, a private sync client, an internal hostname, or a service that only
exists on the author's network. Local notes belong between LOCAL-ONLY markers in the
author's installed copy and are stripped before publishing, so the markers themselves
must never reach the repo.

Also refuses a committed voice profile: the profile is user state, not skill content.
The only permitted profile file is the blank template.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".txt"}

# Unambiguous machine-local markers. Generic words like "docker-compose.yml" are fine:
# they name a file a project might have, not a service this author runs.
LOCAL_PATTERNS = {
    "LOCAL-ONLY marker": re.compile(r"LOCAL-ONLY"),
    "absolute home path": re.compile(r"/home/[a-z]"),
    "private sync client": re.compile(r"Seafile|ccnet", re.I),
    "private network": re.compile(r"tailscale|ts\.net|\.ts\.net", re.I),
    "named client project": re.compile(r"heart[\s-]of[\s-]gold|HoG\b", re.I),
    "cloud CLI bound to one account": re.compile(r"\bgcloud\b", re.I),
    "internal domain": re.compile(r"rapidanai\.com", re.I),
}

SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{16,}"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{16,}"),
    "Slack token": re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

PROFILE_MARKER = re.compile(r"^## Voice in one line\s*$", re.M)
FENCED_BLOCK = re.compile(r"^```.*?^```[ \t]*$", re.M | re.S)
PLACEHOLDER = re.compile(r"^\s*<.*>\s*$")


def skill_dirs() -> list[Path]:
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def text_files() -> list[Path]:
    out: list[Path] = []
    for d in skill_dirs():
        for p in d.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
                out.append(p)
    return out


def looks_like_filled_profile(text: str) -> bool:
    """A real profile has the marker, a Sessions count, and a non-placeholder voice line."""
    prose = FENCED_BLOCK.sub("", text)  # a doc may show the structure inside a code fence
    match = PROFILE_MARKER.search(prose)
    if not match:
        return False
    if not re.search(r"^Sessions:\s*\d+\s*$", prose, re.M):
        return False
    tail = prose[match.end():].splitlines()[:4]
    return any(line.strip() and not PLACEHOLDER.match(line) for line in tail)


class NoLocalContentTests(unittest.TestCase):
    def test_skills_are_discovered(self):
        self.assertTrue(skill_dirs(), "no skills found; the guard would pass vacuously")

    def test_no_machine_local_references(self):
        findings = []
        for path in text_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(text.splitlines(), 1):
                for label, pattern in LOCAL_PATTERNS.items():
                    if pattern.search(line):
                        findings.append(f"{path.relative_to(ROOT)}:{lineno}: {label}: {line.strip()[:110]}")
        self.assertEqual(findings, [], "machine-local content in a published skill:\n" + "\n".join(findings))

    def test_no_secrets(self):
        findings = []
        for path in text_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    findings.append(f"{path.relative_to(ROOT)}: {label}")
        self.assertEqual(findings, [], "possible secret in a published skill:\n" + "\n".join(findings))

    def test_no_committed_profiles(self):
        findings = []
        for path in text_files():
            if path.parent.name == "templates":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if looks_like_filled_profile(text):
                findings.append(f"{path.relative_to(ROOT)}: contains a filled voice profile")
        self.assertEqual(findings, [], "user state committed to the repo:\n" + "\n".join(findings))


if __name__ == "__main__":
    unittest.main()