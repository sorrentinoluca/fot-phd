"""Constants for the C06 B_LOCAL_FIRST_V1 full test (120 agent-cases, 360 calls).

Imports and extends the screening constants; adds the complete case set and
stratum definitions.
"""

from __future__ import annotations

from pathlib import Path

from phase_b.c06.constants import (  # noqa: F401 — re-exported
    AGENT_PACK,
    C06_ROOT,
    CORRECTION_SUFFIX,
    FROZEN_WORKTREE_HASHES,
    HARNESS_COMMIT,
    HARNESS_TAG,
    HARNESS_TAG_OBJECT,
    INFERENCE_GOVERNANCE_COMMIT,
    INFERENCE_PAYLOAD_COMMIT,
    INFERENCE_TAG,
    INFERENCE_TAG_OBJECT,
    LOCAL_CASES,
    LOCAL_FIRST_BLOCK,
    MAX_OUTPUT_TOKENS,
    MAX_STRUCTURAL_RETRIES,
    MODEL,
    PROMPT_ANCHOR,
    REASONING_EFFORT,
    REPETITIONS,
    ROOT,
    SDK_VERSION,
    SEED,
    STORE,
    TEMPERATURE,
    VARIANT,
    VERBALIZATION_GOVERNANCE_COMMIT,
    VERBALIZATION_PAYLOAD_COMMIT,
    VERBALIZATION_TAG,
    VERBALIZATION_TAG_OBJECT,
)

FULL_TEST_ROOT = C06_ROOT / "full_test"

# ---------------------------------------------------------------------------
# Complete case set — 4 agents × 30 cases = 120 agent-case groups
# ---------------------------------------------------------------------------

FAULT_PREFIXES = ("F1", "F8", "F10", "F13")
NORMAL_PREFIX = "N"
CASES_PER_CLASS = 6

ALL_CASE_IDS: tuple[str, ...] = tuple(
    f"EXP3V2-{prefix}-{index:03d}"
    for prefix in (*FAULT_PREFIXES, NORMAL_PREFIX)
    for index in range(1, CASES_PER_CLASS + 1)
)

AGENT_IDS: tuple[str, ...] = ("agent_1", "agent_2", "agent_3", "agent_4")

# Every (agent_id, physical_case_id) pair
ALL_AGENT_CASES: tuple[tuple[str, str], ...] = tuple(
    (agent_id, case_id)
    for agent_id in AGENT_IDS
    for case_id in ALL_CASE_IDS
)

assert len(ALL_AGENT_CASES) == 120

# ---------------------------------------------------------------------------
# Pseudolabel mapping (evaluator-side ground truth)
# ---------------------------------------------------------------------------

FAULT_TO_PSEUDOLABEL = {
    "F1": "CLS-ZOGAA",
    "F8": "CLS-OJNSG",
    "F10": "CLS-R463B",
    "F13": "CLS-Z3ISU",
}

AGENT_LOCAL_FAULT = {
    "agent_1": "F1",
    "agent_2": "F8",
    "agent_3": "F10",
    "agent_4": "F13",
}


def case_fault_prefix(case_id: str) -> str:
    """Extract the fault prefix from a physical case ID."""
    # EXP3V2-F1-001 → F1,  EXP3V2-F10-001 → F10,  EXP3V2-N-001 → N
    parts = case_id.split("-")
    return parts[1]


def expected_label(case_id: str) -> str:
    """Return the correct pseudolabel for a physical case ID."""
    prefix = case_fault_prefix(case_id)
    if prefix == NORMAL_PREFIX:
        return "Normal"
    return FAULT_TO_PSEUDOLABEL[prefix]


def stratum(agent_id: str, case_id: str) -> str:
    """Return the evaluation stratum for an (agent, case) pair."""
    prefix = case_fault_prefix(case_id)
    if prefix == NORMAL_PREFIX:
        return "normal"
    agent_fault = AGENT_LOCAL_FAULT[agent_id]
    if prefix == agent_fault:
        return "local-seen"
    return "local-unseen"


# Stratum sizes
STRATUM_SIZES = {
    "local-seen": 24,   # 4 agents × 6 own-fault cases
    "local-unseen": 72, # 4 agents × 18 other-fault cases
    "normal": 24,       # 4 agents × 6 Normal cases
}

assert sum(STRATUM_SIZES.values()) == 120

# ---------------------------------------------------------------------------
# Full test gates (from C06_FULL_TEST_PLAN.md and user specification)
# ---------------------------------------------------------------------------

GATES = {
    "local_seen_min": 23,
    "local_seen_n": 24,
    "local_unseen_min": 67,
    "local_unseen_n": 72,
    "normal_min": 24,
    "normal_n": 24,
    "parse_failures_max": 0,
}

PLANNED_CALLS = len(ALL_AGENT_CASES) * REPETITIONS  # 360
PLANNED_AGENT_CASES = len(ALL_AGENT_CASES)           # 120
