# UC — failure examination (Step F)

Run: `a8_results/uc/pytest.log` — 26 passed, 1 failed, 0 errors, 89 skipped (NOT_AUTOMATED).

## UC-006 — RSPC-UC-002 Alternative A1

- **Test:** `tests/a8/uc/test_uc_proposal.py::test_UC_006_alternative_A1`
- **Error summary:** `AssertionError: assert 'submitted' == 'draft'`. The create call
  (`POST /api/v1/rspc/proposals/` with `status: "draft"`) returned 201, but the stored proposal is
  `submitted`. The test stops there, before the revise step.

Four checks:
1. **Expected behaviour supported by the cited spec — YES.** RSPC-UC-002 A1: *"Faculty may save or
   revise a draft before submission."* Failure/Minimal Guarantee: *"…the existing draft/record is
   preserved."*
2. **Test correctly implemented and set up — YES.** It uses the only proposal-creation interface
   with a valid payload and an authorized Faculty session. The outcome does not depend on how
   "draft" is signalled. `ResearchProposalView.post` always saves with `status="submitted"`
   (`modules/rspc/api/views.py:23`), and `status` is read-only in `ResearchProposalSerializer`. No
   endpoint lets a proposal be updated or revised (`modules/rspc/api/urls.py`). So no request can
   save or revise a draft.
3. **Reproducible — YES.** Re-ran alone twice; it failed the same way both times.
4. **Observed behaviour contradicts expected — YES.** The proposal is submitted at once and routed
   to HoD review. It cannot be held as a draft or revised before submission.

**Classification: Confirmed Implementation Defect** → `a8_logs/DEFECTS.md` D-02.
