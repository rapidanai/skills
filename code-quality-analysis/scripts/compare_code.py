"""Compare physical lines and changed lines for named files in two directories."""
import argparse
import difflib
import json
from pathlib import Path


def compare(before: Path, after: Path, names: list[str]) -> dict:
    results = []
    for name in names:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError(f'Expected a relative path within both snapshots: {name}')
        left_path, right_path = before / path, after / path
        left = left_path.read_text().splitlines() if left_path.is_file() else []
        right = right_path.read_text().splitlines() if right_path.is_file() else []
        if not left_path.is_file() and not right_path.is_file():
            raise ValueError(f'Missing from both snapshots: {name}')
        added = deleted = 0
        for line in difflib.ndiff(left, right):
            if line.startswith('+ '):
                added += 1
            elif line.startswith('- '):
                deleted += 1
        results.append({'file': name, 'before_lines': len(left), 'after_lines': len(right),
                        'net_lines': len(right) - len(left), 'added_lines': added,
                        'deleted_lines': deleted})
    return {'counting_rule': 'physical text lines, including blanks and comments',
            'files': results,
            'totals': {key: sum(row[key] for row in results) for key in
                       ('before_lines', 'after_lines', 'net_lines', 'added_lines', 'deleted_lines')}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before_dir', type=Path)
    parser.add_argument('after_dir', type=Path)
    parser.add_argument('files', nargs='+', help='relative paths; list the same scope for both snapshots')
    args = parser.parse_args()
    if not args.before_dir.is_dir() or not args.after_dir.is_dir():
        parser.error('both snapshot directories must exist')
    try:
        print(json.dumps(compare(args.before_dir, args.after_dir, args.files), indent=2))
    except (ValueError, UnicodeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
