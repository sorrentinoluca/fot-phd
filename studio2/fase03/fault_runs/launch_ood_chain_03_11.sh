#!/bin/bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CANDIDATE=${1:?candidate: F5 or F12}
case "$CANDIDATE" in
  F5) KIND=ood_chain_f5; DEST="$HERE/ood_chain_f5/chain_f5_001" ;;
  F12) KIND=ood_chain_f12; DEST="$HERE/ood_chain_f12/chain_f12_001" ;;
  *) exit 2 ;;
esac
PLAN="$HERE/plans/${KIND}.csv"
python3 "$HERE/fault_protocol.py" preflight "$PLAN" "$DEST"
/usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('$HERE'); generate_fault_runs('$PLAN','$DEST')" \
  > "$HERE/runtime/${KIND}.matlab.log" 2>&1
