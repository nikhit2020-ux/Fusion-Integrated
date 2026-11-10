# BR obligations → test cases (Step B)

Source: `04_RSPC_Business_Rule_Specifications_v1.3` (38 active BRs) + Problem Statement.
Obligation = each active BR, split into each explicitly stated distinct outcome
(permitted/prohibited, threshold side, condition true/false, stated exception) per the Section-7 BR rule.
Retired legacy IDs (32) have no rule statement and are not obligations.

| # | Obligation | Test(s) | Covered |
|---|---|---|---|
| 1 | BR-RSPC-004 Dean forwards Director-required request to Director (not finalized at Dean) | BR-001, BR-059 | yes |
| 2 | BR-RSPC-005 permitted: Director records approval of large funding request | BR-002 | yes |
| 3 | BR-RSPC-005 prohibited: only Director may record it | BR-003 | yes |
| 4 | BR-RSPC-006 permitted: Director authorizes high-value expenditure | BR-004 | yes |
| 5 | BR-RSPC-006 prohibited: only Director may authorize | BR-005 | yes |
| 6 | BR-RSPC-012 route F→HoD→Admin→Dean→Director (Director applicable) | BR-006 | yes |
| 7 | BR-RSPC-012 exception: Director stage not applicable | BR-007 | yes |
| 8 | BR-RSPC-012 stages followed in order (no stage skipped) | BR-008 (also BR-006) | yes |
| 9 | BR-RSPC-013 mandatory fields complete → submitted/advanced | BR-009 | yes |
| 10 | BR-RSPC-013 mandatory field incomplete → not advanced (objectives, timelines, budget, funding source, resource requirements) | BR-010 | yes |
| 11 | BR-RSPC-014 represented validation fails → advancement prevented | BR-011 | yes |
| 12 | BR-RSPC-014 represented validation passes → advances | BR-012 | yes |
| 13 | BR-RSPC-015 decision timestamp recorded | BR-013 | yes |
| 14 | BR-RSPC-016 decision remarks recorded | BR-014 | yes |
| 15 | BR-RSPC-022 consultancy: HoD/Director stages applicable | BR-015 | yes |
| 16 | BR-RSPC-022 exception: HoD/Director stages not applicable | BR-016 | yes |
| 17 | BR-RSPC-026 staff appointment → Dean-RSPC (Director not applicable) | BR-017 | yes |
| 18 | BR-RSPC-026 staff appointment → Dean-RSPC → Director (applicable) | BR-018 | yes |
| 19 | BR-RSPC-032 within delegated powers → Dean approves | BR-019 | yes |
| 20 | BR-RSPC-032 beyond delegated powers → escalation path | BR-020 | yes |
| 21 | BR-RSPC-033 condition true → routed to Director | BR-020 | yes |
| 22 | BR-RSPC-033 condition false → not routed to Director | BR-019 | yes |
| 23 | BR-RSPC-034 financial lifecycle events logged (request, verification, approval, escalation, transaction) | BR-021 | yes |
| 24 | BR-RSPC-035 within sanctioned budget → eligible | BR-022 | yes |
| 25 | BR-RSPC-035 exceeds sanctioned budget → not eligible | BR-023 | yes |
| 26 | BR-RSPC-036 represented procurement hierarchy followed | BR-024 | yes |
| 27 | BR-RSPC-036 hierarchy bypass blocked | BR-025 | yes |
| 28 | BR-RSPC-037 due date reached → pending status + reminder | BR-026 | yes |
| 29 | BR-RSPC-037 due date not reached → no pending/reminder | BR-027 | yes |
| 30 | BR-RSPC-038 authorized actor sees historical progress reports (whole lifecycle) | BR-028 | yes |
| 31 | BR-RSPC-038 unauthorized actor denied | BR-029 | yes |
| 32 | BR-RSPC-039 authorized actor sees historical utilization reports (whole lifecycle) | BR-030 | yes |
| 33 | BR-RSPC-039 unauthorized actor denied | BR-031 | yes |
| 34 | BR-RSPC-043 closure approved → archived with audit trail | BR-032 | yes |
| 35 | BR-RSPC-043 closure not approved → not archived | BR-033 | yes |
| 36 | BR-RSPC-045 configured integration processed | BR-034 | yes |
| 37 | BR-RSPC-045 unconfigured integration not processed | BR-035 | yes |
| 38 | BR-RSPC-048 authorized data displayed | BR-036 | yes |
| 39 | BR-RSPC-048 data outside scope not displayed | BR-037 | yes |
| 40 | BR-RSPC-049 permitted action allowed | BR-038 | yes |
| 41 | BR-RSPC-049 unauthorized action blocked | BR-039 | yes |
| 42 | BR-RSPC-050 audit/compliance log retained | BR-040 | yes |
| 43 | BR-RSPC-053 assignment via authorized mechanism applied | BR-041 | yes |
| 44 | BR-RSPC-053 assignment from other source not applied | BR-042 | yes |
| 45 | BR-RSPC-054 reassignment via authorized mechanism applied | BR-043 | yes |
| 46 | BR-RSPC-054 reassignment from other source not applied | BR-044 | yes |
| 47 | BR-RSPC-055 authorized role change effective immediately | BR-045 | yes |
| 48 | BR-RSPC-058 no HR/payroll execution (records/status only) | BR-046 | yes |
| 49 | BR-RSPC-059 no accounting/bank-payment execution | BR-047 | yes |
| 50 | BR-RSPC-060 no procurement/inventory execution | BR-048 | yes |
| 51 | BR-RSPC-061 notification triggered via Fusion channels | BR-049 | yes |
| 52 | BR-RSPC-061 exception: external delivery failure does not expand RSPC scope | BR-050 | yes |
| 53 | BR-RSPC-062 external funding-agency process not executed (tracking only) | BR-051 | yes |
| 54 | BR-RSPC-063 platform auth consumed, not administered | BR-052 | yes |
| 55 | BR-RSPC-065 lifecycle-permitted update saved | BR-053 | yes |
| 56 | BR-RSPC-065 non-permitted update rejected | BR-054 | yes |
| 57 | BR-RSPC-066 eligible verification → forwarded | BR-055 | yes |
| 58 | BR-RSPC-066 ineligible verification → not advanced | BR-056 | yes |
| 59 | BR-RSPC-067 recommended → forwarded | BR-057 | yes |
| 60 | BR-RSPC-067 not recommended → recorded, not forwarded | BR-058 | yes |
| 61 | BR-RSPC-068 eligible within authority → Dean approves | BR-007 | yes |
| 62 | BR-RSPC-068 outside authority → forward/escalate, not finalized | BR-059 | yes |
| 63 | BR-RSPC-068 ineligible request → Dean may not approve | BR-060 | yes |
| 64 | BR-RSPC-069 condition true → enters Director stage | BR-006 | yes |
| 65 | BR-RSPC-069 condition false → does not enter Director stage | BR-007 | yes |
| 66 | BR-RSPC-070 represented policy applied | BR-011 | yes |
| 67 | BR-RSPC-070 unrepresented external value not invented | BR-061 | yes |

**Coverage:** 38/38 active BRs; 67/67 distinct outcome obligations covered.

**Gaps:** none → no design completion step needed; no cases appended.

**Untestable obligations:** none excluded at design level. Note for Step C (not a design change):
several obligations concern behaviour (consultancy, staff, finance, procurement, reporting,
closure, integration, notifications) that may have no implementation interface; those will be
handled as `NOT_AUTOMATED: <reason>` skips per Prompt B if so.
