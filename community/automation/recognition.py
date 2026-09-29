"""Offline contributor recognition decision engine; no network or live award API."""
from dataclasses import dataclass
from datetime import datetime,timezone
import json
ALLOWED_REPOSITORIES=frozenset(['grok-gadgets','grok-gadgets-gateway','grok-gadgets-linux-sdk','grok-gadgets-esp32-sdk','grok-gadgets-home-assistant'])
@dataclass(frozen=True)
class Decision:
    outcome:str
    reason:str
    award_key:str|None=None

def decide(record,previous_awards=frozenset()):
    if not record.get('consent') or record.get('revoked'):return Decision('ineligible','Consent absent or revoked')
    if record.get('deleted') or record.get('renamed'):return Decision('review','Account changed; repeat ownership proof')
    # Trusted evidence inputs must come from a future verified adapter, never a browser form's self-assertion.
    gh=record.get('github_proof',{});rd=record.get('reddit_proof',{})
    if not gh.get('verified') or not rd.get('verified') or not gh.get('immutable_id') or not rd.get('immutable_id'):return Decision('ineligible','Both account ownership proofs required')
    if record.get('manual_override')=='deny':return Decision('ineligible','Manual denial')
    if record.get('current_flair') in ['Maintainer','Moderator']:return Decision('preserve','Higher-priority flair preserved')
    eligible=[pr for pr in record.get('contributions',[]) if pr.get('repository') in ALLOWED_REPOSITORIES and pr.get('merged') and pr.get('author_id')==gh['immutable_id'] and not pr.get('automation')]
    if not eligible:return Decision('ineligible','No eligible merged contribution')
    key='contributor:'+str(gh['immutable_id'])+':'+str(rd['immutable_id'])
    if key in previous_awards:return Decision('already_awarded','Idempotent prior award',key)
    return Decision('would_award','Opt-in ownership and merged contribution verified',key)

def dry_run(records,previous_awards=frozenset()):
    # Decision log deliberately excludes account mappings, proofs, and tokens.
    return [dict(index=n,outcome=(d:=decide(r,previous_awards)).outcome,reason=d.reason,dry_run=True) for n,r in enumerate(records)]

def apply_with_adapter(decision,adapter,*,dry_run=True,max_attempts=3):
    """Dependency injection only. Production adapter/runtime not implemented or activated."""
    if decision.outcome!='would_award':return {'outcome':decision.outcome,'attempts':0}
    if dry_run:return {'outcome':'would_award','attempts':0,'dry_run':True}
    if not 1<=max_attempts<=3:raise ValueError('Retries must be bounded 1..3')
    for attempt in range(1,max_attempts+1):
        try:adapter.award(decision.award_key);return {'outcome':'awarded','attempts':attempt}
        except PermissionError:return {'outcome':'authorization_revoked','attempts':attempt}
        except TimeoutError:
            # Outcome unknown: query idempotent state before retrying the same key.
            if adapter.was_awarded(decision.award_key):return {'outcome':'awarded','attempts':attempt}
    return {'outcome':'review','reason':'Retry budget exhausted','attempts':max_attempts}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description='Offline fixtures only; no live APIs');p.add_argument('fixture');args=p.parse_args()
    with open(args.fixture) as f:records=json.load(f)
    print(json.dumps(dry_run(records),indent=2))
