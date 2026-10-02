from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
skill = root / 'skill'
result = subprocess.run(
    [sys.executable, '/Users/zex/.codex/skills/.system/skill-creator/scripts/quick_validate.py', str(skill)],
    capture_output=True,
    text=True,
)
assert result.returncode == 0, result.stdout + result.stderr
evals = json.loads((skill / 'evals/evals.json').read_text())
assert evals['skill_name'] == 'disposable-artifact'
assert len(evals['evals']) == 3
text = (skill / 'SKILL.md').read_text()
for phrase in ['交付决策门', '唯一事实源', '不能把叙述改写成数值趋势', '外部发布边界']:
    assert phrase in text, phrase
assert not any('http://' in path.read_text() or 'https://' in path.read_text() for path in [skill / 'SKILL.md'])
print('project-skill-verification=PASS')
print('evals=', len(evals['evals']))
