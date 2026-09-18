#!/usr/bin/env python3
"""Per-call ledger overhead of the final batch, measured on a COPY of a real ledger.

No model call, no write on the original: the ledger is copied with the SQLite backup API
(WAL included) into a temporary directory and opened there, with the original path as
identity so the D9 configuration still recognises it.

    "$PY" studio2/fase03/batch_finale/bench_ledger_overhead.py \\
        --code-root <worktree> --ledger <ledger.sqlite3> --pilot-id <id> [--stage final_batch_r1]

Run it once with the worktree of the old code and once with the new one: the two
``per_call_ms`` are the fixed cost that every transport call pays before the request.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import tempfile
import time


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--stage", default="final_batch_r1")
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()
    sys.path.insert(0, str(args.code_root.resolve()))
    from studio2.fase03.harness.ledger import PilotLedger

    source = args.ledger.resolve()
    copy = Path(tempfile.mkdtemp(prefix="bench-ledger-")) / "ledger.sqlite3"
    with closing(sqlite3.connect(f"file:{source}?mode=ro", uri=True)) as src, \
            closing(sqlite3.connect(copy)) as dst:
        src.backup(dst)
    ledger = PilotLedger(copy, pilot_id=args.pilot_id, identity_path=source,
                         profile="final_batch")
    rows = ledger.snapshot()["native_requests"]
    timings = []
    for _ in range(args.repeat):
        begin = time.perf_counter()
        binding = ledger.binding(args.stage)       # what Provider.call does before sending
        ledger.bind_stage(args.stage, binding)
        timings.append((time.perf_counter() - begin) * 1000)
    print({"code_root": str(args.code_root), "rows": rows,
           "first_call_ms": round(timings[0], 1),
           "per_call_ms": round(sorted(timings[1:])[len(timings[1:]) // 2], 1)
           if len(timings) > 1 else None})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
