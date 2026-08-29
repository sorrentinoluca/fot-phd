from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "code/verbalizer_config_v2.json": "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519",
    "code/tep_verbalize_v2.py": "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be",
    "code/evaluate_verbalizer_v2.py": "972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92",
    "code/tep_features.py": "cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c",
}


class PhaseAFrozenHashTests(unittest.TestCase):
    def test_phase_a_frozen_hashes_unchanged(self) -> None:
        for relative, expected in EXPECTED.items():
            observed = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(observed, expected, relative)


if __name__ == "__main__":
    unittest.main()
