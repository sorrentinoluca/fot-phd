#!/usr/bin/env python3
"""Read-only query: which scientific lots are marked by a failed canary (rilievo C4).

Opens the final-batch ledger without binding a stage, without reserving anything and
without writing: it only reads events and timestamps, so it can be run at any time,
including after the campaign, and its answer is reproducible from the ledger alone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.canary_marking import marking  # noqa: E402
from studio2.fase03.harness.common import load_json  # noqa: E402
from studio2.fase03.harness.ledger import PilotLedger  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="TARGET_FINALE_7_4.json of the batch")
    parser.add_argument("--ledger", type=Path, help="ledger path (alternative to --target)")
    parser.add_argument("--pilot-id", help="ledger pilot_id (with --ledger)")
    parser.add_argument("--full", action="store_true", help="print every marked request id")
    arguments = parser.parse_args(argv)

    if arguments.target:
        target = load_json(arguments.target)
        path, pilot_id = Path(target["ledger"]["path"]), target["ledger"]["pilot_id"]
    elif arguments.ledger and arguments.pilot_id:
        path, pilot_id = arguments.ledger, arguments.pilot_id
    else:
        parser.error("pass --target, or --ledger together with --pilot-id")

    ledger = PilotLedger(path, pilot_id=pilot_id, profile="final_batch")
    value = marking(ledger)
    if not arguments.full:
        value = dict(value, marked_request_ids=value["marked_request_ids"][:20],
                     truncated=len(value["marked_request_ids"]) > 20)
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
