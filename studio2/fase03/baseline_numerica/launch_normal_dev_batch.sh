#!/bin/bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PLAN="$HERE/plans/normal_dev.csv"
DEST="$HERE/runs/normal_dev_001"
RUNTIME="$HERE/runtime/normal_dev_001"

python3 "$HERE/preflight_normal_dev.py" "$PLAN" "$DEST"
if [[ -e "$RUNTIME" ]]; then
  echo "refusing existing runtime directory: $RUNTIME" >&2
  exit 2
fi
mkdir -p "$RUNTIME"
nohup /usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('$HERE'); generate_normal_dev_runs('$PLAN','$DEST')" \
  > "$RUNTIME/matlab.log" 2>&1 < /dev/null &
pid=$!
echo "$pid" > "$RUNTIME/matlab.pid"
echo "MATLAB PID=$pid log=$RUNTIME/matlab.log"
