"""A8 strategy WF — CW-RSPC-06 / BW-RSPC-11..12 (project closure, approval and archival).

Generated from the frozen a8_design/WF_DESIGN.json.
No interface exists for this workflow in the A8_BASE implementation, so each
case is a skipped NOT_AUTOMATED test (Prompt B rule); the design is unchanged.
"""
import pytest

REASON = (
    "NOT_AUTOMATED: " +
    "the A8_BASE RSPC module exposes no project/closure record, archival state or API endpoint (only research-proposal endpoints under /api/v1/rspc/proposals/), so the closure workflow states cannot be created or driven."
)


def test_wf_030_bw_rspc_11_full_path_cw_rspc_06_rows_1_2_4():
    """WF-030 | source_id: BW-RSPC-11 full path; CW-RSPC-06 rows 1, 2, 4 (closure approved and archived at Dean-RSPC)

    Purpose: Verify the project-closure success path approved by Dean-RSPC ending in archival with the project completed.
    Expected: State after each step: 1) Closure Submitted; 2) Closure Verified; 3) Archived, and the project is marked completed. The closure never enters Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_031_bw_rspc_12_full_path_cw_rspc_06_rows_1_2_5_7():
    """WF-031 | source_id: BW-RSPC-12 full path; CW-RSPC-06 rows 1, 2, 5, 7 (closure approved and archived via Director)

    Purpose: Verify the project-closure path where Director action is required and the Director approves, ending in archival.
    Expected: State after each step: 1) Closure Submitted; 2) Closure Verified; 3) Forwarded to Director (not yet Archived); 4) Archived, and the project is marked completed.
    """
    pytest.skip(REASON)


def test_wf_032_cw_rspc_06_row_3():
    """WF-032 | source_id: CW-RSPC-06 row 3 (RSPC Admin not-eligible outcome)

    Purpose: Verify the closure verification outcome where the closure record is not eligible for forwarding.
    Expected: Closure state becomes Not Eligible for Forwarding; it does not become Closure Verified and the project is not archived.
    """
    pytest.skip(REASON)


def test_wf_033_cw_rspc_06_row_6():
    """WF-033 | source_id: CW-RSPC-06 row 6 (Dean-RSPC not-approved outcome)

    Purpose: Verify the Dean-RSPC decision outcome where project closure is not approved.
    Expected: Closure state becomes Dean Not Approved; it does not become Archived or Forwarded to Director, and the project is not marked completed.
    """
    pytest.skip(REASON)


def test_wf_034_cw_rspc_06_row_8():
    """WF-034 | source_id: CW-RSPC-06 row 8 (Director not-approved outcome)

    Purpose: Verify the Director decision outcome where a forwarded project closure is not approved.
    Expected: Closure state becomes Director Not Approved; it does not become Archived, and the project is not marked completed.
    """
    pytest.skip(REASON)
