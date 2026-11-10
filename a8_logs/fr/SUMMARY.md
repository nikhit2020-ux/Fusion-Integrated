# A8 — Strategy FR summary

Model: Claude Opus 5.5, Claude Code (desktop app; repo in WSL). Base: a8-base 4f8c1c7, branch a8-24bcs287. Package: `modules.rspc`.

| Measure | Value |
|---|---|
| Obligations covered / total | 155 / 155 (29 CFR + 126 AFR) |
| Test cases designed (frozen) | 111 (SHA-256 d4b25a61…bc4c5) |
| Test cases automated | 34 |
| Executable (collected without error) | 111 / 111 |
| Passed | 32 |
| Failed | 2 (FR-009, FR-023) |
| Errors | 0 |
| Skipped / NOT_AUTOMATED | 77 |
| Line coverage (production) | 88.94% (177/199) |
| Branch coverage (production) | 65.00% (26/40) |
| Candidate failures | 2 |
| Confirmed implementation defects | 1 (D-01, FR-009: submission not logged) |
| Other classifications | 1 specification ambiguity (C-01, FR-023: Dean limit undefined) |
| Prompt C repair rounds used | 0 / 2 |
| Elapsed | ≈ 15 min (19:59:41 → 20:14 UTC, 2026-11-10), including one wait for "continue" |

NOT_AUTOMATED breakdown (77): consultancy 9, staff appointment 13, finance 12, procurement 9, reports 5, closure 8, notifications 13, integration 3, project updates 2, role-change log 1, admin audit/compliance records 1, budget allocation 1. FR-098/099/100 are counted under staff/finance/procurement. Reason in every case: the RSPC implementation exposes only the research-proposal workflow (CW-RSPC-01).

## Deviations
1. The handoff file was not at `specs_rspc/A8_HANDOFF_CLAUDE.md`. The copy at `~/ELM_MODEL_1/Claude outputs/` was used.
2. Claude Code ran as the Windows desktop app and reached the repo through WSL (`wsl.exe`, `\\wsl.localhost`), not inside WSL.
3. Before the raw snapshot (nothing had run yet), I changed two of my own asserts (FR-003, FR-109) so they don't depend on the order of the decision list. The raw and final snapshots are identical.
4. The commit includes `tests/__init__.py` (it already existed, untracked) and `tests/a8/__init__.py` alongside `tests/a8/fr/`, so the suite imports the same way from a clean checkout.
5. The coverage terminal report lists the file names under `modules/rspc/tests/` (pytest-cov output). Their contents were never opened.
6. Some expected results were interpreted against the available interfaces, as recorded in the test docstrings: FR-001 (completed = workflow-final approved), FR-023/025 (largest budget), FR-010/022/027/103/109 (review outcome in decision remarks), FR-033 (policy = budget > 0), FR-095/096 (role assignment = IAM session).

## Scope check
`git diff --stat a8-base -- modules config client registry openapi core fusion_auth` → empty (20:12:37 UTC).
