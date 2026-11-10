# BR — failure examination (Step F)

Run: `a8_results/br/pytest.log` — 66 collected, 33 passed, **1 failed**, 32 skipped, 0 errors.

## BR-040 — `test_BR_040_submission_and_decision_logged`

- **source_id:** BR-RSPC-050 (Maintain RSPC Audit and Compliance Logs)
- **Error summary:** `AssertionError: no submission entry in audit log`. After Faculty submits and HoD recommends,
  the proposal's history (`decisions` returned by `GET /api/v1/rspc/proposals/mine/`) contains only the HoD entry
  (`stage HoD, actor_id 2001, outcome recommended, decided_at …`). There is no entry for the submission event.

### Four checks
1. **Is the expected behaviour directly supported by the cited spec? Yes.** BR-RSPC-050: "RSPC shall maintain logs
   needed for audit, transparency, and regulatory compliance for RSPC-managed records and events." It applies to
   "RSPC lifecycle events and records", is triggered when "An auditable RSPC event/record change occurs", and requires
   that "The relevant log/audit information is retained." The PS (3.9) adds: "RSPC maintains logs for audit,
   transparency, and regulatory compliance." Submitting a research proposal is an RSPC lifecycle event that creates an
   RSPC record (PS 3.1, BR-RSPC-012 "A Faculty proposal is submitted").
2. **Is the test correctly implemented and set up? Yes.** It drives the real API (submit as Faculty 1001, recommend as
   HoD 2001) and reads the only history/log interface RSPC exposes, which is the proposal's decision history. The HoD
   half of the assertion (actor, outcome, time) is satisfied, which shows that the setup and the log read work. Only
   the submission entry is missing. The IAM fake only identifies the callers; no RSPC behaviour is mocked.
   Caveat: the spec does not name the log's form. The proposal row stores `pi_id` and `created_at`, but RSPC exposes
   no log entry for the submission (with actor, action and time), and `created_at` is not returned by any endpoint.
3. **Is it reproducible? Yes.** I re-ran it alone twice (`pytest …::test_BR_040_submission_and_decision_logged`) and it
   failed both times with the same assertion.
4. **Does the observed behaviour contradict the expected? Yes.** Expected: a log entry for both the submission and
   the decision. Observed: a log entry for the decision only.

**Classification: Confirmed Implementation Defect.** It is the same underlying problem as the existing shared
defect **D-01** (proposal submission is not logged as a retrievable audit/log event), so BR is added to D-01 as an
exposing strategy instead of opening a new defect.

## Notes (not failures)
- 32 tests are `NOT_AUTOMATED` skips (there is no interface for consultancy, staff, finance, procurement, reporting,
  closure, integration, notifications or project updates; for BR-059 the precondition cannot be set up). They are
  not candidate failures.
- BR-059 (Dean-RSPC must not finalize outside its authority) concerns the same gap as shared candidate C-01. In BR
  it was not automated because no authority limit is represented, so BR did not raise C-01.

**Summary:** candidate failures 1; confirmed implementation defects 1 (D-01, shared with FR); new defects 0.
