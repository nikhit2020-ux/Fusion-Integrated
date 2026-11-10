# UC obligations (Step B)

Source: `specs_rspc/a8_plain/03_RSPC_Use_Case_Specifications_v1.3_SYNCHRONIZED.txt` — 29 active UCs
(RSPC-UC-019/020 retired, no obligations). Section-7 rule: main success flow of every UC + every
explicitly specified alternative/exception flow. UCs whose Alternative Flows say "None specified"
contribute no alternative obligation.

Obligation totals: 29 main flows + 19 alternative flows + 58 exception flows = **106**.
**Covered: 106/106.** Design: 116 test cases (UC-001..UC-116).

Main flows whose step text names several explicit decision outcomes are covered by one test per
named outcome (UC-003 recommended / not recommended; UC-005, UC-023, UC-026 approve / forward to
Director / not approved; UC-006 approve / reject per postcondition; UC-024 approve / forward;
UC-028 approve+archive / forward). These 10 extra cases cite the same Main Flow obligation.

| Obligation | Test case(s) | Status |
|---|---|---|
| RSPC-UC-001 Main Flow | UC-001 | covered |
| RSPC-UC-001 Alternative A1 | UC-002 | covered |
| RSPC-UC-001 Exception E1 | UC-003 | covered |
| RSPC-UC-001 Exception E2 | UC-004 | covered |
| RSPC-UC-002 Main Flow | UC-005 | covered |
| RSPC-UC-002 Alternative A1 | UC-006 | covered |
| RSPC-UC-002 Alternative A2 | UC-007 | covered |
| RSPC-UC-002 Exception E1 | UC-008 | covered |
| RSPC-UC-002 Exception E2 | UC-009 | covered |
| RSPC-UC-003 Main Flow | UC-010, UC-011 | covered |
| RSPC-UC-003 Alternative A1 | UC-012 | covered |
| RSPC-UC-003 Exception E1 | UC-013 | covered |
| RSPC-UC-003 Exception E2 | UC-014 | covered |
| RSPC-UC-004 Main Flow | UC-015 | covered |
| RSPC-UC-004 Alternative A1 | UC-016 | covered |
| RSPC-UC-004 Exception E1 | UC-017 | covered |
| RSPC-UC-004 Exception E2 | UC-018 | covered |
| RSPC-UC-005 Main Flow | UC-019, UC-020, UC-021 | covered |
| RSPC-UC-005 Alternative A1 | UC-022 | covered |
| RSPC-UC-005 Exception E1 | UC-023 | covered |
| RSPC-UC-005 Exception E2 | UC-024 | covered |
| RSPC-UC-006 Main Flow | UC-025, UC-026 | covered |
| RSPC-UC-006 Alternative A1 | UC-027 | covered |
| RSPC-UC-006 Exception E1 | UC-028 | covered |
| RSPC-UC-006 Exception E2 | UC-029 | covered |
| RSPC-UC-007 Main Flow | UC-030 | covered |
| RSPC-UC-007 Alternative A1 | UC-031 | covered |
| RSPC-UC-007 Exception E1 | UC-032 | covered |
| RSPC-UC-007 Exception E2 | UC-033 | covered |
| RSPC-UC-008 Main Flow | UC-034 | covered |
| RSPC-UC-008 Alternative A1 | UC-035 | covered |
| RSPC-UC-008 Exception E1 | UC-036 | covered |
| RSPC-UC-008 Exception E2 | UC-037 | covered |
| RSPC-UC-009 Main Flow | UC-038 | covered |
| RSPC-UC-009 Exception E1 | UC-039 | covered |
| RSPC-UC-009 Exception E2 | UC-040 | covered |
| RSPC-UC-010 Main Flow | UC-041 | covered |
| RSPC-UC-010 Alternative A1 | UC-042 | covered |
| RSPC-UC-010 Exception E1 | UC-043 | covered |
| RSPC-UC-010 Exception E2 | UC-044 | covered |
| RSPC-UC-011 Main Flow | UC-045 | covered |
| RSPC-UC-011 Exception E1 | UC-046 | covered |
| RSPC-UC-011 Exception E2 | UC-047 | covered |
| RSPC-UC-012 Main Flow | UC-048 | covered |
| RSPC-UC-012 Exception E1 | UC-049 | covered |
| RSPC-UC-012 Exception E2 | UC-050 | covered |
| RSPC-UC-013 Main Flow | UC-051 | covered |
| RSPC-UC-013 Alternative A1 | UC-052 | covered |
| RSPC-UC-013 Exception E1 | UC-053 | covered |
| RSPC-UC-013 Exception E2 | UC-054 | covered |
| RSPC-UC-014 Main Flow | UC-055 | covered |
| RSPC-UC-014 Alternative A1 | UC-056 | covered |
| RSPC-UC-014 Exception E1 | UC-057 | covered |
| RSPC-UC-014 Exception E2 | UC-058 | covered |
| RSPC-UC-015 Main Flow | UC-059 | covered |
| RSPC-UC-015 Exception E1 | UC-060 | covered |
| RSPC-UC-015 Exception E2 | UC-061 | covered |
| RSPC-UC-016 Main Flow | UC-062 | covered |
| RSPC-UC-016 Alternative A1 | UC-063 | covered |
| RSPC-UC-016 Exception E1 | UC-064 | covered |
| RSPC-UC-016 Exception E2 | UC-065 | covered |
| RSPC-UC-017 Main Flow | UC-066 | covered |
| RSPC-UC-017 Alternative A1 | UC-067 | covered |
| RSPC-UC-017 Exception E1 | UC-068 | covered |
| RSPC-UC-017 Exception E2 | UC-069 | covered |
| RSPC-UC-018 Main Flow | UC-070 | covered |
| RSPC-UC-018 Alternative A1 | UC-071 | covered |
| RSPC-UC-018 Exception E1 | UC-072 | covered |
| RSPC-UC-018 Exception E2 | UC-073 | covered |
| RSPC-UC-021 Main Flow | UC-074 | covered |
| RSPC-UC-021 Alternative A1 | UC-075 | covered |
| RSPC-UC-021 Exception E1 | UC-076 | covered |
| RSPC-UC-021 Exception E2 | UC-077 | covered |
| RSPC-UC-022 Main Flow | UC-078 | covered |
| RSPC-UC-022 Exception E1 | UC-079 | covered |
| RSPC-UC-022 Exception E2 | UC-080 | covered |
| RSPC-UC-023 Main Flow | UC-081, UC-082, UC-083 | covered |
| RSPC-UC-023 Exception E1 | UC-084 | covered |
| RSPC-UC-023 Exception E2 | UC-085 | covered |
| RSPC-UC-024 Main Flow | UC-086, UC-087 | covered |
| RSPC-UC-024 Exception E1 | UC-088 | covered |
| RSPC-UC-024 Exception E2 | UC-089 | covered |
| RSPC-UC-025 Main Flow | UC-090 | covered |
| RSPC-UC-025 Exception E1 | UC-091 | covered |
| RSPC-UC-025 Exception E2 | UC-092 | covered |
| RSPC-UC-026 Main Flow | UC-093, UC-094, UC-095 | covered |
| RSPC-UC-026 Exception E1 | UC-096 | covered |
| RSPC-UC-026 Exception E2 | UC-097 | covered |
| RSPC-UC-027 Main Flow | UC-098 | covered |
| RSPC-UC-027 Exception E1 | UC-099 | covered |
| RSPC-UC-027 Exception E2 | UC-100 | covered |
| RSPC-UC-028 Main Flow | UC-101, UC-102 | covered |
| RSPC-UC-028 Alternative A1 | UC-103 | covered |
| RSPC-UC-028 Exception E1 | UC-104 | covered |
| RSPC-UC-028 Exception E2 | UC-105 | covered |
| RSPC-UC-029 Main Flow | UC-106 | covered |
| RSPC-UC-029 Exception E1 | UC-107 | covered |
| RSPC-UC-029 Exception E2 | UC-108 | covered |
| RSPC-UC-030 Main Flow | UC-109 | covered |
| RSPC-UC-030 Exception E1 | UC-110 | covered |
| RSPC-UC-030 Exception E2 | UC-111 | covered |
| RSPC-UC-031 Main Flow | UC-112 | covered |
| RSPC-UC-031 Alternative A1 | UC-113 | covered |
| RSPC-UC-031 Alternative A2 | UC-114 | covered |
| RSPC-UC-031 Exception E1 | UC-115 | covered |
| RSPC-UC-031 Exception E2 | UC-116 | covered |

Unmapped source_ids: none

## Missing obligations / design completion
None missing → the one-time completion round was **not used**.

## Testability notes (obligations kept in the design; flagged, not removed)
- Scope-boundary exception flows ("RSPC does not execute payroll / payment / ledger / procurement /
  inventory / settlement / external-agency / other-module processes"): UC-008 E2, 009 E2, 010 E2,
  011 E2, 012 E2, 013 E2, 015 E2, 022 E2, 023 E2, 024 E2, 025 E2, 026 E2, 027 E2, 028 E2, 029 E2,
  030 E1, 016 E2, 031 E2, 018 E1. Only observable as the *absence* of an external action; the tests
  assert that only RSPC records/status change.
- UC-018 (role sync), UC-029/030 (integrations), UC-031 (event-triggered notification/reminders),
  UC-016 E2 (email failure) depend on platform mechanisms / external dependencies; automatable only
  if RSPC exposes an interface — decided at Step C (NOT_AUTOMATED skip otherwise).
