# FR — failure examination (Step F)

Run: `a8_results/fr/pytest.log` / `junit.xml` — 111 tests: 32 passed, 2 failed, 0 errors, 77 skipped (NOT_AUTOMATED).
Re-runs (each failing test alone, twice): `a8_logs/fr/failure_reruns.log`.

## FR-009 — `test_fr_009_rspc_logs_submission_and_review_actions`

- **source_id:** RSPC-CFR-002; RSPC-FR-088
- **Error:** `AssertionError: no log entry for the submission action — assert 2001 in {3001}`. After a Faculty submission and an HoD decision, the proposal's retrievable record contains a log entry for the HoD decision only (actor 3001). There is none for the submission by Faculty 2001.
- **(1) Spec support — yes.** RSPC-FR-088: "RSPC shall maintain comprehensive logs for audit, transparency, and regulatory compliance." RSPC-CFR-002: "…operational records and logs needed for audit, transparency, compliance, and regulatory review of RSPC-managed information and events." Verification focus: "the specified RSPC record/log/history is persisted, retrievable by authorized users, and retains the required lifecycle/audit information." Proposal submission is an RSPC-managed event.
- **(2) Test correctly implemented and set up — yes.** The decision records nested in `GET proposals/mine/` are the only log RSPC exposes, and they are read as the authorized owner. Setup used the real API for both actions (201, then 200). The proposal model does store `created_at` and `pi_id`, but no RSPC API returns `created_at` and nothing records it as a log entry, so submission is not retrievable as a logged event.
- **(3) Reproducible — yes.** It failed the same way on both isolated runs (20:11:24 and 20:11:34 UTC).
- **(4) Observed contradicts expected — yes.** Only review decisions are logged. Submission, the first lifecycle event, is not.
- **Classification: Confirmed Implementation Defect.** RSPC does not log proposal submission as a retrievable audit/log event. Its only log covers review decisions.

## FR-023 — `test_fr_023_dean_cannot_finally_approve_beyond_limit`

- **source_id:** RSPC-CFR-004; RSPC-FR-126
- **Error:** `AssertionError: assert 'approved' != 'approved'`. Dean-RSPC gave final approval to a proposal with budget 99,999,999.99 (the largest value the field holds), and the status became `approved`.
- **(1) Spec support — no, not directly.** RSPC-FR-126: "RSPC shall allow Dean-RSPC to approve eligible RSPC requests within delegated or defined limits." The spec states that a limit exists but never gives its value or basis. Nor do the Problem Statement ("Approves eligible requests within delegated or defined limits") or CFR-004. That this proposal exceeds the Dean's limit is the test's assumption (documented in its docstring), not a value from the spec.
- **(2) Test correctly implemented and set up — yes.** The proposal was routed through HoD and RSPC Admin with the real API, and the Dean `decide` call was the one under test.
- **(3) Reproducible — yes.** It failed the same way on both isolated runs (20:11:40 and 20:11:46 UTC).
- **(4) Observed contradicts expected — yes**, as long as the budget is taken to be over the limit. The implementation applies no Dean approval limit of any size: `decide` approves any `admin_verified` proposal whatever its budget.
- **Classification: Specification ambiguity** (not a confirmed defect). The Dean's approval limit is required but undefined, so the over-limit expected result cannot be traced to a specified value. Observation for the report: the implementation has no Dean limit at all.
