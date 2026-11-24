"""Create, validate, and display a voice-workshop profile. Standard library only.

Usage:
    python3 voice_profile.py init [--name NAME] [--path PATH] [--force]
    python3 voice_profile.py validate [--name NAME] [--path PATH]
    python3 voice_profile.py show [--name NAME] [--path PATH]

The profile lives at ~/.voice-workshop/profile.md by default. --path overrides
--name and points at an explicit file (used when the profile is kept with a project).
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path.home() / ".voice-workshop"
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "profile.md"
REQUIRED_SECTIONS = (
    "Voice in one line",
    "Rules",
    "Prefer",
    "Avoid",
    "Patterns",
    "Examples",
    "Open questions",
)


def resolve_path(name: str | None, explicit: str | None) -> Path:
    """Explicit --path wins; otherwise ~/.voice-workshop/<name|profile>.md."""
    if explicit:
        return Path(explicit).expanduser()
    return DEFAULT_DIR / f"{name or 'profile'}.md"


def read_template() -> str:
    """The bundled template with the date placeholder filled in."""
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    return text.replace("<YYYY-MM-DD>", datetime.date.today().isoformat())


def cmd_init(args: argparse.Namespace) -> int:
    path = resolve_path(args.name, args.path)
    if path.exists() and not args.force:
        print(f"Profile already exists: {path}")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(read_template(), encoding="utf-8")
    print(f"Created profile: {path}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = resolve_path(args.name, args.path)
    if not path.is_file():
        print(f"Missing profile: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    problems = []
    if not re.search(r"^#\s+Voice Profile\s*$", text, re.MULTILINE):
        problems.append("missing '# Voice Profile' title")
    if not re.search(r"^Updated:\s*\S", text, re.MULTILINE):
        problems.append("missing 'Updated:' line")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            problems.append(f"missing section: {section}")
    if problems:
        print(f"Invalid profile: {path}")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"Valid profile: {path}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    path = resolve_path(args.name, args.path)
    if not path.is_file():
        print(f"Missing profile: {path}")
        return 1
    sys.stdout.write(path.read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name, handler in (("init", cmd_init), ("validate", cmd_validate), ("show", cmd_show)):
        sub_parser = sub.add_parser(name)
        sub_parser.add_argument("--name", help="Profile name (default: profile)")
        sub_parser.add_argument("--path", help="Explicit profile path (overrides --name)")
        if name == "init":
            sub_parser.add_argument("--force", action="store_true", help="Overwrite an existing profile")
        sub_parser.set_defaults(func=handler)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
