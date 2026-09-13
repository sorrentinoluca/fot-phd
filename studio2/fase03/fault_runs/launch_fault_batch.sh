#!/bin/bash
# This file is delivered, not executed in the preparation window.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
DEST="$HERE/runs/fault_dev_001"
PLAN="$HERE/plans/fault_dev.csv"
LAUNCH="$HERE/runtime/batch_launch"
python3 "$HERE/fault_protocol.py" preflight "$PLAN" "$DEST"
mkdir "$LAUNCH"  # Atomic exclusive launch claim; refuse overwrite/rerun.
# Source/MEX are prepared and verified before this command, never rebuilt during a batch.
nohup /usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
 "addpath('$HERE'); generate_fault_runs('$PLAN','$DEST')" \
 > "$LAUNCH/matlab.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$LAUNCH/matlab.pid"
printf 'MATLAB PID=%s; log=%s\n' "$!" "$LAUNCH/matlab.log"
