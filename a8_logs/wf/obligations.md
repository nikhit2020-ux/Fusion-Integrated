# WF obligations → test cases

Source: specs_rspc/a8_plain/05_RSPC_Workflow_Specifications_v2.1_SYNCHRONIZED.txt (state-transition tables are authoritative).
Adequacy rule (Section 7, WF): every explicitly specified distinct workflow path/decision outcome; every important stated transition at least once.

Obligations counted:
- (a) each Basis workflow BW-RSPC-01..12 = one distinct end-to-end path (12);
- (b) each row (transition / decision outcome) of each Composite workflow CW-RSPC-01..06 (10+11+9+8+8+8 = 54). CW-RSPC-02 row 6 has two
  stated from-states ("Consultancy Submitted / Department Recommended") and is counted as two transitions → 55.
Basis-table rows are identical to the success rows of their composite, so they are covered through (a) and (b) and not counted again.

## (a) Basis paths

| Obligation | Test(s) | Covered |
|---|---|---|
| BW-RSPC-01 Research proposal approved at Dean-RSPC | WF-001 | yes |
| BW-RSPC-02 Research proposal approved via Director | WF-002 | yes |
| BW-RSPC-03 Consultancy approved at Dean-RSPC | WF-007 | yes |
| BW-RSPC-04 Consultancy approved via Director | WF-008 | yes |
| BW-RSPC-05 Staff appointment approved at Dean-RSPC | WF-015 | yes |
| BW-RSPC-06 Staff appointment approved via Director | WF-016 | yes |
| BW-RSPC-07 Financial request approved at Dean-RSPC | WF-020 | yes |
| BW-RSPC-08 Financial request approved via Director | WF-021 | yes |
| BW-RSPC-09 Procurement approved at Dean-RSPC | WF-025 | yes |
| BW-RSPC-10 Procurement approved via Director | WF-026 | yes |
| BW-RSPC-11 Closure approved and archived at Dean-RSPC | WF-030 | yes |
| BW-RSPC-12 Closure approved and archived via Director | WF-031 | yes |

## (b) Composite transitions / decision outcomes

