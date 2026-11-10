# A8 — Strategy WF (Workflow Specifications) — Summary

Model: Claude Opus 5.5 in Claude Code (same model/effort as FR, UC and BR). Base: tag a8-base (4f8c1c7), branch a8-24bcs287. Package: modules.rspc.

| Metric | Value |
|---|---|
| Obligations covered / total | 67 / 67 (12 basis paths + 55 composite transitions/decision outcomes) |
| Test cases designed (frozen) | 34 (WF-001..WF-034), SHA-256 f1431321de85478027244a1e9ee3c09a2e481d71e03acc52614a1695e4bbd0f6 |
| Test cases automated | 6 (WF-001..006, CW-RSPC-01 research proposal) |
| Executable (collected without error) | 34 / 34 |
| Passed | 6 |
| Failed | 0 |
| Errors | 0 |
| Skipped / NOT_AUTOMATED | 28 (WF-007..034: consultancy, staff appointment, financial, procurement, closure; there is no interface for them in A8_BASE) |
| Line coverage (production) | 88.44 % (176/199) |
| Branch coverage (production) | 55.00 % (22/40) |
| Candidate failures | 0 |
| Confirmed implementation defects | 0 |
| Prompt C repair rounds used | 0 / 2 |
| Elapsed (wall clock, session start 21:15:33 UTC → 2026-11-10 21:28:58 UTC) | 13 min, including waits for Nikhit's go-ahead between steps |

## Deviations / notes
- A directory listing while creating folders showed the *filenames* in a8_design/ and tests/a8/ (other strategies' files existed). No other strategy's file was opened before Step F.
  In Step F only the shared a8_logs/DEFECTS.md was read, as permitted.
- The design was completed in one pass; the one-time completion pass in Step B was not needed.
- The first draft of test_wf_research_proposal.py was an incomplete stub. It was overwritten with the full file in Step C, before the raw snapshot and before any run.
  raw/ and final/ snapshots are identical.
- In Step D, one plain run without coverage (`pytest tests/a8/wf -q -rs -p no:cacheprovider`) was done to detect run-time setup errors. None were found and nothing was changed.
- Implementation mapping choices in the tests: spec state names were mapped to status codes, and "Director action required" was represented by a high-value budget with the Dean choosing `forward`
  (the implementation has no automatic routing rule).
- Production code was not modified. xfail and mocks of the behaviour under test were not used. Only the IAM was stubbed, using the root `stub_iam` fixture.
