#!/usr/bin/env python3
"""Build and validate the pre-specified Normal threshold plans."""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
KEY = "0x464f545445503032"
FIELDS = ("run_id","set_name","stream_id","seed_namespace","seed_digest","J",
          "window_position","burn_in_h","stop_time_h","window_h","use")
RANGES = {"cal_thr": range(40000,40350), "far_ver": range(50000,50150),
          "smoke_cal_thr": range(49900,49901), "smoke_far_ver": range(49901,49902)}

def digest(namespace: str, ordinal: int, stream: int) -> str:
    return hashlib.sha256(f"{KEY}|{namespace}|{ordinal}|{stream}".encode()).hexdigest()

def draw(namespace: str, ordinal: int, stream: int, upper: int) -> tuple[int,str]:
    d = digest(namespace, ordinal, stream)
    return int(d[:16], 16) % upper + 1, d

def build_rows(kind: str):
    ns = "fot-tep/fase03/soglie_normal/cal_thr/j/v1" if "cal" in kind else "fot-tep/fase03/soglie_normal/far_ver/position/v1"
    rows = []
    for ordinal, stream in enumerate(RANGES[kind], 1):
        if "cal" in kind:
            j, d = draw(ns, ordinal, stream, 10)
            if kind == "smoke_cal_thr":
                j = 1
            pos, stop = j, 20 + 5*j
            use = "threshold" if kind == "cal_thr" else "smoke"
        else:
            pos, d = draw(ns, ordinal, stream, 10)
            j, stop, use = 10, 70, ("far_ver" if kind == "far_ver" else "smoke")
        rows.append({"run_id":f"{kind}-{ordinal:03d}","set_name":kind,"stream_id":stream,
          "seed_namespace":ns,"seed_digest":d,"J":j,"window_position":pos,
          "burn_in_h":20,"stop_time_h":stop,"window_h":5,"use":use})
    return rows

def validate_rows(rows, kind):
    assert len(rows) == len(RANGES[kind])
    assert len({r["stream_id"] for r in rows}) == len(rows)
    assert all(1 <= int(r["J"]) <= 10 for r in rows)
    assert all(int(r["window_position"]) == int(r["J"]) for r in rows if "cal" in kind)
    assert all(int(r["stop_time_h"]) == (20+5*int(r["J"]) if "cal" in kind else 70) for r in rows)
    occupied = set()
    mod = importlib.util.spec_from_file_location("p", ROOT/"studio2/fase02/build_generation_plan.py")
    m = importlib.util.module_from_spec(mod); mod.loader.exec_module(m)
    for values in m.STREAM_RANGES.values(): occupied.update(values)
    occupied.update(range(30000,30040))
    assert not ({int(r["stream_id"]) for r in rows} & occupied)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("kind", choices=RANGES); ap.add_argument("output", type=Path); a=ap.parse_args()
    out=a.output.resolve()
    if out.parent != HERE/"plans": ap.error("output must be under soglie_normal/plans")
    if out.exists(): ap.error(f"refusing to overwrite {out}")
    rows=build_rows(a.kind); validate_rows(rows,a.kind); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("x",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(f"OK: {len(rows)} rows; sha256={hashlib.sha256(out.read_bytes()).hexdigest()}")
if __name__ == "__main__": main()
