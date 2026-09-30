"""Create unpublished source/artifact archives and checksums. No external actions."""

from pathlib import Path
import subprocess
import json
import hashlib
import shutil
import tarfile

R = Path(__file__).resolve().parents[1]
OUT = R / "artifacts/publication"
OUT.mkdir(parents=True, exist_ok=True)
records = []
for repo in [R, *sorted(R.parent.glob("grok-gadgets-*"))]:
    if not (repo / ".git").is_dir():
        continue
    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    archive = OUT / (repo.name + "-" + commit[:8] + ".tar.gz")
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "archive",
            "--format=tar.gz",
            "--prefix=" + repo.name + "/",
            "-o",
            str(archive),
            commit,
        ],
        check=True,
    )
    records.append(
        dict(
            repository=repo.name,
            source_commit=commit,
            commits=subprocess.check_output(
                ["git", "-C", str(repo), "log", "--format=%h %s"], text=True
            ).splitlines(),
            file=archive.name,
            sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        )
    )
    for src in sorted((repo / "dist").glob("*")):
        if src.suffix not in [".whl", ".gz"]:
            continue
        dest = OUT / src.name
        shutil.copy2(src, dest)
        records.append(
            dict(
                repository=repo.name,
                file=dest.name,
                sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                evidence="Built package; canonical component manifest has source provenance",
            )
        )
firmware = R.parent / "grok-gadgets-esp32-sdk/artifacts/c124-usb"
for src in sorted(firmware.glob("*")):
    if not src.is_file():
        continue
    dest = OUT / ("c124-" + src.name)
    shutil.copy2(src, dest)
    records.append(
        dict(
            repository="grok-gadgets-esp32-sdk",
            file=dest.name,
            sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
            status="Unpublished; physical/Grok pending; binary redistribution dependency review gate",
        )
    )
site = OUT / "website-static.tar.gz"
with tarfile.open(site, "w:gz") as archive:
    archive.add(R / "website/dist", arcname="website")
records.append(
    dict(
        repository=R.name,
        file=site.name,
        sha256=hashlib.sha256(site.read_bytes()).hexdigest(),
    )
)
(OUT / "manifest.json").write_text(
    json.dumps(
        dict(
            status="unpublished local candidate",
            version="0.1.0-alpha.1",
            artifacts=records,
        ),
        indent=2,
    )
    + "\n"
)
(OUT / "SHA256SUMS").write_text(
    "".join(x["sha256"] + "  " + x["file"] + "\n" for x in records)
)
print(f"Prepared {len(records)} local unpublished files at {OUT}")
