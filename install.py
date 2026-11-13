"""Install code-quality-analysis using only the Python standard library."""
import argparse
import os
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
    parser.add_argument('--agent', required=True, choices=('codex', 'claude', 'hermes'))
    parser.add_argument('--project', type=Path,
                        help='Existing project directory (Codex/Claude only); omit for a personal install')
    parser.add_argument('--hermes-home', type=Path,
                        help='Existing active Hermes profile home; overrides HERMES_HOME')
    args = parser.parse_args()
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
    source = Path(__file__).resolve().parent / 'code-quality-analysis'
    destination = base / relative / source.name
    try:
        if destination.exists() or destination.is_symlink():
            if matches(source, destination):
                print(f'Already installed and verified: {destination}')
                return
            parser.error(f'Already installed with different content: {destination}. Preserve local edits; review before replacing.')
        shutil.copytree(source, destination)
        if not matches(source, destination):
            parser.exit(1, f'Installation verification failed: {destination}\n')
    except OSError as error:
        parser.exit(1, f'Installation failed: {error}\n')
    print(f'Installed and verified: {destination}')
    print('Start a new agent session to load the skill.')


if __name__ == '__main__':
    main()
