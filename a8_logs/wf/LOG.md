# A8 — Strategy WF (Workflow Specifications) — Log

Model: Claude Opus 5.5 (Claude Code). Branch a8-24bcs287, base tag a8-base.

## Start
- 2026-11-10 21:15:33 UTC — session start (fresh session, WF only).

## Step A — design (Prompt A)
- Read ONLY: specs_rspc/A8_HANDOFF_CLAUDE.md, specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt,
  specs_rspc/a8_plain/05_RSPC_Workflow_Specifications_v2.1_SYNCHRONIZED.txt. No implementation, tests, other specs or other strategies' artifacts opened.
  (Directory listing of a8_design/ and tests/a8/ was shown while creating WF folders; only filenames were seen, no other strategy file was opened.)
- Prompt A with placeholders filled saved to a8_logs/wf/PROMPT_A.txt.
- 2026-11-10 21:17:29 UTC — Design produced and saved unchanged to a8_design/WF_DESIGN.json: 34 test cases (WF-001..WF-034),
  12 positive basis paths (one per BW-RSPC-01..12, each also exercising the matching CW success rows), 1 alternative routing path
  (CW-RSPC-02 row 4, department stage not applicable), 21 negative decision outcomes (every non-success row of CW-RSPC-01..06).
  JSON validated (parses; exactly the 7 required fields per case). Not yet frozen — awaiting Step B.

## Step B — obligations and freeze
- 2026-11-10 21:20:05 UTC — Obligations listed in a8_logs/wf/obligations.md: 12 basis paths + 55 composite transitions/decision outcomes = 67; covered 67/67.
  No missing obligations, so the one-time completion pass was not used. Retired legacy workflows (WF-006/008/009) are listed as not obligations, with reasons.
- 2026-11-10 21:20:05 UTC — Design frozen. SHA-256 f1431321de85478027244a1e9ee3c09a2e481d71e03acc52614a1695e4bbd0f6 written to a8_logs/wf/FROZEN.txt.
- Stopped to report counts to Nikhit; waiting for "continue" before Step C.
- 2026-11-10 21:20:29 UTC — Step C started (Nikhit said "continue"). Prompt B saved to a8_logs/wf/PROMPT_B.txt. Reading implementation (excluding modules/rspc/tests/).
- Implementation read: modules/rspc/{models,registry,apps}.py, modules/rspc/api/{urls,serializers,views}.py, config/urls.py (rspc route),
  fusion_auth/{permissions,authentication}.py, root conftest.py, pyproject pytest config, modules/directory/tests/test_search_api.py (stub_iam usage pattern).
  modules/rspc/tests/ NOT opened. Finding: only the research-proposal workflow (CW-RSPC-01) has an interface.
- First draft of test_wf_research_proposal.py was an incomplete stub (empty WF-001 body + placeholder fixture); it was overwritten with the full
  file before any run or snapshot (writing in Step C, not a repair).
- 2026-11-10 21:21:45 UTC — Tests written under tests/a8/wf/ (34 test functions, one per design case):
  - test_wf_research_proposal.py: WF-001..006 automated against /api/v1/rspc/proposals/ (stub_iam for IAM only; role permissions from registry.ROLE_GRANTS).
    Spec state names mapped to status codes; "Director condition" represented by a high-value budget with Dean choosing "forward".
  - test_wf_consultancy.py (WF-007..014), test_wf_staff_appointment.py (WF-015..019), test_wf_financial_request.py (WF-020..024),
    test_wf_procurement.py (WF-025..029), test_wf_project_closure.py (WF-030..034): pytest.skip("NOT_AUTOMATED: ...") — no model/endpoint exists.
  - Syntax check only (py_compile). Not run. Raw copy saved to a8_snapshots/wf/raw/.

## Step D — make executable
- 2026-11-10 21:22:44 UTC — `.venv/bin/pytest tests/a8/wf --collect-only -q`: 34 collected, 0 collection errors.
- Run-time setup check (`.venv/bin/pytest tests/a8/wf -q -rs -p no:cacheprovider`): 6 passed, 28 skipped (NOT_AUTOMATED), 0 errors, 0 failures.
- No syntax/import/fixture/setup error → **0 Prompt C repair rounds used**; no PROMPT_C file written. Tests unchanged.
- Final tests copied to a8_snapshots/wf/final/ (identical to raw/).

## Step E — execute
- 2026-11-10 21:27:57 UTC — exact Step-E command run from repo root (exit 0). Outputs: a8_results/wf/{junit.xml, coverage.xml, pytest.log} (not edited).
- Result: 6 passed, 0 failed, 0 errors, 28 skipped (NOT_AUTOMATED), 9.42 s.
- Production-only coverage (excl. tests/ and migrations/): line 88.44 % (176/199), branch 55.00 % (22/40) → a8_results/wf/coverage_summary.md.

## Step F — failures
- 21:28:44 UTC — 0 failed or errored → a8_logs/wf/failures.md records none. A WF note was appended to the shared a8_logs/DEFECTS.md (no new defects, no existing rows changed).

## Step G — wrap up
- 2026-11-10 21:28:58 UTC — SUMMARY.md written. Elapsed 13 min.
- Verified: git diff --stat a8-base -- modules config client registry openapi core fusion_auth is empty.
