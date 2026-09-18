"""Explicit local reconciliation/authorization. Never performs transport."""
import argparse
import sqlite3
from contextlib import closing
from pathlib import Path
from .ledger import PROFILE_EVENT_PREFIX, PilotLedger
from .common import HarnessError, canonical_json


def declared_profile(path: Path) -> str:
    """The quota envelope the ledger itself declares.

    A ledger written before 7.4 declares nothing and is, by definition, a pilot ledger.
    Reading the declaration instead of assuming it is what lets this tool open a
    ``final_batch`` ledger at all -- the reconciliation path of D3 runs through here.
    """
    if not Path(path).is_file():
        raise HarnessError(f"ledger not found: {path}")
    with closing(sqlite3.connect(f"file:{Path(path)}?mode=ro", uri=True)) as c:
        declared = [r[0] for r in c.execute("SELECT event FROM events")
                    if r[0].startswith(PROFILE_EVENT_PREFIX)]
    if len(declared) > 1:
        raise HarnessError("ledger declares more than one quota profile")
    return declared[0][len(PROFILE_EVENT_PREFIX):] if declared else "pilot"


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--pilot-id',required=True)
    p.add_argument('--profile',default=None,
                   help='quota envelope; by default the one the ledger declares')
    sub=p.add_subparsers(dest='action',required=True)
    sub.add_parser('status')
    reconcile=sub.add_parser('reconcile-zero-token')
    reconcile.add_argument('--request-id',required=True)
    reconcile.add_argument('--evidence',type=Path,required=True)
    reconcile.add_argument('--approval',type=Path,required=True)
    remediation=sub.add_parser('authorize-remediation')
    remediation.add_argument('--diff',type=Path,required=True)
    remediation.add_argument('--template',type=Path,required=True)
    remediation.add_argument('--approval',type=Path,required=True)
    a=p.parse_args()
    ledger=PilotLedger(a.ledger,pilot_id=a.pilot_id,profile=a.profile or declared_profile(a.ledger))
    if a.action=='reconcile-zero-token':ledger.reconcile_zero_token(a.request_id,evidence_path=a.evidence,approval_path=a.approval)
    if a.action=='authorize-remediation':ledger.authorize_remediation(diff_path=a.diff,template_path=a.template,approval_path=a.approval)
    print(canonical_json(ledger.snapshot()))
    return 0


if __name__=='__main__':raise SystemExit(main())
