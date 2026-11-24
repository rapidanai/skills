"""Validate voice-workshop eval definitions and the profile template round-trip.

Package integrity checks, not behavioral grading of an assistant.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL_DIR = ROOT.parent
SCRIPT = SKILL_DIR / "scripts" / "voice_profile.py"


def validate_cases() -> int:
    data = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    cases = data.get("cases")
    assert isinstance(cases, list) and cases, "cases.json must define a non-empty 'cases' list"
    seen: set[str] = set()
    for case in cases:
        for field in ("id", "prompt", "must", "must_not"):
            assert field in case, f"case missing '{field}': {case.get('id')}"
        assert case["id"] not in seen, f"duplicate case id: {case['id']}"
        seen.add(case["id"])
        for field in ("must", "must_not"):
            assert isinstance(case[field], list) and case[field], f"{case['id']}: '{field}' must be a non-empty list"
    return len(cases)


def validate_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "profile.md"
        init = subprocess.run(
            [sys.executable, str(SCRIPT), "init", "--path", str(path)],
            capture_output=True, text=True,
        )
        assert init.returncode == 0, init.stdout + init.stderr
        assert path.is_file(), "init did not create the profile"
        check = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", "--path", str(path)],
            capture_output=True, text=True,
        )
        assert check.returncode == 0, check.stdout + check.stderr


def main() -> int:
    count = validate_cases()
    validate_roundtrip()
    print(f"{count} scenario definitions and fixture oracles validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
