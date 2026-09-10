#!/usr/bin/env bash
# C06 B_LOCAL_FIRST_V1 full test launcher
# 120 agent-cases x 3 replicas = 360 API calls to gpt-5.6-terra
#
# Usage:
#   cd /Users/luker/fot-tep
#   bash phase_b/c06/full_test/run_c06_full_test.sh
#
# Prerequisites:
#   - OPENAI_API_KEY set in environment
#   - /Users/luker/fot-c06-env with openai==3.6.0 installed
#
# The runner is resumable: if interrupted, re-run the same command.
# Existing records are validated and skipped automatically.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "=== C06 B_LOCAL_FIRST_V1 full test ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Verify API key
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "ERROR: OPENAI_API_KEY is not set."
    echo "  export OPENAI_API_KEY='sk-...'"
    exit 1
fi
echo "API key: present (${#OPENAI_API_KEY} chars)"

# Verify venv
VENV_PYTHON="/Users/luker/fot-c06-env/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "ERROR: venv python not found at $VENV_PYTHON"
    echo "Create it with:"
    echo "  python3 -m venv /Users/luker/fot-c06-env"
    echo "  /Users/luker/fot-c06-env/bin/pip install openai==3.6.0"
    exit 1
fi
echo "Python: $VENV_PYTHON"

# Verify openai SDK version
SDK_VERSION=$("$VENV_PYTHON" -c "import openai; print(openai.__version__)")
if [ "$SDK_VERSION" != "3.6.0" ]; then
    echo "ERROR: openai SDK is $SDK_VERSION, expected 3.6.0"
    exit 1
fi
echo "OpenAI SDK: $SDK_VERSION"
echo ""

cd "$PROJECT_ROOT"

# Step 1: Preflight
echo "--- Preflight check ---"
PYTHONPATH="$PROJECT_ROOT" "$VENV_PYTHON" -m phase_b.c06.full_test.run_full_test --preflight
echo ""

# Step 2: Execute
echo "--- Starting inference (360 calls) ---"
echo "Estimated cost: ~USD 2.42 (uncached ceiling)"
echo "Estimated time: 10-20 minutes"
echo ""
PYTHONPATH="$PROJECT_ROOT" "$VENV_PYTHON" -m phase_b.c06.full_test.run_full_test --execute
echo ""

# Step 3: Evaluate
echo "--- Running stratified evaluation ---"
PYTHONPATH="$PROJECT_ROOT" "$VENV_PYTHON" -m phase_b.c06.full_test.evaluate
echo ""
echo "=== Full test complete ==="
echo "Results: phase_b/c06/full_test/inference/full_test_results.json"
echo "Report:  phase_b/c06/full_test/inference/FULL_TEST_REPORT.md"
