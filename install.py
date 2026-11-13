"""Install code-quality-analysis using only the Python standard library."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', required=True, choices=('codex', 'claude'))
    parser.add_argument('--project', type=Path,
                        help='Existing project directory; omit for a personal install')
    args = parser.parse_args()
    base = args.project.expanduser().resolve() if args.project else Path.home()
    if not base.is_dir():
        parser.error(f'Directory does not exist: {base}')
    folder = '.agents' if args.agent == 'codex' else '.claude'
    source = Path(__file__).resolve().parent / 'code-quality-analysis'
    destination = base / folder / 'skills' / source.name
    if destination.exists() or destination.is_symlink():
        parser.error(f'Already installed: {destination}. Back up and remove that directory before reinstalling.')
    try:
        shutil.copytree(source, destination)
    except OSError as error:
        parser.exit(1, f'Installation failed: {error}\n')
    print(f'Installed to {destination}')
    print('Start a new agent session to load the skill.')


if __name__ == '__main__':
    main()
