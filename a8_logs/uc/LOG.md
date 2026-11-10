# A8 — Strategy UC (Use Case Specifications) — Log

Model: Claude Opus 5.5 in Claude Code (same model/effort as other strategies). Fresh session for UC.

- 2026-11-10 20:42 UTC — **Start.** Handoff file was not at the path given in the request
  (`ELM_MODEL_1/Claude outputs/A8_HANDOFF_CLAUDE.md`); located by filename search at
  `specs_rspc/A8_HANDOFF_CLAUDE.md` and read it.
  Deviation note: while locating it, `ls specs_rspc` and `ls a8_logs a8_design tests/a8` printed
  directory/file *names* only (incl. names of hidden folders and FR artefacts). No content of any
  hidden/other-strategy file was opened.
- 20:42 — Step A: read only `specs_rspc/a8_plain/01_*` (Problem Statement) and
  `specs_rspc/a8_plain/03_*` (Use Case Specifications v1.3, 29 active UCs; UC-019/020 retired).
- 20:42 — Created `tests/a8/uc/` (+`__init__.py`), `a8_logs/uc/`, `a8_results/uc/`,
  `a8_snapshots/uc/{raw,final}/`. Wrote filled Prompt A to `a8_logs/uc/PROMPT_A.txt`.
- 20:45 — Applied Prompt A to the two allowed specs; wrote the JSON array unchanged to
  `a8_design/UC_DESIGN.json`: 116 test cases (UC-001..UC-116), valid JSON, exactly the 7 required
  fields each; 39 main-flow, 19 alternative-flow, 58 exception-flow; all 29 active UCs cited.
- 20:45 UTC — Step B: enumerated 106 obligations (29 main + 19 alternative + 58 exception flows) →
  `a8_logs/uc/obligations.md`. Covered 106/106; one-time completion round not used.
  Testability flags recorded (scope-boundary "does not execute" exceptions; role-sync/integration/
  notification UCs depend on interfaces to be checked at Step C).
- 20:45 UTC — **Design frozen.** SHA-256 4a3d74b984f983fb41acbc3d3d508c3f526f59ce308914b5fc63ba9c79555ff9 → `a8_logs/uc/FROZEN.txt`. Stopped; waiting for
  Nikhit's "continue" before Step C.
- 20:47 — Nikhit said "continue". Step C started: reading implementation (never modules/rspc/tests/).
- 20:50 — Step C: read implementation (`modules/rspc/{registry,models,api/*}.py`, root `conftest.py`,
  `fusion_auth/{permissions,authentication}.py`, `core/api/exceptions.py`, one placement test for the
  stub_iam/APIClient pattern). Never opened `modules/rspc/tests/` or `tests/a8/fr/`.
  Only interface: research-proposal API (submit, mine, queue, recommend, verify, decide, authorize).
  Wrote Prompt B → `PROMPT_B.txt`. Tests: `tests/a8/uc/test_uc_proposal.py` (27 automated: UC-001..003,
  005..011, 013..015, 017..021, 023..029, 070, 071) and `test_uc_not_automated.py` (89 NOT_AUTOMATED skips,
  generated from the frozen JSON, reason per UC). 116/116 cases present. Interpretation recorded in
  docstrings: notification events and audit-log entries have no RSPC interface and are not asserted;
  all other parts of each expected result are asserted. Preconditions seeded via ORM.
  Copied to `a8_snapshots/uc/raw/`. Not run before snapshot.
- 20:48 — Step D: `.venv/bin/pytest tests/a8/uc --collect-only -q` → 116 collected, no syntax/import/
  fixture errors. The full run then showed no ERROR-state setup errors either. **Prompt C rounds used: 0.**
  Copied tests to `a8_snapshots/uc/final/` (identical to raw).
- 20:49 — Step E: ran the exact command → 26 passed, 1 failed, 89 skipped, 0 errors (16.5 s).
  Production coverage (excl. tests/migrations): lines 184/199 = 92.46 %, branches 30/40 = 75.00 % →
  `a8_results/uc/coverage_summary.md`. (First run of my summary script crashed with ZeroDivisionError
  on empty `__init__.py` files; I fixed the script, not any machine-generated file.)
- 20:50 — Step F: UC-006 (RSPC-UC-002 A1) failed `'submitted' == 'draft'`. Reproduced alone twice.
  All four checks yes → **Confirmed Implementation Defect D-02** (no draft save/revise). Wrote
  `failures.md`; read and appended to the shared `a8_logs/DEFECTS.md`. The existing rows D-01 and C-01
  were not exposed by UC tests (UC asserts no audit-log or approval-limit behaviour).
- 20:52 — Step G: SUMMARY.md written; `git diff --stat a8-base -- modules config client registry
  openapi core fusion_auth` is empty; frozen design hash unchanged (4a3d74b9…).
