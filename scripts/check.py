from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
for name in ['LICENSE','README.md','AGENTS.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md','SECURITY.md']:
    assert (root/name).is_file(),name
issues=json.loads((root/'planning/issues.json').read_text())
assert len({i['id'] for i in issues})==len(issues)
for i in issues:
    assert i['stage'] in ['proposed','ready','in progress','review','blocked','done']
    assert all(k in i for k in ['repository','problem','acceptance','dependencies','labels','milestone','commits','evidence'])
    assert len(i['labels'])>=3
print(f'Hub foundation and {len(issues)} labeled issue records verified')
