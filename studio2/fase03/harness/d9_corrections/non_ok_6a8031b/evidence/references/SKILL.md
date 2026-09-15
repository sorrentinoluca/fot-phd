---
name: fot-tep-harness-lessons
description: Apply lessons from FoT-TEP harness reviews R01–R10 and C01–D04 when changing or reviewing its durable ledger, retry quotas, persisted evidence, gates, or resume paths. Also use when asked to retain lessons from these reviews. Does not authorize implementation during a read-only review or scientific execution.
---

# FoT-TEP — lessons from harness reviews

Use these lessons to prevent recurrence of demonstrated failures. The current user mandate,
repository contract and exact candidate remain authoritative; this skill is reusable process
memory, not a new source of scientific decisions or authorization.

For an implementation or review, read the relevant parts of
[lessons-and-evidence.md](references/lessons-and-evidence.md). For a request to learn or
summarize, retain the lessons without starting another correction, integration or test campaign.
Do not load the full review archives for an unrelated edit.

## Locate the decision before changing a validator

Map the affected normative value from acquisition to persistence, reload, validation and
its consuming decision. List the actual callers: direct ledger API, runner, CLI, first run,
resume, same-instance reuse and restart. Include open/partial stages and closed outcomes.

For quotas, identify **every contributor to the cumulative reserve**, including other stages.
For prerequisites, follow the historical dependency chain, not just the current stage.
Put required validation before the first protected side effect: client/server inquiry where
required by the contract, request reservation, transport, outcome or output materialization.
A rejection after a send is not a preventive rejection.

## Reuse the complete contract

Reuse the same semantic validation for acquisition and reconfirmation. Do not reconstruct
another partial list of checks. In this harness, zero-token proof and approval must be
validated consistently in acquisition, retry ancestors and the reconciled gate path.

Keep caller-specific admissibility separate from shared content/identity checks. A partial
stage may be structurally valid without satisfying the complete coverage and outcome required
for closure. Reusing a closing function that requires PASS is not a substitute for this split.

A field classified normative must be checked **where it influences a decision**. D04 showed
that validating quota_kind only at closure did not protect a new reservation in an open stage.
Diagnostic snapshots must not become authorization inputs without normative validation.

## Recompute durable evidence, preserve uncertain history

Check required content, types and bindings in addition to hash syntax and equality. Two stored
hash strings agreeing with each other do not authenticate a modified payload. Parse and hash
the same bytes read once; recompute content digests and validate their durable link on reuse.
Do not treat a freshly computed hash of received data as proof of its prior approval.

For this harness, historic zero-token evidence without the required digest/link fails closed.
Do not backfill a digest over potentially altered history; unblocking requires the separately
reviewed reconciliation specified by the active contract. Explain any approved compatibility
change and keep legitimate historical positives distinct from intentionally rejected legacy data.

## Turn the demonstrated defect into a discriminating test

Before the runtime fix, establish the contract/inventory and run the new test against the
exact rejected candidate. Use the same final test bytes against the corrected code. If the
test changes later, retain its initial version and rerun the final version on both candidates.
A test that passes on the rejected code has not demonstrated this regression.

Start from a valid fixture that reaches the intended boundary. Include a positive control;
check the reason and timing of refusal so an earlier missing prerequisite cannot create a false
green. Derive field mutations from the normative/forensic inventory, defaulting new named
fields to DA_COPRIRE. Add the relevant **role × stage/state × entry × operation** dimensions;
choose cases that exercise the changed decision rather than blindly multiplying every axis.
Do not equate a list of fields with coverage of all decisions using them.

Assert observable outcomes: no client/server call where required, zero new sends/intents,
logical DB unchanged relative to the injected-fault baseline, and unchanged raw/output artifacts.
Do not accept any HarnessError as success if the transport has already run. Keep provider
attempts distinct from logical outputs: nine requests may yield eight evaluable pairs.

## Protect the complete transaction

Keep validation of the read set and the decision/insertion in one transaction. For shared
quotas test contributors from other stages and concurrent requests for the last available slot,
not only two retries of the same parent. Use real processes/locks when those are at issue.
For atomic groups, inject failure after an intermediate insertion and verify total rollback,
restart behavior and the subsequent valid operation. Check a fresh fault after a prior success
on the same instance to detect caches that outlive their transaction.

Preserve legitimate early refusals and their established diagnostics: hard stops and invalid
prerequisites may reject before a more expensive inventory check. The complete inventory must
still be validated before every positive authorization. Fix ordering regressions in runtime;
do not weaken historical assertions just to recover green results.

## Verify and report at the scope actually established

Run the affected historical regressions and required complete suites on final runtime bytes.
Preserve original reviewer scripts; document genuine adaptations and retain obsolete literal
failures alongside their verified replacements. Distinguish test methods, subcases, assertions,
processes and overlapping suites. Read the result artifact: a launcher can exit zero with failures.

Report executed results separately from source inspection, environment-blocked tests and
proposed equivalence. Byte identity establishes a scope fact; excluding a test also requires
checking its dependencies. Different models can provide additional perspectives, but shared
contracts and independent behavioral tests are the primary protection against these failures.

Keep candidate commit/tree distinct from documentary successors; preserve source/review copies
and verify provenance. An OK applies to those bytes and the reviewed scope. In FoT-TEP the
historical documentary guardian NON PASS is a separate, nonblocking result for these deltas;
compare failure identifiers rather than relabeling it PASS. Do not carry numeric totals or
historical authorizations forward as current facts without checking the new task's scope.
