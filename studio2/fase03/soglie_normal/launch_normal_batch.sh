#!/bin/bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
MODE=${1:?mode: smoke|batch}
if [[ "$MODE" == smoke ]]; then
  CAL="$HERE/plans/smoke_cal_thr.csv"; FAR="$HERE/plans/smoke_far_ver.csv"; DEST="$HERE/runs/smoke_001"
  python3 "$HERE/preflight.py" "$CAL" "$FAR" "$DEST"; mkdir "$HERE/runtime/smoke_launch"
  nohup /usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch "addpath('$HERE'); generate_normal_runs_soglie('$CAL','$DEST/cal_thr'); generate_normal_runs_soglie('$FAR','$DEST/far_ver')" > "$HERE/runtime/smoke_launch/matlab.log" 2>&1 < /dev/null &
elif [[ "$MODE" == batch ]]; then
  CAL="$HERE/plans/cal_thr.csv"; FAR="$HERE/plans/far_ver.csv"; DEST="$HERE/runs/normal_001"
  python3 "$HERE/preflight.py" "$CAL" "$FAR" "$DEST"; mkdir "$HERE/runtime/batch_launch"
  nohup /usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch "addpath('$HERE'); generate_normal_runs_soglie('$CAL','$DEST/cal_thr'); generate_normal_runs_soglie('$FAR','$DEST/far_ver')" > "$HERE/runtime/batch_launch/matlab.log" 2>&1 < /dev/null &
else exit 2; fi
echo "$!" > "$HERE/runtime/${MODE}_launch/matlab.pid"; echo "MATLAB PID=$!"
