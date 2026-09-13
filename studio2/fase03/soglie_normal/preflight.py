#!/usr/bin/env python3
import csv, sys
from pathlib import Path
if len(sys.argv)!=4: raise SystemExit('usage: preflight.py cal.csv far.csv destination')
cal,far,dest=map(Path,sys.argv[1:]); rows=[]
for p in (cal,far):
    if not p.is_file(): raise SystemExit(f'missing plan: {p}')
    rows += list(csv.DictReader(p.open()))
if len(rows) not in (2,500): raise SystemExit(f'unexpected rows: {len(rows)}')
if len({r['stream_id'] for r in rows})!=len(rows): raise SystemExit('duplicate stream')
if dest.exists(): raise SystemExit(f'refusing existing destination: {dest}')
if any(1000<=int(r['stream_id'])<=1009 or 30000<=int(r['stream_id'])<=30039 for r in rows): raise SystemExit('pilot/fault stream collision')
print(f'preflight accepted rows={len(rows)} destination={dest}')
