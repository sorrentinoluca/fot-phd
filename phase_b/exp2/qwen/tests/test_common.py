from __future__ import annotations

import unittest
from unittest.mock import patch

from phase_b.exp2.qwen.common import tokenize_prompt


class CommonTests(unittest.TestCase):
    @patch("phase_b.exp2.qwen.common.http_json")
    def test_tokenize_uses_server_root_not_v1(self, mocked):
        mocked.return_value = {"count": 123}
        count = tokenize_prompt(
            {
                "base_url": "http://127.0.0.1:8000/v1",
                "requested_model": "fot-exp2-consumer",
            },
            "prompt",
        )
        self.assertEqual(count, 123)
        self.assertEqual(
            mocked.call_args.args[0], "http://127.0.0.1:8000/tokenize"
        )


if __name__ == "__main__":
    unittest.main()
