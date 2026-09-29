"""Prepare a migration plan only; never invokes GitHub."""

from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
records = []
for repo in [root, *sorted(root.parent.glob("grok-gadgets-*"))]:
    src = repo / "planning/issues.json"
    if not src.is_file():
        continue
    items = json.loads(src.read_text())
    if isinstance(items, dict):
        items = items.get("issues", [])
    for issue in items:
        records.append(
            dict(
                repository=repo.name,
                local_id=issue["id"],
                github_number=None,
                stage=issue.get("stage"),
                source=str(src.relative_to(root.parent)),
                record=issue,
            )
        )
out = root / "publication/issue-migration.json"
out.write_text(
    json.dumps(dict(activated=False, owner=None, records=records), indent=2) + "\n"
)
print(f"Prepared {len(records)} local issue records; no GitHub changes")
