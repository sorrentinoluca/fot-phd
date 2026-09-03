# Experiment 3 V2 pre-execution incidents — Revision 003 record

Revision 003 preserves Revision 002 (`261e54b10fe2c0a8897627ff7626c1a2d05672f8`,
tag `exp3-v2-harness-frozen-002`) unchanged and records three distinct
pre-execution technical aborts. None is a completed sentinel simulation.

1. Revision 001 clean-checkout preflight stopped on missing Git-boundary
   artifacts: zero RNG calls, zero simulations, zero workbooks.
2. The Revision 002 external preservation driver stopped on
   `EXP3V2:WrongModelPath` before RNG/simulation: zero RNG calls, zero
   simulations, zero workbooks.
3. The Revision 002 official frozen wrapper stopped at tagged
   `run_exp3v2_engine.m:120` with
   `MATLAB:string:MustBeStringScalarOrCharacterVector`, before RNG/simulation:
   zero RNG calls, zero simulations, zero workbooks.

The failing expression used square-bracket concatenation of two string scalars,
which MATLAB evaluates as a nonscalar 1×2 string array. `evalin` requires a char
vector or string scalar. The Revision 003 candidate changes only this text
construction and adds a no-simulation regression test.

The machine-readable companion records canonical paths, byte sizes, SHA-256
hashes, directory tree hashes, repository status, and every currently available
independent log. Four JSON artifacts are preserved as byte-identical versioned
archives. No reported evidence was unavailable at reconciliation time. All
temporary evidence remains in place and was not deleted or rewritten.

Aggregate state after all three aborts: sentinel simulations 0, RNG seed calls
0, simulation calls 0, sentinel seed `987654321` unconsumed, scientific seeds
consumed 0, workbooks created 0.
