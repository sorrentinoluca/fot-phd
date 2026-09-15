# FoT-TEP — demonstrated failures and retained corrections

Historical record: 15 September 2026. These are bounded lessons from the offline harness,
not instructions to freeze, deploy, alter scientific decisions or start another review.

## Failure → cause → prevention

| Finding | Demonstrated omission | Reusable prevention and regression |
| --- | --- | --- |
| C01/R04 and D01 | A probe or replay could trust an unresolved/invalid alternate or historical gate closure. | Reconfirm the entire prerequisite chain on reuse, including historical outcomes. Exercise ordinary runner/CLI and valid legacy fixtures. |
| C02 / N48 | Timeout stopped the gate rather than contributing an invalid first attempt to T3/T6. | Preserve the planned denominator and distinguish transport invalidity from a response. Test one, scattered and all timeouts, then replay without sending again. |
| C03 | Producer summary counted eight logical outputs after nine provider attempts. | Derive request counts from durable attempts; keep requests, evaluable pairs and insight counts separate. |
| D02 | Reconfirmation accepted predecessor records with corrupt raw data or incomplete coverage. | Recompute raw/record bindings and validate identity, order and complete coverage at the required stage boundary; counts alone do not establish authenticity. |
| D03 | Acquisition validated zero-token content/approval, but replay had a partial list. Stored hashes remained mutually equal after payload alteration. | One semantic proof+approval validator across acquisition, retry ancestry and gate; recalculable content digests with a durable link; no automatic legacy backfill. Test types (including bool vs int), required fields, nested content and valid-looking alterations. |
| D04 | quota_kind was checked in closure, but consumed unvalidated when reserving in an open stage. One changed SQL field allowed an eighth retry without waiver. | Validate every contributor to the cumulative reserve before binding and reservation, reusing the full structural attempt contract in the transaction. Include other open stages, direct execution without rebind, restart and the last-slot race. |
| D04 intermediate diagnostics | Earlier inventory checks displaced the hard-stop and alternate-prerequisite messages expected by historical tests. | Preserve safe early-refusal precedence while requiring full validation before authorization. Keep the tests and failed intermediate logs; rerun final suites. |

The repeated mechanism was broader than a missing condition: shared invariants were split
between paths, and tests covered a field in one lifecycle position rather than all relevant
consuming decisions. The small D04 fix succeeded by reusing existing validation at the right
boundaries, not by accumulating another independent checklist.

## Proven examples worth reusing when relevant

- D03: `test_d03_contract.py`, immutable field inventory and W01–W04. Semantic mutations
  with locally aligned hashes show that mere digest checks cannot replace content validation.
- D04: `test_d04_open_quota.py` and D04_DECISION_CONTRACT.json. Same final test bytes gave
  eight methods / 240 failed assertions in six methods on 23859a2, and 8/8 on aae29a9.
  The matrix has 216 quota cases, 72 positive controls and 14 role-dependency cases.
- Codex's U01: six decision entries (new/resumed binding, base, retry, remediation, triplet),
  a real writer blocked during validation and released afterward.
- U02: failure after the second insertion of a triplet; complete rollback, reopen and valid retry.
- U03: two processes in different stages compete for the fifteenth transport after waiver;
  exactly one succeeds. The limit is a historical FoT-TEP contract, not a universal quota.
- U04: an unknown stage, missing parent or missing proof in another open stage must be detected,
  including after an earlier success on the same instance and after restart.
- U05: execute_request without a prior rebind must reject in reservation before transport/journal;
  replacing snapshot with a failing stub proves that authorization does not depend on that diagnostic.

No need to repeat all these tests for an unrelated document change. Select by the affected
invariant and active mandate; do not use selection to silently omit an explicitly required suite.

## Latest independently reviewed state (historical, exact bytes)

- Technical candidate: `aae29a908356e4a4842a214fdc3db9bff26ec3ca`.
- Tree: `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`.
- Documentary successor: `feaf1d3c56ff142e1d1b4bc4dd243348c20bcb98`.
- Source: `/Users/luker/fot-tep-harness-0310-d04`.
- Contract/test-first: `bf7774f2d153ecc50f27ba095f77b612933b4d26`.
- Runtime delta: ledger.py +18/−3; earlier tests D01/D02/D03 unchanged.

[Codex verbatim review](review-codex-d04.md): OK limited to the exact offline candidate;
128/128 targeted, 163/163 discovery, historical reproductions and U01–U05 5/5 reported
executed. R01–R10 and later findings closed within the checked cases. Guardian remains
NON PASS, 14 historical failures and one skip. The learning task read this report and
verified its supplied SHA-256; it did not rerun the suites or reverify every evidence member.

[Claude verbatim review](review-claude-d04.md): OK for the same candidate, with 128 targeted
methods collected, 127 passed and one blocked by an absolute legacy path. Dedicated
V/W/Y/Z/X launchers, the complete discovery and guardian were not rerun there. Its opening
wording about complete suites must be read together with these explicit limits. Its claim
that unchanged files cannot be affected is not a general inference to adopt: source identity
alone is insufficient without dependency analysis. Do not promote inspected/covered-in-other-
ways tests to independently executed PASS results.

The Codex report supplies the full observed run for its environment; Claude adds an
independent model-family perspective and additional probes with its stated limits. Do not
sum their counts or infer that either review certifies future changes. Model configuration
is not proof of the backend actually served.

At that review, executable reception of approved D9, actual label order approval, real
insights, service/tokenizer/identity/capacity qualifications, T5 and pilot remained separate.
No freeze or GO was authorized. Recheck the current record before a later task; this note
must not override subsequent author decisions.

## Source locations and integrity

Copies in this reference folder preserve the exact reviewed report bytes. Source paths,
measured SHA-256 and supplied expected hashes are in [provenance.json](provenance.json).
The original evidence directories remain the place to retrieve scripts, logs, matrices and
fixtures; those are not duplicated into this personal skill.

- Codex source: `/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/VERIFICA_D04.md`.
- Codex manifest: same directory, `SHA256SUMS`.
- Codex additional probes: same directory, `decision_edge_probes.py` and JSON/log.
- Claude source: `/Users/luker/fot-tep-harness-0310-d04-checks/VERIFICA_D04.md`.
- Prior corrections and provenance: `/Users/luker/fot-tep-harness-0310-d04/studio2/fase03/harness/`.
