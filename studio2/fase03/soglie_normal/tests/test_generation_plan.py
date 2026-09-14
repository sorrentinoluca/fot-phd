import csv, importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("plan", HERE/"build_generation_plan.py")
plan=importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

def test_counts_streams_and_disjointness():
    cal=plan.build_rows("cal_thr"); far=plan.build_rows("far_ver")
    plan.validate_rows(cal,"cal_thr"); plan.validate_rows(far,"far_ver")
    assert len(cal)==350 and len(far)==150
    assert {r["stream_id"] for r in cal}.isdisjoint({r["stream_id"] for r in far})
    assert all(1 <= r["J"] <= 10 for r in cal)
    assert all(r["stop_time_h"] == 20+5*r["J"] for r in cal)
    assert all(r["stop_time_h"] == 70 for r in far)

def test_seed_draws_are_reproducible_and_positions_uniform_domain():
    a=plan.build_rows("far_ver"); b=plan.build_rows("far_ver")
    assert a==b
    assert {r["window_position"] for r in a} <= set(range(1,11))
