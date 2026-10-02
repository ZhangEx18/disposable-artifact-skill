"""Portable structure check, not a model or browser evaluation."""
from pathlib import Path
import json
import re
import sys


def verify(root):
    errors = []
    source = (root / 'skill/SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', source, re.S)
    if not match:
        errors.append('SKILL.md needs frontmatter')
    else:
        fields = dict(re.findall(r'^([a-z-]+):[ \t]*(.*)$', match[1], re.M))
        if fields.get('name') != 'disposable-artifact':
            errors.append('unexpected skill name')
        if not fields.get('description') or len(fields['description']) > 1024:
            errors.append('description must be 1..1024 characters on one line')
    cases = json.loads((root / 'skill/evals/evals.json').read_text(encoding='utf-8'))
    if cases.get('skill_name') != 'disposable-artifact':
        errors.append('eval skill_name does not match')
    ids = set()
    for case in cases.get('evals', []):
        if case.get('id') in ids:
            errors.append('duplicate eval id')
        ids.add(case.get('id'))
        if not all(case.get(key) for key in ('id', 'prompt', 'expected_output', 'expectations')):
            errors.append('incomplete eval case')
        for filename in case.get('files', []):
            path = (root / 'skill' / filename).resolve()
            if not path.is_relative_to((root / 'skill').resolve()) or not path.is_file():
                errors.append('missing or out-of-scope eval fixture: ' + filename)
    if not ids:
        errors.append('no eval cases')
    for path in [root / 'README.md', *root.glob('skill/**/*.md')]:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if re.match(r'(https?://|#|mailto:)', target):
                continue
            resolved = (path.parent / target.split('#')[0]).resolve()
            if not resolved.is_file() or not resolved.is_relative_to(root.resolve()):
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        errors = verify(root)
    except (OSError, ValueError) as error:
        print('Structure check failed:', error, file=sys.stderr)
        return 1
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('Structure and fixture links: PASS (not a model/browser evaluation)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
