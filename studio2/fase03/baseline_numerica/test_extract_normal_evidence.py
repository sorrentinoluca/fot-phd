from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .extract_normal_evidence import (
    EXPECTED_EXTRACTOR_SHA256,
    load_verified_extractor,
)


class ExtractNormalEvidenceTests(unittest.TestCase):
    def test_extractor_guard_rejects_changed_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "extract_evidence.py").write_text("# changed\n", encoding="utf-8")
            (root / "leakage.py").write_text("# changed\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "extractor guard failed"):
                load_verified_extractor(root / "extract_evidence.py")

    def test_expected_extractor_hash_is_fixed(self) -> None:
        self.assertEqual(len(EXPECTED_EXTRACTOR_SHA256), 64)


if __name__ == "__main__":
    unittest.main()
