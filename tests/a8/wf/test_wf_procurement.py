"""A8 strategy WF — CW-RSPC-05 / BW-RSPC-09..10 (procurement request).

Generated from the frozen a8_design/WF_DESIGN.json.
No interface exists for this workflow in the A8_BASE implementation, so each
case is a skipped NOT_AUTOMATED test (Prompt B rule); the design is unchanged.
"""
import pytest

REASON = (
    "NOT_AUTOMATED: " +
    "the A8_BASE RSPC module exposes no procurement request or sanctioned-budget model or API endpoint (only research-proposal endpoints under /api/v1/rspc/proposals/), so the procurement workflow states cannot be created or driven."
)


def test_wf_025_bw_rspc_09_full_path_cw_rspc_05_rows_1_2_4():
    """WF-025 | source_id: BW-RSPC-09 full path; CW-RSPC-05 rows 1, 2, 4 (Dean-final procurement approval path)

    Purpose: Verify the procurement request success path approved by Dean-RSPC without Director action.
    Expected: State after each step: 1) Submitted; 2) Verified; 3) Approved. The request never enters Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_026_bw_rspc_10_full_path_cw_rspc_05_rows_1_2_5_7():
    """WF-026 | source_id: BW-RSPC-10 full path; CW-RSPC-05 rows 1, 2, 5, 7 (Director-routed procurement approval path)

    Purpose: Verify the procurement request path where the represented hierarchy requires Director action and the Director approves.
    Expected: State after each step: 1) Submitted; 2) Verified; 3) Forwarded to Director; 4) Approved.
    """
    pytest.skip(REASON)


def test_wf_027_cw_rspc_05_row_3():
    """WF-027 | source_id: CW-RSPC-05 row 3 (verification or sanctioned-budget validation fails)

    Purpose: Verify the procurement verification outcome where verification/sanctioned-budget validation fails and the request is not eligible for forwarding.
    Expected: Request state becomes Not Eligible for Forwarding; it does not become Verified and is not available for Dean-RSPC decision.
    """
    pytest.skip(REASON)


def test_wf_028_cw_rspc_05_row_6():
    """WF-028 | source_id: CW-RSPC-05 row 6 (Dean-RSPC not-approved outcome)

    Purpose: Verify the Dean-RSPC decision outcome where a verified procurement request is not approved.
    Expected: Request state becomes Dean Not Approved; it does not become Approved or Forwarded to Director.
    """
    pytest.skip(REASON)


def test_wf_029_cw_rspc_05_row_8():
    """WF-029 | source_id: CW-RSPC-05 row 8 (Director not-approved outcome)

    Purpose: Verify the Director decision outcome where a forwarded procurement request is not approved/authorized.
    Expected: Request state becomes Director Not Approved; it does not become Approved.
    """
    pytest.skip(REASON)
