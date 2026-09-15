"""D9 discriminating probes. Offline fixture approvals are never scientific authorization."""
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from copy import deepcopy
from unittest.mock import patch

# Same test file can target exact prior bytes, without modifying that checkout.
if os.environ.get('FOT_D9_TARGET'):
    sys.path.insert(0, os.environ['FOT_D9_TARGET'])
from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text
from studio2.fase03.harness.guards import require_execution


class D9Contract(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)

    def approved(self, config):
        value=deepcopy(config); p=self.home/'approval.json'
        p.write_text(json.dumps({'author':'FIXTURE ONLY','decision':'accepted',
                                'configuration_sha256':sha256_text(canonical_json(value))}))
        value['execution_authorization']={'path':str(p),'sha256':sha256_text(p.read_text())}
        return value

    def test_legacy_nominal_approval_is_not_d9(self):
        config=self.approved({'study_model_decision':'APPROVED','status':'APPROVED_FOR_PHASE03_EXECUTION'})
        with self.assertRaisesRegex(HarnessError,'D9'):
            require_execution(config)

    def test_fixed_roles_and_pending_configuration(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        self.assertEqual(d9.ROLES,{'producer':'122B','consumer':'122B','alternate':'27B'})
        path=Path(d9.__file__).parents[1]/'config/pilot_d9_pending.json'
        config=json.loads(path.read_text())
        self.assertEqual(config['d9']['roles'],d9.ROLES)
        self.assertEqual(config['d9']['alternate_placement'],'PENDING')
        with self.assertRaises(HarnessError):require_execution(config)

    def test_payload_122b_omits_temperature_and_preserves_controls(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        generation={'max_tokens':100,'seed':None,'thinking_token_budget':None}
        self.assertEqual(d9.generation_kwargs(generation,model_role='122B'),{'max_tokens':100})
        self.assertEqual(d9.generation_kwargs(dict(generation,seed=17,thinking_token_budget=50),model_role='122B'),
                         {'max_tokens':100,'seed':17,'extra_body':{'thinking_token_budget':50}})
        for value in (None,0,0.6,''):
            with self.subTest(value=value),self.assertRaises(HarnessError):
                d9.generation_kwargs(dict(generation,temperature=value),model_role='122B')

    def test_role_stage_mapping_rejects_extra_arms(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        for stage in ('producer_conformity','producer_remediation','budget_probe','stability_gate'):
            self.assertEqual(d9.model_for_stage(stage),'122B')
        self.assertEqual(d9.model_for_stage('alternate_conformity'),'27B')
        for stage in ('terra','consumer_27b','fallback','swap_gate'):
            with self.subTest(stage=stage),self.assertRaises(HarnessError):d9.model_for_stage(stage)

if __name__=='__main__':unittest.main(verbosity=2)
