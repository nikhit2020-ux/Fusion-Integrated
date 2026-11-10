# A8 — Strategy BR — Summary

| Item | Value |
|---|---|
| Model / runtime | Claude Opus 5.5 / Claude Code (same model and effort as FR, UC) |
| Spec used | 04 Business Rule Specifications v1.3 (+ 01 Problem Statement) |
| Design | `a8_design/BR_DESIGN.json` — 61 test cases, SHA-256 aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca |
| Obligations covered / total | 38/38 active BRs; 67/67 distinct outcome obligations |
| Design completion used (Step B) | No (no gaps) |
| Test cases automated | 29 of 61 |
| Skipped / NOT_AUTOMATED | 32 of 61 |
| Executable | 61/61 (66 pytest items incl. parametrization; 0 collection or setup errors) |
| Passed / Failed | 28 cases passed (33 items), 1 case failed (BR-040) |
| Line coverage (prod only) | 88.94 % (177/199) |
| Branch coverage (prod only) | 65.00 % (26/40) |
| Candidate failures | 1 (BR-040) |
| Confirmed defects | 1 — D-01 "proposal submission not logged" (shared with FR; no new defect) |
| Prompt C repair rounds | 0 of 2 |
| Elapsed | 20:57:55 → 21:10:50 UTC (~12 min) |

## Deviations
- Before snapshotting (Step C, nothing run yet), I corrected two helper slips in my own draft of BR-041 and
  BR-043: one would have raised a KeyError and the other was a meaningless assertion. Test intent and expected
  results were unchanged, and raw = final.
- In Step D I ran the suite once without coverage, to detect run-time setup errors as the handoff permits. No
  test code was changed afterwards.
- The pytest-cov terminal report in `pytest.log` lists the file names under `modules/rspc/tests/`. Their contents
  were not read.
- Corrected one hand-typed timestamp in LOG.md (Step A design entry, 21:10 → 21:00, from the file mtime).
- BR-036/BR-037: RSPC has no single-proposal detail endpoint. Details are read from the "mine" list, and the
  out-of-scope detail request to the nonexistent `proposals/<id>/` route returns 404, so that part of BR-037 is
  weak evidence.
- BR-011/012: "represented policy validation" was implemented using the two value validations RSPC represents
  (budget > 0; end date not before start date).
