import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('p',HERE/'build_generation_plan.py')
p=importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
cal=p.build_rows('cal_thr'); far=p.build_rows('far_ver')
assert len(cal)==350 and len(far)==150
assert len({r['stream_id'] for r in cal+far})==500
assert all(1<=r['J']<=10 for r in cal)
assert all(r['stop_time_h']==20+5*r['J'] for r in cal)
assert all(r['stop_time_h']==70 for r in far)
assert all(r['window_position']==r['J'] for r in cal)
assert cal==p.build_rows('cal_thr') and far==p.build_rows('far_ver')
print('PASS standard-library plan tests')
