#!/bin/bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PLAN="$HERE/plans/ood_preflight_03_11.csv"
DEST="$HERE/ood_preflight/ood_preflight_001"
LAUNCH="$HERE/runtime/ood_preflight_03_11"
python3 "$HERE/fault_protocol.py" preflight "$PLAN" "$DEST"
mkdir "$LAUNCH"
/usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('$HERE'); generate_fault_runs('$PLAN','$DEST')" \
  > "$LAUNCH/matlab.log" 2>&1
printf '%s\n' "$?" > "$LAUNCH/exit_code"
