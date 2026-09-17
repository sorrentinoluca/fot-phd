#!/bin/bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CANDIDATE=${1:?candidate: F5 or F12}
case "$CANDIDATE" in
  F5) KIND=test_batch_f5 ;;
  F12) KIND=test_batch_f12 ;;
  *) exit 2 ;;
esac
PLAN="$HERE/plans/${KIND}.csv"
DEST="$HERE/test_batch/${KIND}_001"
python3 "$HERE/fault_protocol.py" preflight "$PLAN" "$DEST"
/usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('$HERE'); generate_fault_runs('$PLAN','$DEST')" \
  > "$HERE/runtime/${KIND}.matlab.log" 2>&1
