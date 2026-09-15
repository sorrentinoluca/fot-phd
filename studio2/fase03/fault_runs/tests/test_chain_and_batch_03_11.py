import sys
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import build_generation_plan as plan
import fault_protocol


class ChainAndBatchTests(unittest.TestCase):
    def test_chain_identifiers_and_streams_are_fixed(self):
        f5 = plan.build_rows('ood_chain_f5')
        f12 = plan.build_rows('ood_chain_f12')
        self.assertEqual([(r['run_id'], r['idv'], r['stream_id']) for r in f5],
                         [('chain-F5-001', 5, '70002')])
        self.assertEqual([(r['run_id'], r['idv'], r['stream_id']) for r in f12],
                         [('chain-F12-001', 12, '70003')])

    def test_each_batch_has_frozen_89_row_composition(self):
        for candidate, base in ((5, 71000), (12, 72000)):
            rows = plan.build_rows(f'test_batch_f{candidate}')
            self.assertEqual(len(rows), 89)
            self.assertEqual([int(r['stream_id']) for r in rows], list(range(base, base+89)))
            primary = [r for r in rows if r['run_id'].startswith('test-primary-F')]
            normal = [r for r in rows if r['run_id'].startswith('test-primary-Normal')]
            ood = [r for r in rows if r['run_id'].startswith('test-ood-')]
            spares = [r for r in rows if r['run_id'].startswith('test-spare-')]
            self.assertEqual(Counter(r['idv'] for r in primary), Counter({x: 8 for x in plan.CATALOG}))
            self.assertEqual((len(normal), len(ood), len(spares)), (8, 6, 11))
            self.assertEqual(Counter(r['idv'] for r in ood), Counter({candidate: 3, 4: 3}))
            self.assertTrue(all(r['stop_time_h'] == 65 and r['useful_windows_expected'] == 8 for r in rows))

    def test_all_new_streams_are_pairwise_disjoint(self):
        kinds = ('ood_chain_f5','ood_chain_f12','test_batch_f5','test_batch_f12')
        sets = [{int(r['stream_id']) for r in plan.build_rows(k)} for k in kinds]
        for i, left in enumerate(sets):
            self.assertFalse(left & plan.occupied_indices())
            for right in sets[i+1:]:
                self.assertFalse(left & right)

    def test_normal_idv_trace_requires_no_activation(self):
        diag = [[0.0, 0], [25.0, 0], [65.0, 0]]
        self.assertEqual(fault_protocol.check_idv(diag, [], 25, 0, 65), (False, None))
        with self.assertRaisesRegex(ValueError, 'Normal run contains'):
            fault_protocol.check_idv([[0.0, 0], [25.0, 1]], [[25.0, 1]], 25, 0, 65)


if __name__ == '__main__':
    unittest.main()
