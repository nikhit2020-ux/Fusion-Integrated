# A8 — Strategy UC — Summary

Model: Claude Opus 5.5 (Claude Code); spec: 03 Use Case Specifications v1.3 + 01 Problem Statement.
Frozen design: `a8_design/UC_DESIGN.json` (SHA-256 4a3d74b984f983fb41acbc3d3d508c3f526f59ce308914b5fc63ba9c79555ff9).

| Metric | Value |
|---|---|
| Obligations covered / total | 106 / 106 (29 main + 19 alternative + 58 exception flows) |
| Test cases designed (frozen) | 116 |
| Test cases implemented as pytest tests | 116 (27 automated + 89 `NOT_AUTOMATED` skips) |
| Executable (collected without error) | 116 |
| Passed | 26 |
| Failed | 1 (UC-006) |
| Errors | 0 |
| Skipped / NOT_AUTOMATED | 89 |
| Line coverage (modules.rspc, excl. tests/migrations) | 92.46 % (184/199) |
| Branch coverage | 75.00 % (30/40) |
| Candidate failures | 1 |
| Confirmed implementation defects | 1 (D-02: no draft save/revise; UC-006) |
| Prompt C repair rounds used | 0 of 2 |
| Elapsed (wall clock, incl. wait for "continue") | ~10 min (20:42–20:52 UTC, 2026-11-10) |

## Why 89 cases are NOT_AUTOMATED
The A8_BASE code implements only the research-proposal workflow (CW-RSPC-01). No interface exists for
consultancy (UC-003 A1, UC-004 A1, UC-007, UC-008), staff appointments (UC-009, 010, 022, 023), finance
(UC-011, 012, 024), procurement (UC-013, 025, 026), progress reports (UC-014), closure (UC-015, 027, 028),
notifications (UC-016, 031), reports/audit (UC-017), role administration (UC-018 E1/E2), lifecycle
updates (UC-021), integrations (UC-029, 030), a configurable Director threshold (UC-005 A1), or a Faculty
single-record view (UC-001 E2).

## Deviations / interpretations
- The handoff path in the request was wrong; I found the file at `specs_rspc/A8_HANDOFF_CLAUDE.md`. While
  searching, directory listings showed names (not contents) of hidden and FR files.
- Notification events and audit-log entries in expected results have no RSPC interface. They are named
  in each test docstring and not asserted; every other observable part is asserted.
- Preconditions (proposals at a given stage) are seeded via the ORM. IAM identity/roles come from the
  shared `stub_iam` fake, an external dependency. UC-018 role changes are simulated as changed IAM
  sessions.
- The coverage XML lists the hidden `modules/rspc/tests/*` file names; they were excluded and not opened.
