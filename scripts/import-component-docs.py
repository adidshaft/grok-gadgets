"""Import tested component docs, retaining source commits/hashes; no network."""

from pathlib import Path
import subprocess
import json
import hashlib

R = Path(__file__).resolve().parents[1]
out = R / "docs/components"
out.mkdir(exist_ok=True)
manifest = R / "compatibility/documentation-sources.json"
previous = json.loads(manifest.read_text()) if manifest.exists() else []
records = []
for repo in sorted(R.parent.glob("grok-gadgets-*")):
    if not (repo / ".git").is_dir():
        continue
    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    for src in [repo / "README.md", *sorted((repo / "docs").glob("*.md"))]:
        text = src.read_text()
        dest = out / (repo.name + "-" + src.name)
        dest.write_text(
            "Source: "
            + repo.name
            + "/"
            + str(src.relative_to(repo))
            + " at "
            + commit
            + "\n\nThis is a pinned documentation snapshot. Relative filesystem paths describe the component checkout.\n\n"
            + text
        )
        records.append(
            dict(
                repository=repo.name,
                source=str(src.relative_to(repo)),
                commit=commit,
                sha256=hashlib.sha256(text.encode()).hexdigest(),
                snapshot=str(dest.relative_to(R)),
            )
        )
# Remove only prior generator-owned snapshots absent from the new source inventory.
current = {record["snapshot"] for record in records}
for record in previous:
    stale = (R / record["snapshot"]).resolve()
    if record["snapshot"] not in current and stale.parent == out.resolve():
        stale.unlink(missing_ok=True)
manifest.write_text(json.dumps(records, indent=2) + "\n")
print(f"Imported {len(records)} pinned component documentation sources")
