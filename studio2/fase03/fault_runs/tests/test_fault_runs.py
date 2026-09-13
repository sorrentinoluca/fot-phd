import copy
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import build_generation_plan as plan
import fault_protocol as protocol
import prepare_simulator as simulator


class Plans(unittest.TestCase):
    def test_exact_catalog_batch_indices(self):
        rows = plan.validate_plan(HERE/'plans/fault_dev.csv')
        self.assertEqual(len(rows), 40)
        self.assertEqual([int(r['stream_id']) for r in rows], list(range(30000,30040)))
        self.assertEqual({int(r['idv']) for r in rows}, set(plan.CATALOG))
        for f in plan.CATALOG:
            self.assertEqual([int(r['batch']) for r in rows if int(r['idv'])==f],list(range(1,6)))
        self.assertTrue(all(float(r['onset_h'])==25 and float(r['stop_time_h'])==65 for r in rows))

    def test_disjoint_all_phase02_manifests_and_reservations(self):
        new = {int(r['stream_id']) for k in ('fault_dev','smoke') for r in plan.build_rows(k)}
        self.assertEqual(len(new),41)
        self.assertFalse(new & plan.occupied_indices())

    def test_collision_blocks_generation(self):
        with patch.object(plan,'occupied_indices',return_value={30000}):
            with self.assertRaises(ValueError):plan.build_rows('fault_dev')

    def test_reordered_edited_duplicate_incomplete_plan_rejected(self):
        original=(HERE/'plans/fault_dev.csv').read_text().splitlines()
        for lines in (original[:1]+original[2:]+original[1:2], original[:-1],
                      original[:2]+original[1:2]+original[3:],
                      [s.replace(',25,40,65,',',20,40,60,') for s in original]):
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'plan.csv';p.write_text('\n'.join(lines)+'\n')
                with self.assertRaises(ValueError):plan.validate_plan(p)

    def test_smoke_separate_and_reduced_only_post_horizon(self):
        rows=plan.validate_plan(HERE/'plans/smoke.csv')
        self.assertEqual(len(rows),1)
        r=rows[0]
        self.assertEqual((r['idv'],r['stream_id'],r['onset_h'],r['burn_in_h']),('1','30040','25','20'))
        self.assertEqual(r['horizon_h'],'0.1')
        self.assertEqual(r['useful_windows_expected'],'0')

    def test_seed_words_reconstruct_uint64(self):
        for r in plan.build_rows('fault_dev'):
            self.assertEqual((r['stream_hi32']<<32)|r['stream_lo32'],int(r['stream_id']))
            self.assertEqual(r['seed_descriptor'],f"{plan.KEY}:{int(r['stream_id']):016x}")

    def test_destination_guard_and_existing_directory(self):
        with self.assertRaises(ValueError):protocol.preflight(HERE/'plans/fault_dev.csv','/tmp/fault')
        with tempfile.TemporaryDirectory(dir=HERE) as d:
            with self.assertRaises(ValueError):protocol.preflight(HERE/'plans/smoke.csv',d)


class Instrumentation(unittest.TestCase):
    def test_only_marked_diagnostics_added_to_qualified_source(self):
        original=simulator.BASE.read_bytes()
        changed=simulator.instrument(original)
        self.assertEqual(simulator.strip_instrumentation(changed),original)
        for marker in (b'FOT_IDV',b'FOT_DIAG',b'FOT_TRIP'):
            self.assertIn(marker,changed)

    def test_unknown_base_source_is_rejected(self):
        with self.assertRaises(ValueError):simulator.instrument(simulator.BASE.read_bytes()+b'\n')


class Logs(unittest.TestCase):
    def line(self,t=25,mask=1):
        return 'FOT_DIAG,'+','.join(map(str,[t,mask]+[0]*13))

    def test_parser_extracts_trip_and_onset(self):
        text=self.line(0,0)+'\nFOT_IDV,25,1\n'+self.line()+'\nFOT_TRIP,25.1,4\nwarning'
        diag,tr,trip=protocol.parse_simulation_log(text)
        self.assertEqual(tr,[[25,1]])
        self.assertEqual(trip,[[25.1,4]])
        self.assertEqual(len(diag),2)
        self.assertEqual(protocol.check_idv(diag,tr,25,1,25.1),(True,25))

    def test_malformed_instrumentation_not_silently_ignored(self):
        for text in ('FOT_IDV,25','FOT_TRIP,25,0','FOT_IDV,nan,1','FOT_OTHER,25,1',
                     self.line(25)+'\n'+self.line(24),self.line(25,2**28)):
            with self.assertRaises(ValueError):protocol.parse_simulation_log(text)

    def test_wrong_early_extra_or_missing_idv_rejected(self):
        for diag,transition in (([[24,1]],[[24,1]]),([[25,3]],[[25,3]]),
                                ([[25,1]],[]),([[25,1]],[[25,1],[26,0]])):
            with self.assertRaises(ValueError):protocol.check_idv(diag,transition,25,1,65)
        self.assertEqual(protocol.check_idv([[20,0]],[],25,1,20),(False,None))

    def test_event_log_sequence_and_timestamps(self):
        events=[{'timestamp_utc':f'2026-09-13T10:00:0{i}Z','event':e,'run_id':'r'}
                for i,e in enumerate(('campaign_start','run_start','run_end','campaign_end'))]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'events.jsonl'
            p.write_text('\n'.join(map(json.dumps,events)))
            self.assertEqual(len(protocol.parse_event_log(p)),4)
            p.write_text('\n'.join(map(json.dumps,events[:-1])))
            with self.assertRaises(ValueError):protocol.parse_event_log(p)
            events[2]['run_id']='other'
            p.write_text('\n'.join(map(json.dumps,events)))
            with self.assertRaises(ValueError):protocol.parse_event_log(p)


