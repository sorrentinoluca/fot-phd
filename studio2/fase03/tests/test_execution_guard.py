from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import unittest

from studio2.fase03 import prepare_gate, producer_probe, run_pilot
from studio2.fase03.protocol import load_json


ROOT = Path(__file__).resolve().parents[3]


class ExecutionGuardTests(unittest.TestCase):
    def test_plan_only_reports_zero_execution_status(self):
        config = load_json(ROOT / "studio2/fase03/config/pilot_preflight.json")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run_pilot.print_plan(config)
        value = json.loads(output.getvalue())
        self.assertEqual(value["status"], "PLAN_ONLY_NO_PROVIDER_CALLS")
        self.assertEqual(value["stability_gate_calls"], 120)
        self.assertEqual(value["planned_total_with_retry_reserve"], 160)
        self.assertFalse(value["retry_reserve_authorized"])
        self.assertEqual(value["hard_stop_provider_requests"], 200)
        self.assertEqual(config["candidate"]["expected_max_model_len"], 16384)
        self.assertEqual(
            config["candidate"]["expected_process"]["environment"],
            {
                "CUDA_VISIBLE_DEVICES": "0",
                "VLLM_USE_FLASHINFER_SAMPLER": "0",
            },
        )
        self.assertFalse(config["candidate"]["gpu_kv_cache"]["comparison_key"])
        self.assertFalse(value["provisional_stress_probe"]["writes_gate_freeze"])
        self.assertTrue(value["provisional_stress_probe"]["real_prompt_repeat_required"])

    def test_inventory_is_blocked_and_has_no_calls(self):
        value = prepare_gate.inventory()
        self.assertEqual(value["status"], "GATE_ENVELOPE_FROZEN_EXECUTION_SUSPENDED")
        self.assertEqual(value["model_calls"], 0)
        self.assertTrue(value["next_command_requires_independently_frozen_study2_pilot_inputs"])
        self.assertTrue(value["provisional_cap_stress_never_authorizes_stability_gate"])

    def test_producer_probe_defaults_to_plan_only(self):
        config = load_json(ROOT / "studio2/fase03/config/pilot_preflight.json")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            producer_probe.print_plan(config)
        value = json.loads(output.getvalue())
        self.assertEqual(value["status"], "PLAN_ONLY_NO_PROVIDER_CALLS")
        self.assertEqual(value["calls_per_producer"], 8)
        self.assertEqual(value["global_insights_checked"], 16)


if __name__ == "__main__":
    unittest.main()
