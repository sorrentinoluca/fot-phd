"""Frozen constants for the C06 B_LOCAL_FIRST_V1 screening."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
C06_ROOT = ROOT / "phase_b" / "c06"

VARIANT = "B_LOCAL_FIRST_V1"
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
SDK_VERSION = "3.6.0"
REPETITIONS = 3
MAX_OUTPUT_TOKENS = 512
MAX_STRUCTURAL_RETRIES = 2
TEMPERATURE = None
SEED = None
STORE = False

INFERENCE_TAG = "exp3-v2-inference-frozen-001"
INFERENCE_PAYLOAD_COMMIT = "9f6ef6eb58b677b623c8c9ed5c33fb9768b018aa"
VERBALIZATION_TAG = "exp3-v2-verbalizations-frozen-001"
VERBALIZATION_PAYLOAD_COMMIT = "5be0c3c14e7e1601708486d56c2cb4cee29658ab"
HARNESS_TAG = "exp3-v2-inference-harness-frozen-001"
HARNESS_TAG_OBJECT = "df1f77fee805b19d7a6e782c0ea696dd6c3ffa07"
HARNESS_COMMIT = "24b030a07652649556953aaa1a2cfb29e54ab2f7"
INFERENCE_TAG_OBJECT = "e1aa80d2f54d4cefdbc7273cbcdb139f0df57563"
INFERENCE_GOVERNANCE_COMMIT = "9a7ccaa95bae8c0d2d00dc0959e177eb90a5cd61"
VERBALIZATION_TAG_OBJECT = "4eeb14e77c5d5b45395da0d88012bcf30cea83ea"
VERBALIZATION_GOVERNANCE_COMMIT = "4159fba5e4d23cbc9af62c2aad72f11eda1491db"

AGENT_PACK = {
    "agent_1": "LKP-001",
    "agent_2": "LKP-002",
    "agent_3": "LKP-003",
    "agent_4": "LKP-004",
}

LOCAL_CASES = {
    "agent_1": tuple(f"EXP3V2-F1-{index:03d}" for index in range(1, 7)),
    "agent_2": tuple(f"EXP3V2-F8-{index:03d}" for index in range(1, 7)),
    "agent_3": tuple(f"EXP3V2-F10-{index:03d}" for index in range(1, 7)),
    "agent_4": tuple(f"EXP3V2-F13-{index:03d}" for index in range(1, 7)),
}

LOCAL_FIRST_BLOCK = """DECISION POLICY
First compare the case with the local labeled examples. Prefer a local match supported by specific variables and temporal behavior; use peer observations mainly when the local examples do not provide a good match. Do not choose a peer-supported label from global counts or generic persistence alone. If local and peer evidence are both plausible and neither is clearly stronger, abstain."""

PROMPT_ANCHOR = (
    "You are a diagnostic reasoning agent. Use only the supplied local labeled "
    "examples, optional peer observations, and the neutral case description. "
    "Choose from the supplied label space. The neutral description contains "
    "observations, not a diagnosis. Return strict JSON only, without markdown or "
    "extra keys."
)

CORRECTION_SUFFIX = """

CORRECTION REQUIRED
The previous response failed strict schema validation. Return only one valid JSON object with exactly: predicted_label, abstain, used_insight_ids, reasoning_summary. Do not add markdown, confidence, or any other key.
""".rstrip()

FROZEN_WORKTREE_HASHES = {
    "phase_b/conditions/builders.py": "5a4906304e5ab09ad12cd004e8838dd337ac2f5544ac03d0c392f21ae2009bd9",
    "phase_b/conditions/diagnostic_output.openai.schema.json": "6ef214cdebbfe06e59a7a5a2f51f3fb93dd8d47e8397f6bc5bc68047e1364bf8",
    "phase_b/conditions/diagnostic_output.schema.json": "5abed6a82be2ecd1a6654a32124338fe08c1dceae0c24b51e0ec9e6c99363b19",
    "phase_b/conditions/parser.py": "bdddfe99ba6e4328a071ea94c221a91cc5942252865691a280bcd6687301eb99",
    "phase_b/conditions/retry.py": "ba144230e0e99111c7b6154acc7574aec32aeddb2146bf2a39ff8d6af5321b29",
    "phase_b/config/protocol_config.json": "a67b721609647c9a428c9895de1f0d684547e9fc8cf91f0a626f823af094e135",
    "phase_b/execution/openai_adapter.py": "39d7317e3a0c7808d297617356dfc580120b0f32c58a5e6e71eb45bf9f3eee06",
    "phase_b/insights/final_local_insights.json": "b7ea847ccaf72b04c407ae4878924719c5363d4ccc6851d3d5fef79386e4bcfd",
    "phase_b/insights/peer_libraries/agent_1_B.json": "262768a6cada9e88106faa8d07367bb565e5ea0fdb9155cdee1095137a69693f",
    "phase_b/insights/peer_libraries/agent_2_B.json": "4b0b5bdd228cb1daee5089691fb4612cbd0b7d337153f87264d9433d27e6b083",
    "phase_b/insights/peer_libraries/agent_3_B.json": "fe5606c35e6a483f5db46acea7b8dae3c238bc2f02423e7b726fe8961528a9a0",
    "phase_b/insights/peer_libraries/agent_4_B.json": "620ace1214f9ee7b163920deaadef7ee9d16d43ad7bb1de710f3a4559feaf4b3",
    "phase_b/local_knowledge/local_examples.json": "468d51b7987b8655fc80638d99366dbe3632af0606c9034ca6db7fd1fdcd0a5c",
    "phase_b/prompts/fot_B.txt": "cecc664e5d9b9558ca7f8675bee37ae59a5d97a5ff0518175a8a8855a5328289",
    "phase_b/prompts/leakage.py": "da1a39c72d36d7c04d276097d2de4c57fecb94642027870bd802b449b429ee76",
}
