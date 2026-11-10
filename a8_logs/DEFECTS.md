# A8 — shared defect log (RSPC)

One row per underlying problem. "Exposed by" lists the strategies whose tests revealed it; later strategies add themselves to an existing row instead of adding a duplicate.

| Defect ID | Summary | Classification | Spec evidence | Exposed by (test_ids) |
|---|---|---|---|---|
| D-01 | Proposal submission is not logged as a retrievable audit/log event; only review decisions (HoD/Admin/Dean/Director) are logged. | Confirmed Implementation Defect | RSPC-FR-088; RSPC-CFR-002; BR-RSPC-050 | FR (FR-009); BR (BR-040) |
| D-02 | No draft save/revise for research proposals: create always records the proposal as `submitted` (status read-only, hard-coded in the view) and there is no update endpoint, so Faculty cannot save or revise a draft before submission. | Confirmed Implementation Defect | RSPC-UC-002 Alternative A1 | UC (UC-006) |

## Candidate failures not confirmed as defects

| Ref | Summary | Classification | Spec evidence | Raised by (test_ids) |
|---|---|---|---|---|
| C-01 | Dean-RSPC can finally approve a proposal of any budget; no Dean approval limit is applied. The spec requires approval "within delegated or defined limits" but defines no limit. | Specification ambiguity | RSPC-FR-126; RSPC-CFR-004 | FR (FR-023) |

## WF strategy (added in WF Step F)

WF (34 tests: 6 passed, 0 failed, 28 NOT_AUTOMATED) produced no failed or errored tests, so it exposed no new defect and does not add itself to D-01, D-02 or C-01.
The WF tests cover only the research-proposal state transitions (CW-RSPC-01). Those transitions do not exercise submission audit logging (D-01), draft save/revise (D-02) or a Dean approval limit (C-01).
