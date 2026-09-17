import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import build_generation_plan as plan


class OODPreflightPlanTests(unittest.TestCase):
    def test_exact_frozen_order_and_streams(self):
        rows = plan.build_rows('ood_preflight')
        self.assertEqual([r['run_id'] for r in rows], ['preflight-F6-001', 'preflight-F4-001'])
        self.assertEqual([r['idv'] for r in rows], [6, 4])
        self.assertEqual([int(r['stream_id']) for r in rows], [70000, 70001])
        self.assertTrue(all(r['onset_h'] == 25 and r['stop_time_h'] == 65 for r in rows))
        self.assertTrue(all(r['useful_windows_expected'] == 8 for r in rows))

    def test_streams_are_disjoint_from_known_allocations(self):
        streams = {int(r['stream_id']) for r in plan.build_rows('ood_preflight')}
        self.assertFalse(streams & plan.occupied_indices())
        self.assertFalse(streams & set(range(30000, 30041)))
        self.assertFalse(streams & set(range(40000, 40350)))
        self.assertFalse(streams & set(range(49900, 50150)))
        self.assertFalse(streams & set(range(60000, 60040)))


if __name__ == '__main__':
    unittest.main()
