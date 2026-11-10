"""A8 strategy WF — CW-RSPC-04 / BW-RSPC-07..08 (financial and fund request).

Generated from the frozen a8_design/WF_DESIGN.json.
No interface exists for this workflow in the A8_BASE implementation, so each
case is a skipped NOT_AUTOMATED test (Prompt B rule); the design is unchanged.
"""
import pytest

REASON = (
    "NOT_AUTOMATED: " +
    "the A8_BASE RSPC module exposes no fund-utilization/expenditure request model or API endpoint (only research-proposal endpoints under /api/v1/rspc/proposals/), so the financial-request workflow states cannot be created or driven."
)


def test_wf_020_bw_rspc_07_full_path_cw_rspc_04_rows_1_2_4():
    """WF-020 | source_id: BW-RSPC-07 full path; CW-RSPC-04 rows 1, 2, 4 (approval within delegated Dean-RSPC powers)

    Purpose: Verify the financial/fund request success path approved within delegated Dean-RSPC financial powers.
    Expected: State after each step: 1) Submitted; 2) Verified; 3) Approved. The request never enters Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_021_bw_rspc_08_full_path_cw_rspc_04_rows_1_2_5_7():
    """WF-021 | source_id: BW-RSPC-08 full path; CW-RSPC-04 rows 1, 2, 5, 7 (high-value Director-routed approval path)

    Purpose: Verify the financial/fund request path where the high-value/Director condition applies and the Director approves/authorizes.
    Expected: State after each step: 1) Submitted; 2) Verified; 3) Forwarded to Director (not Approved by Dean-RSPC alone); 4) Approved.
    """
    pytest.skip(REASON)


def test_wf_022_cw_rspc_04_row_3():
    """WF-022 | source_id: CW-RSPC-04 row 3 (RSPC Admin not-eligible outcome)

    Purpose: Verify the initial-verification outcome where a financial request is not eligible for forwarding.
    Expected: Request state becomes Not Eligible for Forwarding; it does not become Verified.
    """
    pytest.skip(REASON)


def test_wf_023_cw_rspc_04_row_6():
    """WF-023 | source_id: CW-RSPC-04 row 6 (Dean-RSPC not-approved outcome)

    Purpose: Verify the Dean-RSPC decision outcome where a verified financial request is not approved.
    Expected: Request state becomes Dean Not Approved; it does not become Approved or Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_024_cw_rspc_04_row_8():
    """WF-024 | source_id: CW-RSPC-04 row 8 (Director not-approved outcome)

    Purpose: Verify the Director decision outcome where a forwarded financial request is not approved/authorized.
    Expected: Request state becomes Director Not Approved; it does not become Approved.
    """
    pytest.skip(REASON)
