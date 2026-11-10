"""A8 strategy WF — CW-RSPC-02 / BW-RSPC-03..04 (consultancy registration and approval).

Generated from the frozen a8_design/WF_DESIGN.json.
No interface exists for this workflow in the A8_BASE implementation, so each
case is a skipped NOT_AUTOMATED test (Prompt B rule); the design is unchanged.
"""
import pytest

REASON = (
    "NOT_AUTOMATED: " +
    "the A8_BASE RSPC module exposes no consultancy model or API endpoint (only research-proposal endpoints under /api/v1/rspc/proposals/), so the consultancy workflow states cannot be created or driven."
)


def test_wf_007_bw_rspc_03_full_path_cw_rspc_02_rows_1_2_5_7():
    """WF-007 | source_id: BW-RSPC-03 full path; CW-RSPC-02 rows 1, 2, 5, 7 (department-reviewed Dean-final approval path)

    Purpose: Verify the consultancy success path with applicable department review ending in Dean-RSPC approval.
    Expected: State after each step: 1) Consultancy Submitted; 2) Department Recommended; 3) Admin Verified; 4) Approved. The registration never enters Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_008_bw_rspc_04_full_path_cw_rspc_02_rows_1_2_5_8_10():
    """WF-008 | source_id: BW-RSPC-04 full path; CW-RSPC-02 rows 1, 2, 5, 8, 10 (department-reviewed Director-routed approval path)

    Purpose: Verify the consultancy success path with department review where Dean-RSPC forwards to the Director and the Director approves.
    Expected: State after each step: 1) Consultancy Submitted; 2) Department Recommended; 3) Admin Verified; 4) Forwarded to Director; 5) Approved.
    """
    pytest.skip(REASON)


def test_wf_009_cw_rspc_02_row_3():
    """WF-009 | source_id: CW-RSPC-02 row 3 (HoD not-recommended outcome)

    Purpose: Verify the consultancy department-review outcome where the HoD does not recommend.
    Expected: Registration state becomes Department Not Recommended; it does not become Department Recommended, Admin Verified or Approved.
    """
    pytest.skip(REASON)


def test_wf_010_cw_rspc_02_rows_1_4_7():
    """WF-010 | source_id: CW-RSPC-02 rows 1, 4, 7 (department stage not applicable path)

    Purpose: Verify the consultancy path that skips department review when the department stage is not applicable, going directly from submission to admin verification and Dean-RSPC approval.
    Expected: State after each step: 1) Consultancy Submitted; 2) Admin Verified (without passing through Department Recommended); 3) Approved.
    """
    pytest.skip(REASON)


def test_wf_011_cw_rspc_02_row_6_from_consultancy_submitted():
    """WF-011 | source_id: CW-RSPC-02 row 6 from Consultancy Submitted (department stage not applicable; admin not-eligible outcome)

    Purpose: Verify the admin-verification not-eligible outcome on a consultancy registration that has no department stage.
    Expected: Registration state becomes Not Eligible for Forwarding; it does not become Admin Verified.
    """
    pytest.skip(REASON)


def test_wf_012_cw_rspc_02_row_6_from_department_recommended():
    """WF-012 | source_id: CW-RSPC-02 row 6 from Department Recommended (admin not-eligible outcome)

    Purpose: Verify the admin-verification not-eligible outcome on a department-recommended consultancy registration.
    Expected: Registration state becomes Not Eligible for Forwarding; it does not become Admin Verified.
    """
    pytest.skip(REASON)


def test_wf_013_cw_rspc_02_row_9():
    """WF-013 | source_id: CW-RSPC-02 row 9 (Dean-RSPC not-approved outcome)

    Purpose: Verify the Dean-RSPC decision outcome where the consultancy registration is not approved.
    Expected: Registration state becomes Dean Not Approved; it does not become Approved or Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_014_cw_rspc_02_row_11():
    """WF-014 | source_id: CW-RSPC-02 row 11 (Director not-approved outcome)

    Purpose: Verify the Director decision outcome where a forwarded consultancy registration is not approved.
    Expected: Registration state becomes Director Not Approved; it does not become Approved.
    """
    pytest.skip(REASON)
