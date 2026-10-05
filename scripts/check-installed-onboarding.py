"""Fresh installed-wheel custom example acceptance; bounded local gateway, no source imports."""

from pathlib import Path
import os
import re
import subprocess
import tempfile
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
STDERR_LIMIT = 4000


def safe_stderr(value):
    if isinstance(value, bytes):
        value = value.decode(errors="replace")
    value = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", value or "")
    value = re.sub(r"https?://\S+", "[registry URL]", value)
    value = value.replace(str(Path.home()), "[home]")
    sensitive = re.compile(
        r"authorization\s*[:=]|(?:api[-_ ]?key|access[-_ ]?token|password|secret)\s*[:=]"
        r"|bearer\s+\S+|gh[pousr]_\S+|github_pat_\S+|xai-[A-Za-z0-9]{20,}",
        re.I,
    )
    value = "\n".join(
        "[redacted credential detail]" if sensitive.search(line) else line
        for line in value.splitlines()
    ).strip()
    if len(value) > STDERR_LIMIT:
        marker = "[stderr truncated]\n"
        value = marker + value[-(STDERR_LIMIT - len(marker)) :]
    return value or "No diagnostic stderr"


def run_checked(command, *, step, env, cwd=None, timeout=60):
    try:
        return subprocess.run(
            command,
            check=True,
            env=env,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"{step} failed (exit {exc.returncode}):\n{safe_stderr(exc.stderr)}"
        ) from None
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{step} timed out:\n{safe_stderr(exc.stderr)}") from None


def check_installed(root=ROOT):
    sdk = root.parent / "grok-gadgets-linux-sdk"
    gateway = root.parent / "grok-gadgets-gateway"
    with tempfile.TemporaryDirectory(prefix="grok-installed-") as directory:
        envdir = Path(directory) / "venv"
        command_env = dict(os.environ)
        command_env.pop("PYTHONPATH", None)
        command_env.pop("PYTHONHOME", None)
        run_checked(
            [
                "uv",
                "venv",
                str(envdir),
                "--offline",
                "--python",
                str(sdk / ".venv/bin/python"),
            ],
            step="Fresh installed environment",
            env=command_env,
        )
        python = envdir / "bin/python"
        wheels = []
        for repo in [sdk, gateway]:
            matches = list(repo.glob("dist/*.whl"))
            if len(matches) != 1:
                raise RuntimeError(f"Expected exactly one current wheel in {repo.name}")
            wheels.append(matches[0])
        # CI warms these same locked runtime pins before this offline acceptance.
        requirements = Path(directory) / "gateway-runtime.txt"
        run_checked(
            [
                "uv",
                "export",
                "--frozen",
                "--offline",
                "--no-dev",
                "--no-emit-project",
                "--no-header",
                "--no-annotate",
                "--project",
                str(gateway),
                "--output-file",
                str(requirements),
            ],
            step="Frozen gateway runtime export",
            env=command_env,
        )
        run_checked(
            [
                "uv",
                "pip",
                "install",
                "--offline",
                "--strict",
                "--python",
                str(python),
                "--requirements",
                str(requirements),
                *map(str, wheels),
            ],
            step="Offline installed-wheel runtime",
            env=command_env,
        )
        for variant in [[], ["--dataclass"]]:
            result = run_checked(
                [
                    str(python),
                    "-I",
                    str(sdk / "scripts/check_onboarding.py"),
                    str(sdk / "docs/development.md"),
                    *variant,
                ],
                step="Installed custom capability onboarding",
                env=command_env,
                cwd=directory,
                timeout=30,
            )
            print(result.stdout)
        print(
            json.dumps(
                {
                    "installed_wheels": [
                        dict(
                            file=p.name,
                            sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                        )
                        for p in wheels
                    ]
                }
            )
        )


if __name__ == "__main__":
    check_installed()
