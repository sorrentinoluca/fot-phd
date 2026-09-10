# C02b shared numerical prototypes

This directory contains the frozen, same-task comparison requested by C02b.
The method name is **baseline numerica con prototipi condivisi, ispirata a
FedProto**; it is intentionally not presented as the original FedProto
algorithm.

Run from the repository root:

```bash
python phase_b/baselines/c02b_shared_numeric_prototypes/run_baseline.py
python -m unittest phase_b.baselines.c02b_shared_numeric_prototypes.tests.test_baseline -v
```

The executable verifies the protocol freeze and every frozen classifier input,
creates predictions before loading held-out truth, and refuses to overwrite a
different deterministic output. The main result and limitations are in
[`results/C02B_BASELINE_REPORT.md`](results/C02B_BASELINE_REPORT.md).
