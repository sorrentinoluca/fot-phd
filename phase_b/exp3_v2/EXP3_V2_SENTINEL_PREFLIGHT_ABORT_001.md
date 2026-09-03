# Experiment 3 V2 sentinel preflight abort 001

Status: **ABORTED BEFORE SENTINEL** on 2026-09-03.

The clean worktree at `exp3-v2-harness-frozen` resolved to commit
`c96519f46291fcf7da5fc64f1d71cd2934816600`, but manifest validation stopped
because the tagged Git tree did not materialize the live ignored EXP3 log or
four simulator files listed as Git-boundary artifacts.

- Simulation calls: 0
- Sentinel executions: 0
- Sentinel seed consumed: false
- Workbooks created: 0
- Retry performed: false
- Diagnostic signal inspected: false
- Real-path interference: false

Revision 002 separates committed Git-boundary artifacts from explicitly
materialized and hash-verified external runtime dependencies. The original tag
is retained unchanged and may not be used for another sentinel attempt.