class Manifests(unittest.TestCase):
    def fixture(self,d,trip=False):
        row=plan.build_rows('smoke')[0]
        directory=Path(d);rid=row['run_id']
        end=25.05 if trip else 25.1
        with (directory/(rid+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(protocol.RAW_FIELDS)
            for i in range(round(end*60)+1):w.writerow([i/60]+[0]*53)
        lines=[]
        for i in range(round(end*60)+1):
            t=i/60;mask=0 if t<25 else 1
            if i==1500:lines.append('FOT_IDV,25,1')
            lines.append('FOT_DIAG,'+','.join(map(str,[t,mask]+[0]*13)))
        if trip:lines.append('FOT_TRIP,25.055,4')
        (directory/(rid+'.simulation.log')).write_text('\n'.join(lines))
        meta={k:'a'*64 for k in ('mex_sha256','model_sha256','script_sha256','source_sha256',
              'base_source_sha256','plan_sha256','spec_sha256')}
        meta.update(plan_row=row,counter_end='1234',started_at_utc=protocol.utcnow(),
                    simulation_seconds=0.01,platform={'architecture':'fixture'},matlab_version='fixture',
                    dependency_hashes=[],model_overrides={},git_commit='a'*40,technical_error='')
        p=directory/(rid+'.attempt.json');p.write_text(json.dumps(meta));return p

    def test_complete_manifest_fields_window_exclusion_and_immutability(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fixture(d);r=protocol.finalize(p)
            self.assertTrue(protocol.REQUIRED<=r.keys())
            self.assertEqual(r['status'],'complete')
            self.assertFalse(r['pre_fault_window']['development_eligible'])
            self.assertTrue(r['pre_fault_window']['complete'])
            self.assertEqual(r['post_fault_windows'],[])
            with self.assertRaises(FileExistsError):protocol.finalize(p)

    def test_trip_prefix_preserved_without_replacement(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fixture(d,trip=True);r=protocol.finalize(p)
            self.assertEqual(r['status'],'physical_trip')
            self.assertEqual(r['trip_time_h'],25.055)
            self.assertIsNotNone(r['sha256'])
            self.assertEqual(r['stream_id'],'30040')

    def test_early_stop_without_trip_is_technical_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fixture(d,trip=True)
            log=Path(d)/'smoke-F1-001.simulation.log'
            log.write_text(log.read_text().replace('FOT_TRIP,25.055,4',''))
            r=protocol.finalize(p)
            self.assertEqual(r['status'],'technical_failure')
            self.assertIsNone(r['output_path'])
            self.assertTrue(Path(r['quarantined_output_path']).exists())

    def test_missing_fields_or_modified_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            r=protocol.finalize(self.fixture(d))
            for field in protocol.REQUIRED:
                copy_r=copy.deepcopy(r);del copy_r[field]
                with self.assertRaises(ValueError):protocol.validate_manifest(copy_r)
            Path(r['output_path']).write_text('changed')
            with self.assertRaises(ValueError):protocol.validate_manifest(r,verify_files=True)

    def test_changed_manifest_invariants_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            r=protocol.finalize(self.fixture(d))
            for k,v in (('onset_h',20),('horizon_h',50),('ts_base_h',0.001),('msflag',32),
                        ('stream_id','999999'),('useful_windows_complete',1)):
                changed=copy.deepcopy(r);changed[k]=v
                with self.assertRaises(ValueError):protocol.validate_manifest(changed)

    def test_missing_counter_records_technical_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fixture(d);meta=json.loads(p.read_text());meta['counter_end']=[]
            p.write_text(json.dumps(meta))
            r=protocol.finalize(p)
            self.assertEqual(r['status'],'technical_failure')
            self.assertIsNone(r['counter_end'])

    def test_failure_marks_remaining_reserved_runs_not_run(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.fixture(d);meta=json.loads(p.read_text())
            meta['plan_row']=plan.build_rows('fault_dev')[0]
            meta['technical_error']='synthetic failure before output'
            rid=meta['plan_row']['run_id']
            (Path(d)/(rid+'.simulation.log')).write_text('synthetic technical failure')
            p.write_text(json.dumps(meta));protocol.finalize(p)
            records=protocol.finish_campaign(HERE/'plans/fault_dev.csv',d)
            self.assertEqual(len(records),40)
            self.assertEqual(records[0]['status'],'technical_failure')
            self.assertTrue(all(r['status']=='not_run' for r in records[1:]))
            self.assertTrue(all(r['started_at_utc'] is None for r in records[1:]))
            for r in records:protocol.validate_manifest(r,verify_files=True)

    def test_trip_window_completeness(self):
        row=plan.build_rows('fault_dev')[0]
        pre,post=protocol.windows(row,37)
        self.assertTrue(pre['complete'])
        self.assertEqual(sum(w['complete'] for w in post),2)
        self.assertEqual(len(post),8)

if __name__=='__main__':unittest.main()
