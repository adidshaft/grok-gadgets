"""Reject commits whose author or committer email is a known private address.

  python3 scripts/check-commit-emails.py              check the identity Git will use now
  python3 scripts/check-commit-emails.py BASE..HEAD   check every commit in a range

Private addresses are stored only as SHA-256 hashes so this file never republishes them.
Use the GitHub noreply address or adidshaft@kyokasuigetsu.xyz instead.
"""

import hashlib
import subprocess
import sys

PRIVATE_SHA256 = {
    "9fb498561c8f0c80b0e01994957a1cca6230bbb6fa26e90607f336a30f63a3f4",
}
FIX = (
    "Set a public identity for this clone, for example:\n"
    "  git config user.email 224602646+adidshaft@users.noreply.github.com"
)


def private(email):
    return hashlib.sha256(email.strip().lower().encode()).hexdigest() in PRIVATE_SHA256


def git(*args):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def current_identity():
    found = []
    for variable in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
        ident = git("var", variable)
        email = ident[ident.find("<") + 1 : ident.find(">")]
        if private(email):
            found.append(variable.split("_")[1].lower())
    return found


def commits(revision_range):
    found = []
    for line in git("log", "--format=%h %ae %ce", revision_range).splitlines():
        sha, author, committer = line.split(" ")
        if private(author) or private(committer):
            found.append(sha)
    return found


def main(argv):
    if argv:
        bad = commits(argv[0])
        if bad:
            raise SystemExit(
                "Private email in commits "
                + ", ".join(bad)
                + ". Rewrite them before pushing.\n"
                + FIX
            )
        print("Commit identities are public")
        return
    bad = current_identity()
    if bad:
        raise SystemExit(
            "Git would record a private " + " and ".join(bad) + " email.\n" + FIX
        )
    print("Git identity is public")


if __name__ == "__main__":
    main(sys.argv[1:])
