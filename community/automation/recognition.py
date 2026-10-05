"""Offline contributor recognition decision engine; no network or live award API.

Trust contract for `decide()`: every proof, ID, repository and merge field must
come from a verified adapter (GitHub/Reddit APIs), never from a form. Values are
checked with exact types, so text such as "false" or "yes" never counts as true.
"""

from dataclasses import dataclass
import hashlib
import json
import re

OWNER = "adidshaft"
ALLOWED_REPOSITORIES = frozenset(
    OWNER + "/" + name
    for name in [
        "grok-gadgets",
        "grok-gadgets-gateway",
        "grok-gadgets-linux-sdk",
        "grok-gadgets-esp32-sdk",
        "grok-gadgets-home-assistant",
    ]
)
REPLACEABLE_FLAIRS = frozenset(["", "contributor"])
REDDIT_ID = re.compile(r"t2_[a-z0-9]{1,16}")


@dataclass(frozen=True)
class Decision:
    outcome: str
    reason: str
    award_key: str | None = None


def _github_id(value):
    return value if type(value) is int and value > 0 else None


def _reddit_id(value):
    return value if isinstance(value, str) and REDDIT_ID.fullmatch(value) else None


def _flag(value):
    """None/False mean unset; True means set; anything else is malformed."""
    if value is None or value is False:
        return False
    if value is True:
        return True
    raise ValueError


def award_key(reddit_id):
    return "contributor:reddit:" + reddit_id


def decide(record, previous_awards=frozenset(), active_links=None):
    """Return one decision. `active_links` maps {"github": {id: reddit}, "reddit": {id: github}}."""
    try:
        revoked = _flag(record.get("revoked"))
        changed = _flag(record.get("deleted")) or _flag(record.get("renamed"))
    except ValueError:
        return Decision("review", "Malformed account state")
    gh = record.get("github_proof") or {}
    rd = record.get("reddit_proof") or {}
    gh_id = _github_id(gh.get("immutable_id"))
    rd_id = _reddit_id(rd.get("immutable_id"))
    if record.get("consent") is not True or revoked:
        key = award_key(rd_id) if rd_id else None
        if key and key in previous_awards:
            return Decision("would_remove", "Consent revoked after an award", key)
        return Decision("ineligible", "Consent absent or revoked")
    if changed:
        return Decision("review", "Account changed; repeat ownership proof")
    if (
        gh.get("verified") is not True
        or rd.get("verified") is not True
        or not gh_id
        or not rd_id
    ):
        return Decision("ineligible", "Both typed account ownership proofs required")
    if gh.get("type", "User") != "User":
        return Decision("ineligible", "Automation accounts are not recognized")
    override = record.get("manual_override")
    if override is not None:
        if isinstance(override, str) and override.strip().lower() == "deny":
            return Decision("ineligible", "Manual denial")
        return Decision("review", "Unknown manual override")
    flair = record.get("current_flair")
    if flair is not None and (
        not isinstance(flair, str) or flair.strip().lower() not in REPLACEABLE_FLAIRS
    ):
        return Decision("preserve", "Existing flair preserved")
    links = active_links or {}
    linked_reddit = links.get("github", {}).get(gh_id)
    linked_github = links.get("reddit", {}).get(rd_id)
    if (linked_reddit not in (None, rd_id)) or (linked_github not in (None, gh_id)):
        return Decision("review", "Account already linked to a different account")
    eligible = [
        pr
        for pr in record.get("contributions", [])
        if pr.get("repository") in ALLOWED_REPOSITORIES
        and pr.get("merged") is True
        and pr.get("author_id") == gh_id
        and type(pr.get("author_id")) is int
        and pr.get("author_type", "User") == "User"
        and pr.get("automation") in (None, False)
    ]
    if not eligible:
        return Decision("ineligible", "No eligible merged contribution")
    key = award_key(rd_id)
    if key in previous_awards:
        return Decision("already_awarded", "Idempotent prior award", key)
    return Decision(
        "would_award", "Opt-in ownership and merged contribution verified", key
    )


def dry_run(records, previous_awards=frozenset(), active_links=None, now=None):
    # Decision log deliberately excludes account mappings, proofs, and tokens.
    log = []
    for n, r in enumerate(records):
        d = decide(r, previous_awards, active_links)
        digest = hashlib.sha256(
            json.dumps(r, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        entry = dict(
            index=n,
            outcome=d.outcome,
            reason=d.reason,
            inputs_digest=digest,
            award_key_hash=(
                hashlib.sha256(d.award_key.encode()).hexdigest()[:16]
                if d.award_key
                else None
            ),
            dry_run=True,
        )
        if now:
            entry["timestamp"] = now
        log.append(entry)
    return log


RETRYABLE = (TimeoutError, ConnectionError)


def apply_with_adapter(decision, adapter, *, dry_run=True, max_attempts=3, sleep=None):
    """Dependency injection only. Production adapter/runtime not implemented or activated."""
    if decision.outcome not in ("would_award", "would_remove"):
        return {"outcome": decision.outcome, "attempts": 0}
    if dry_run:
        return {"outcome": decision.outcome, "attempts": 0, "dry_run": True}
    if not 1 <= max_attempts <= 3:
        raise ValueError("Retries must be bounded 1..3")
    removing = decision.outcome == "would_remove"
    for attempt in range(1, max_attempts + 1):
        try:
            if removing:
                adapter.remove(decision.award_key)
                return {"outcome": "removed", "attempts": attempt}
            adapter.award(decision.award_key)
            return {"outcome": "awarded", "attempts": attempt}
        except PermissionError:
            return {"outcome": "authorization_revoked", "attempts": attempt}
        except RETRYABLE:
            # Outcome unknown: query idempotent state before retrying the same key.
            awarded = adapter.was_awarded(decision.award_key)
            if awarded != removing:
                return {
                    "outcome": "removed" if removing else "awarded",
                    "attempts": attempt,
                }
            if sleep and attempt < max_attempts:
                sleep(2 ** (attempt - 1))
    return {
        "outcome": "review",
        "reason": "Retry budget exhausted",
        "attempts": max_attempts,
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Offline fixtures only; no live APIs")
    p.add_argument("fixture")
    args = p.parse_args()
    with open(args.fixture) as f:
        records = json.load(f)
    print(json.dumps(dry_run(records), indent=2))
