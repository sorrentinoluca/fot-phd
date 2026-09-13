"""Regression checks for D1 replay and its frozen-context guards; no scientific data."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('d1_replay', HERE / 'draw_d1.py')
d1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d1)


class DrawReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='d1-review-')
        cls.repo = Path(cls.temp.name) / 'repo'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet', str(ROOT), str(cls.repo)], check=True)
        # Only the two current normative inputs are materialized. Historical blobs
        # remain available through the local object store; no experiment data is read.
        for name in [d1.CRITERIA_PATH, d1.MANIFEST_PATH]:
            p = cls.repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())
        subprocess.run(['git', '-C', str(cls.repo), '-c', 'user.name=D1 replay test',
                        '-c', 'user.email=d1-replay@example.invalid', 'commit', '--allow-empty',
                        '--quiet', '-m', 'Temporary replay context after the original draw'], check=True)
        assert subprocess.check_output(['git', '-C', str(cls.repo), 'rev-parse', 'HEAD'], text=True).strip() != d1.DRAW_CONTEXT_COMMIT

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_exact_replay_after_head_advances(self):
        out = Path(self.temp.name) / 'replay.json'
        subprocess.run([sys.executable, str(HERE / 'draw_d1.py'), '--repo', str(self.repo),
                        '--draw-context-commit', d1.DRAW_CONTEXT_COMMIT, '--out', str(out)],
                       check=True, capture_output=True)
        self.assertEqual(out.read_bytes(), (HERE / 'D1_DRAW_LOG.json').read_bytes())

    def test_altered_criteria_stop_before_enumeration_or_draw(self):
        p = self.repo / d1.CRITERIA_PATH
        original = p.read_bytes()
        try:
            p.write_bytes(original + b'\ninvalid revision\n')
            with patch.object(sys, 'argv', ['draw_d1', '--repo', str(self.repo)]), \
                 patch.object(d1, 'enumerate_admissible') as enumeration, \
                 patch.object(d1, 'draw_index') as draw:
                with self.assertRaisesRegex(SystemExit, 'registro dei criteri'):
                    d1.main()
                enumeration.assert_not_called()
                draw.assert_not_called()
        finally:
            p.write_bytes(original)

    def test_unrecorded_context_rejected_before_draw(self):
        with patch.object(sys, 'argv', ['draw_d1', '--repo', str(self.repo), '--draw-context-commit', 'HEAD']), \
             patch.object(d1, 'draw_index') as draw:
            with self.assertRaisesRegex(SystemExit, 'Replay limitato'):
                d1.main()
            draw.assert_not_called()

    def test_original_draw_log_cannot_be_overwritten(self):
        log = HERE / 'D1_DRAW_LOG.json'
        original = log.read_bytes()
        with patch.object(sys, 'argv', ['draw_d1', '--repo', str(self.repo), '--out', str(log)]), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(SystemExit, 'log originale si conserva'):
                d1.main()
        self.assertEqual(log.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