| Obligation | Transition | Test(s) | Covered |
|---|---|---|---|
| CW-RSPC-01 r1 | Proposal Draft → Proposal Submitted | WF-001, WF-002 (setup in WF-003..006) | yes |
| CW-RSPC-01 r2 | Proposal Submitted → Department Recommended | WF-001, WF-002 | yes |
| CW-RSPC-01 r3 | Proposal Submitted → Department Not Recommended | WF-003 | yes |
| CW-RSPC-01 r4 | Department Recommended → Admin Verified | WF-001, WF-002 | yes |
| CW-RSPC-01 r5 | Department Recommended → Not Eligible for Forwarding | WF-004 | yes |
| CW-RSPC-01 r6 | Admin Verified → Approved (Dean) | WF-001 | yes |
| CW-RSPC-01 r7 | Admin Verified → Forwarded to Director | WF-002 | yes |
| CW-RSPC-01 r8 | Admin Verified → Dean Not Approved | WF-005 | yes |
| CW-RSPC-01 r9 | Forwarded to Director → Approved | WF-002 | yes |
| CW-RSPC-01 r10 | Forwarded to Director → Director Not Approved | WF-006 | yes |
| CW-RSPC-02 r1 | Consultancy Draft → Consultancy Submitted | WF-007, WF-008, WF-010 | yes |
| CW-RSPC-02 r2 | Consultancy Submitted → Department Recommended | WF-007, WF-008 | yes |
| CW-RSPC-02 r3 | Consultancy Submitted → Department Not Recommended | WF-009 | yes |
| CW-RSPC-02 r4 | Consultancy Submitted → Admin Verified (dept stage not applicable) | WF-010 | yes |
| CW-RSPC-02 r5 | Department Recommended → Admin Verified | WF-007, WF-008 | yes |
| CW-RSPC-02 r6a | Consultancy Submitted → Not Eligible for Forwarding | WF-011 | yes |
| CW-RSPC-02 r6b | Department Recommended → Not Eligible for Forwarding | WF-012 | yes |
| CW-RSPC-02 r7 | Admin Verified → Approved (Dean) | WF-007, WF-010 | yes |
| CW-RSPC-02 r8 | Admin Verified → Forwarded to Director | WF-008 | yes |
| CW-RSPC-02 r9 | Admin Verified → Dean Not Approved | WF-013 | yes |
| CW-RSPC-02 r10 | Forwarded to Director → Approved | WF-008 | yes |
| CW-RSPC-02 r11 | Forwarded to Director → Director Not Approved | WF-014 | yes |
| CW-RSPC-03 r1 | Appointment Draft → Appointment Requested | WF-015, WF-016 | yes |
| CW-RSPC-03 r2 | Appointment Requested → Admin Verified | WF-015, WF-016 | yes |
| CW-RSPC-03 r3 | Appointment Requested → Not Eligible for Forwarding | WF-017 | yes |
| CW-RSPC-03 r4 | Admin Verified → Selection Recommendation Recorded | WF-015, WF-016 | yes |
| CW-RSPC-03 r5 | Selection Recommendation Recorded → Approved (Dean) | WF-015 | yes |
| CW-RSPC-03 r6 | Selection Recommendation Recorded → Forwarded to Director | WF-016 | yes |
| CW-RSPC-03 r7 | Selection Recommendation Recorded → Dean Not Approved | WF-018 | yes |
| CW-RSPC-03 r8 | Forwarded to Director → Approved | WF-016 | yes |
| CW-RSPC-03 r9 | Forwarded to Director → Director Not Approved | WF-019 | yes |
| CW-RSPC-04 r1 | Financial Request Draft → Submitted | WF-020, WF-021 | yes |
| CW-RSPC-04 r2 | Submitted → Verified | WF-020, WF-021 | yes |
| CW-RSPC-04 r3 | Submitted → Not Eligible for Forwarding | WF-022 | yes |
| CW-RSPC-04 r4 | Verified → Approved (within delegated powers) | WF-020 | yes |
| CW-RSPC-04 r5 | Verified → Forwarded to Director (high-value) | WF-021 | yes |
| CW-RSPC-04 r6 | Verified → Dean Not Approved | WF-023 | yes |
| CW-RSPC-04 r7 | Forwarded to Director → Approved | WF-021 | yes |
| CW-RSPC-04 r8 | Forwarded to Director → Director Not Approved | WF-024 | yes |
| CW-RSPC-05 r1 | Procurement Request Draft → Submitted | WF-025, WF-026 | yes |
| CW-RSPC-05 r2 | Submitted → Verified (budget validation passes) | WF-025, WF-026 | yes |
| CW-RSPC-05 r3 | Submitted → Not Eligible for Forwarding (verification/budget fails) | WF-027 | yes |
| CW-RSPC-05 r4 | Verified → Approved (Dean) | WF-025 | yes |
| CW-RSPC-05 r5 | Verified → Forwarded to Director | WF-026 | yes |
| CW-RSPC-05 r6 | Verified → Dean Not Approved | WF-028 | yes |
| CW-RSPC-05 r7 | Forwarded to Director → Approved | WF-026 | yes |
| CW-RSPC-05 r8 | Forwarded to Director → Director Not Approved | WF-029 | yes |
| CW-RSPC-06 r1 | Closure Draft → Closure Submitted | WF-030, WF-031 | yes |
| CW-RSPC-06 r2 | Closure Submitted → Closure Verified | WF-030, WF-031 | yes |
| CW-RSPC-06 r3 | Closure Submitted → Not Eligible for Forwarding | WF-032 | yes |
| CW-RSPC-06 r4 | Closure Verified → Archived (Dean; project completed) | WF-030 | yes |
| CW-RSPC-06 r5 | Closure Verified → Forwarded to Director | WF-031 | yes |
| CW-RSPC-06 r6 | Closure Verified → Dean Not Approved | WF-033 | yes |
| CW-RSPC-06 r7 | Forwarded to Director → Archived (project completed) | WF-031 | yes |
| CW-RSPC-06 r8 | Forwarded to Director → Director Not Approved | WF-034 | yes |

## Totals
- Basis paths: 12 / 12 covered.
- Composite transitions/outcomes: 55 / 55 covered.
- **Total: 67 / 67 obligations covered** by 34 test cases. No missing obligations → no completion pass needed; the design is frozen as produced in Step A.

## Not counted as obligations (with reason)
- Legacy RSPC-WF-006 (progress/utilization reporting), RSPC-WF-008 (role administration), RSPC-WF-009 (notification delivery):
  explicitly **Retired** in the spec's Legacy Workflow Disposition; not workflows to test under WF.
- Legacy RSPC-WF-001..005, 007: replaced by the CW/BW workflows above (already covered).
- Failure of the submission guard (e.g. mandatory fields missing at row 1) is not a stated workflow outcome/resulting state in any
  table, so it isn't an obligation (testing it would add a combination the spec doesn't support).
