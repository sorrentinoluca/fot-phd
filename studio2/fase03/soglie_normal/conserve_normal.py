#!/usr/bin/env python3
"""Create the file-level conservation manifest for the completed Normal lot."""
import argparse,csv,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
 paths=[]
 paths += sorted((HERE/'runs'/'normal_001').rglob('*'))
 paths += [HERE/'runtime'/'batch_launch'/'matlab.log',HERE/'runtime'/'batch_launch'/'matlab.pid']
 paths += [HERE/'plans'/'cal_thr.csv',HERE/'plans'/'far_ver.csv',HERE/'CAL_THR_SCORES.csv',HERE/'THRESHOLD_FREEZE.json',HERE/'FAR_VERIFICATION.json',HERE/'FAR_VERIFICATION.md',HERE/'LOT_AUDIT.json',HERE/'R2_GUARD_RECHECK.json',HERE/'SPECIFICA_SOGLIE_NORMAL.md',HERE/'HANDOFF_BATCH.md',HERE/'REPORT_SOGLIE_NORMAL.md']
 paths=sorted({p for p in paths if p.is_file()})
 with a.output.open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n'); w.writerow(['path','bytes','sha256'])
  for p in paths: w.writerow([str(p.relative_to(ROOT)),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
 print(f'files={len(paths)} bytes={sum(p.stat().st_size for p in paths)} manifest={a.output}')
if __name__=='__main__': main()
