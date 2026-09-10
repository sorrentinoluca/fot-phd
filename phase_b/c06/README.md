# C06 diagnostic experiment

This directory isolates the post-hoc `B_LOCAL_FIRST_V1` screening from every
EXP3_V2 frozen artifact. It never modifies a frozen tag, source prompt, result,
or evaluator.

Build deterministic pre-inference assets:

```bash
../fot-c06-env/bin/python -m phase_b.c06.build_screening_assets
```

Run the tests, then freeze every C06 input before inference:

```bash
../fot-c06-env/bin/python -m unittest phase_b.c06.tests.test_c06_screening
../fot-c06-env/bin/python -m phase_b.c06.freeze_inputs
```

Run the fail-closed preflight:

```bash
../fot-c06-env/bin/python -m phase_b.c06.run_screening --preflight
```

Execute exactly the 72 scheduled screening calls:

```bash
../fot-c06-env/bin/python -m phase_b.c06.run_screening --execute-screening
```

Evaluate only after all 72 repetition records exist:

```bash
../fot-c06-env/bin/python -m phase_b.c06.evaluate_screening
```

The runner reads `OPENAI_API_KEY` only from the process environment. Ground
truth and the list of original failures live under `evaluator_side/`, which is
not imported by the prompt builder or inference runner.
