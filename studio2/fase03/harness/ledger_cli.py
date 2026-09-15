"""Explicit local reconciliation/authorization. Never performs transport."""
import argparse
from pathlib import Path
from .ledger import PilotLedger
from .common import canonical_json


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--pilot-id',required=True)
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
    a=p.parse_args();ledger=PilotLedger(a.ledger,pilot_id=a.pilot_id)
    if a.action=='reconcile-zero-token':ledger.reconcile_zero_token(a.request_id,evidence_path=a.evidence,approval_path=a.approval)
    if a.action=='authorize-remediation':ledger.authorize_remediation(diff_path=a.diff,template_path=a.template,approval_path=a.approval)
    print(canonical_json(ledger.snapshot()))
    return 0


if __name__=='__main__':raise SystemExit(main())
