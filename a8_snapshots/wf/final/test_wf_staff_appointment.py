"""A8 strategy WF — CW-RSPC-03 / BW-RSPC-05..06 (project staff appointment and selection).

Generated from the frozen a8_design/WF_DESIGN.json.
No interface exists for this workflow in the A8_BASE implementation, so each
case is a skipped NOT_AUTOMATED test (Prompt B rule); the design is unchanged.
"""
import pytest

REASON = (
    "NOT_AUTOMATED: " +
    "the A8_BASE RSPC module exposes no staff-appointment / selection-recommendation model or API endpoint (only research-proposal endpoints under /api/v1/rspc/proposals/), so the appointment workflow states cannot be created or driven."
)


def test_wf_015_bw_rspc_05_full_path_cw_rspc_03_rows_1_2_4_5():
    """WF-015 | source_id: BW-RSPC-05 full path; CW-RSPC-03 rows 1, 2, 4, 5 (Dean-final appointment approval path)

    Purpose: Verify the project-staff appointment success path ending in Dean-RSPC approval.
    Expected: State after each step: 1) Appointment Requested; 2) Admin Verified; 3) Selection Recommendation Recorded; 4) Approved. The request never enters Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_016_bw_rspc_06_full_path_cw_rspc_03_rows_1_2_4_6_8():
    """WF-016 | source_id: BW-RSPC-06 full path; CW-RSPC-03 rows 1, 2, 4, 6, 8 (Director-routed appointment approval path)

    Purpose: Verify the project-staff appointment success path where Dean-RSPC forwards to the Director and the Director approves.
    Expected: State after each step: 1) Appointment Requested; 2) Admin Verified; 3) Selection Recommendation Recorded; 4) Forwarded to Director; 5) Approved.
    """
    pytest.skip(REASON)


def test_wf_017_cw_rspc_03_row_3():
    """WF-017 | source_id: CW-RSPC-03 row 3 (RSPC Admin not-eligible outcome)

    Purpose: Verify the admin-verification outcome where a staff appointment request is not eligible for forwarding.
    Expected: Request state becomes Not Eligible for Forwarding; it does not become Admin Verified.
    """
    pytest.skip(REASON)


def test_wf_018_cw_rspc_03_row_7():
    """WF-018 | source_id: CW-RSPC-03 row 7 (Dean-RSPC not-approved outcome)

    Purpose: Verify the Dean-RSPC decision outcome where a staff appointment request is not approved.
    Expected: Request state becomes Dean Not Approved; it does not become Approved or Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_019_cw_rspc_03_row_9():
    """WF-019 | source_id: CW-RSPC-03 row 9 (Director not-approved outcome)

    Purpose: Verify the Director decision outcome where a forwarded staff appointment request is not approved.
    Expected: Request state becomes Director Not Approved; it does not become Approved.
    """
    pytest.skip(REASON)
