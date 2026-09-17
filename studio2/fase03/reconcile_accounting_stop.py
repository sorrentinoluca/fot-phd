#!/usr/bin/env python3
"""Reconcile the original spurious 122B accounting STOP; plan-only unless acknowledged.

Offline only: no provider call, no request, no deletion of the STOP.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import HarnessError, canonical_json, load_json  # noqa: E402

ACK = "RECONCILE_PHASE03_ACCOUNTING_STOP"


def run(*, ledger_path: Path, pilot_id: str, approval_path: Path, fixed_commit: str,
        provider_path: Path, snapshot: Path) -> dict:
    from studio2.fase03.harness.guards import verify_tokenizer
    from studio2.fase03.harness.ledger import PilotLedger, load_tokenizer_accounting_guard
    from studio2.fase03.producer_probe import provider_config
    if not ledger_path.is_absolute() or not ledger_path.is_file():
        raise HarnessError("reconciliation requires an existing absolute ledger")
    provider = provider_config(provider_path)
    if "tokenizer_accounting" not in provider:
        raise HarnessError("reconciliation requires the frozen 122B accounting provider config")
    verify_tokenizer(snapshot, **provider["tokenizer"])
    guard = load_tokenizer_accounting_guard(snapshot)
    ledger = PilotLedger(ledger_path, pilot_id=pilot_id)
    return ledger.reconcile_accounting_stop(
        approval_path=approval_path, fixed_commit=fixed_commit, guard=guard)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--fixed-commit", required=True)
    parser.add_argument("--provider-config", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args(argv)
    if not args.execute:
        approval = load_json(args.approval)
        print(canonical_json({"status": "PLAN_ONLY", "ledger": str(args.ledger),
                              "pilot_id": args.pilot_id, "approval": approval,
                              "fixed_commit": args.fixed_commit,
                              "requires": f"--execute --acknowledge {ACK}"}))
        return 0
    if args.acknowledge != ACK:
        raise SystemExit(f"reconciliation requires --execute --acknowledge {ACK}")
    result = run(ledger_path=args.ledger, pilot_id=args.pilot_id,
                 approval_path=args.approval, fixed_commit=args.fixed_commit,
                 provider_path=args.provider_config, snapshot=args.model_snapshot)
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
