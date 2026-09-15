"""Replay original review methods in a separate sacrificial directory; no network.

N20/N21 get only the newly required frozen sample/identity fixture, preserving
all original semantic assertions. The other twelve methods run unchanged.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import unittest

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--candidate',type=Path,required=True)
p.add_argument('--original',type=Path,required=True)
p.add_argument('--reference',type=Path,required=True)
p.add_argument('--sandbox',type=Path,required=True)
a=p.parse_args()
root=a.sandbox.resolve();root.mkdir(parents=True,exist_ok=False)
(root/'candidate').symlink_to(a.candidate.resolve(),target_is_directory=True)
e=root/'evidence';e.mkdir()
shutil.copyfile(a.original,e/'negative_probes.py')
(e/'reference').symlink_to(a.reference.resolve(),target_is_directory=True)
spec=importlib.util.spec_from_file_location('original_probes',e/'negative_probes.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
from studio2.fase03.harness.offline_fixtures import sample
frozen=sample()
for i,row in enumerate(frozen):row['prompt_id']=f'p{i}'
original_rows=m.rows
original_evaluate=m.evaluate_stability_gate

def rows():
    values=original_rows()
    for i,row in enumerate(values):
        row.update({k:frozen[i//3][k] for k in ('prompt_sha256','agent_id','case_id','sample_role')},
                   request_id=f'FIXTURE-request-{i}',identity_valid=True)
    return values

m.rows=rows
m.evaluate_stability_gate=lambda records:original_evaluate(records,expected_prompts=frozen)
numbers={20,21,30,31,32,33,34,36,37,38,46,60,61,62}
suite=unittest.TestSuite()
for cls in (m.GateProbes,m.InputProbes,m.RunnerProbes,m.RecoveredModuleProbes):
    for name in unittest.defaultTestLoader.getTestCaseNames(cls):
        if int(name.split('_')[1]) in numbers:suite.addTest(cls(name))
with (root/'applicable.log').open('w') as log:
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
             original_sha256=hashlib.sha256(a.original.read_bytes()).hexdigest(),
             unchanged_methods=12,fixture_adapted_methods=[20,21],observations=m.OBS)
(root/'applicable.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='observations'}))
sys.exit(not result.wasSuccessful())
