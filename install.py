"""Install selected Rapidan AI skills using only the Python standard library."""
import argparse
import os
import re
from pathlib import Path
import shutil


def matches(source, destination):
    """Verify a complete copy, refusing symlinks or extra files."""
    if destination.is_symlink() or not destination.is_dir():
        return False
    expected = {p.relative_to(source): p for p in source.rglob('*')}
    actual = {p.relative_to(destination): p for p in destination.rglob('*')}
    if expected.keys() != actual.keys():
        return False
    for name, original in expected.items():
        copied = actual[name]
        if copied.is_symlink() or original.is_dir() != copied.is_dir():
            return False
        if original.is_file() and original.read_bytes() != copied.read_bytes():
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=('codex', 'claude', 'hermes'))
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--skills', nargs='+', metavar='NAME', help='Install only these skill names')
    selection.add_argument('--all', action='store_true', help='Install all available skills')
    selection.add_argument('--list', action='store_true', help='List available skills without installing')
    parser.add_argument('--project', type=Path,
                        help='Existing project directory (Codex/Claude only); omit for a personal install')
    parser.add_argument('--hermes-home', type=Path,
                        help='Existing active Hermes profile home; overrides HERMES_HOME')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    available = {p.name: p for p in sorted(root.iterdir())
                 if p.is_dir() and not p.is_symlink()
                 and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p.name)
                 and (p / 'SKILL.md').is_file()}
    if args.list:
        print('\n'.join(available))
        return
    if not args.agent:
        parser.error('--agent is required when installing.')
    if not available:
        parser.error('No skill packages found in this checkout.')
    if args.skills:
        unknown = [name for name in args.skills if name not in available]
        if unknown:
            parser.error(f'Unknown skill(s): {", ".join(unknown)}. Available: {", ".join(available)}')
        names = list(dict.fromkeys(args.skills))
    elif args.all or len(available) == 1:
        names = list(available)
    else:
        parser.error('Choose --skills NAME [NAME ...] or --all; use --list to see available skills.')
    if args.agent == 'hermes':
        if args.project:
            parser.error('Hermes uses a profile home, not --project; use --hermes-home.')
        selected = args.hermes_home or os.environ.get('HERMES_HOME', '').strip()
        if not selected:
            parser.error('Resolve the active Hermes profile and pass --hermes-home, or set HERMES_HOME.')
        base = Path(selected).expanduser().resolve()
        relative = Path('skills/software-development')
    else:
        if args.hermes_home:
            parser.error('--hermes-home is only valid with --agent hermes.')
        base = args.project.expanduser().resolve() if args.project else Path.home()
        relative = Path('.agents' if args.agent == 'codex' else '.claude') / 'skills'
    if not base.is_dir():
        parser.error(f'Directory does not exist: {base}')
    packages = [(available[name], base / relative / name) for name in names]
    try:
        # Check every destination before writing any selected package.
        existing = set()
        for source, destination in packages:
            if destination.exists() or destination.is_symlink():
                if not matches(source, destination):
                    parser.error(f'Already installed with different content: {destination}. Preserve local edits; review before replacing.')
                existing.add(destination)
        for source, destination in packages:
            if destination in existing:
                print(f'Already installed and verified: {destination}')
                continue
            shutil.copytree(source, destination)
            if not matches(source, destination):
                parser.exit(1, f'Installation verification failed: {destination}\n')
            print(f'Installed and verified: {destination}')
    except OSError as error:
        parser.exit(1, f'Installation failed: {error}\n')
    print('Start a new agent session to load the skill.')


if __name__ == '__main__':
    main()
