"""A8 strategy WF — CW-RSPC-01 / BW-RSPC-01..02 (research proposal workflow).

Generated from the frozen a8_design/WF_DESIGN.json (WF-001..WF-006).
Drives the real RSPC API at /api/v1/rspc/ with the IAM stubbed by the root
`stub_iam` fixture (IAM is an external dependency, not the behaviour under test).
Each actor gets exactly the permissions modules/rspc/registry.py grants its role.
"""
import pytest
from rest_framework.test import APIClient

from conftest import make_session
from modules.rspc.models import ResearchProposal
from modules.rspc.registry import ROLE_GRANTS

pytestmark = pytest.mark.django_db

BASE = "/api/v1/rspc/proposals/"

# Workflow-spec state names -> implementation status codes.
STATE = {
    "Proposal Submitted": "submitted",
    "Department Recommended": "dept_recommended",
    "Department Not Recommended": "dept_not_recommended",
    "Admin Verified": "admin_verified",
    "Not Eligible for Forwarding": "not_eligible",
    "Approved": "approved",
    "Forwarded to Director": "forwarded_to_director",
    "Dean Not Approved": "dean_not_approved",
    "Director Not Approved": "director_not_approved",
}

ACTORS = {
    "Faculty": (2001, "faculty"),
    "HoD": (2002, "faculty"),
    "RSPC Admin": (2003, "staff"),
    "Dean-RSPC": (2004, "faculty"),
    "Director": (2005, "faculty"),
}


@pytest.fixture
def act(stub_iam):
    """Return an APIClient authenticated as the given RSPC role."""
    def _as(role):
        uid, kind = ACTORS[role]
        stub_iam(make_session(
            user_id=uid, kind=kind, roles=(role,), active_role=role,
            permissions=ROLE_GRANTS[role], modules=("rspc",),
        ))
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION="Token wf-token")
        return c
    return _as


def _proposal_payload(budget):
    """All mandatory proposal fields: objectives, timeline, budget, funding source,
    resource requirements."""
    return {
        "title": "Edge AI for agricultural sensing",
        "objectives": "Develop low-power edge inference for field sensors.",
        "start_date": "2027-01-01",
        "end_date": "2028-12-31",
        "budget": budget,
        "funding_agency": "SERB",
        "resource_requirements": "2 JRFs, GPU workstation",
        "department": "CSE",
    }


# Ordinary proposal (no Director condition) vs high-value/significant proposal.
NORMAL_BUDGET = "500000.00"
HIGH_VALUE_BUDGET = "50000000.00"


def _state(pid):
    return ResearchProposal.objects.get(pk=pid).status


def _submit(act, budget=NORMAL_BUDGET):
    r = act("Faculty").post(BASE, _proposal_payload(budget), format="json")
    assert r.status_code == 201, r.content
    return r.json()["id"]


def _step(act, role, pid, action, outcome):
    r = act(role).post(f"{BASE}{pid}/{action}/",
                       {"outcome": outcome, "remarks": f"{role}: {outcome}"},
                       format="json")
    assert r.status_code == 200, r.content


def _dean_queue_ids(act):
    r = act("Dean-RSPC").get(f"{BASE}queue/")
    assert r.status_code == 200, r.content
    return {p["id"] for p in r.json()}


def _to_admin_verified(act, budget=NORMAL_BUDGET):
    pid = _submit(act, budget)
    _step(act, "HoD", pid, "recommend", "recommended")
    _step(act, "RSPC Admin", pid, "verify", "eligible")
    assert _state(pid) == STATE["Admin Verified"]
    return pid


def test_wf_001_bw_rspc_01_dean_final_approval_path(act):
    """WF-001 | source_id: BW-RSPC-01 full path; CW-RSPC-01 rows 1, 2, 4, 6
    (Dean-final approval path)."""
    seen = []

    pid = _submit(act, NORMAL_BUDGET)
    seen.append(_state(pid))
    assert seen[-1] == STATE["Proposal Submitted"]

    _step(act, "HoD", pid, "recommend", "recommended")
    seen.append(_state(pid))
    assert seen[-1] == STATE["Department Recommended"]

    _step(act, "RSPC Admin", pid, "verify", "eligible")
    seen.append(_state(pid))
    assert seen[-1] == STATE["Admin Verified"]

    _step(act, "Dean-RSPC", pid, "decide", "approve")
    seen.append(_state(pid))
    assert seen[-1] == STATE["Approved"]

    assert STATE["Forwarded to Director"] not in seen


def test_wf_002_bw_rspc_02_director_routed_approval_path(act):
    """WF-002 | source_id: BW-RSPC-02 full path; CW-RSPC-01 rows 1, 2, 4, 7, 9
    (Director-routed approval path)."""
    pid = _submit(act, HIGH_VALUE_BUDGET)
    assert _state(pid) == STATE["Proposal Submitted"]

    _step(act, "HoD", pid, "recommend", "recommended")
    assert _state(pid) == STATE["Department Recommended"]

    _step(act, "RSPC Admin", pid, "verify", "eligible")
    assert _state(pid) == STATE["Admin Verified"]

    _step(act, "Dean-RSPC", pid, "decide", "forward")
    assert _state(pid) == STATE["Forwarded to Director"]
    assert _state(pid) != STATE["Approved"]

    _step(act, "Director", pid, "authorize", "approve")
    assert _state(pid) == STATE["Approved"]


def test_wf_003_cw_rspc_01_row_3_hod_not_recommended(act):
    """WF-003 | source_id: CW-RSPC-01 row 3 (HoD not-recommended outcome)."""
    pid = _submit(act)
    assert _state(pid) == STATE["Proposal Submitted"]

    _step(act, "HoD", pid, "recommend", "not_recommended")

    final = _state(pid)
    assert final == STATE["Department Not Recommended"]
    assert final not in (STATE["Department Recommended"], STATE["Admin Verified"],
                         STATE["Approved"])


def test_wf_004_cw_rspc_01_row_5_admin_not_eligible(act):
    """WF-004 | source_id: CW-RSPC-01 row 5 (RSPC Admin not-eligible outcome)."""
    pid = _submit(act)
    _step(act, "HoD", pid, "recommend", "recommended")
    assert _state(pid) == STATE["Department Recommended"]

    _step(act, "RSPC Admin", pid, "verify", "not_eligible")

    final = _state(pid)
    assert final == STATE["Not Eligible for Forwarding"]
    assert final != STATE["Admin Verified"]
    assert pid not in _dean_queue_ids(act)


def test_wf_005_cw_rspc_01_row_8_dean_not_approved(act):
    """WF-005 | source_id: CW-RSPC-01 row 8 (Dean-RSPC not-approved outcome)."""
    pid = _to_admin_verified(act)

    _step(act, "Dean-RSPC", pid, "decide", "not_approve")

    final = _state(pid)
    assert final == STATE["Dean Not Approved"]
    assert final not in (STATE["Approved"], STATE["Forwarded to Director"])


def test_wf_006_cw_rspc_01_row_10_director_not_approved(act):
    """WF-006 | source_id: CW-RSPC-01 row 10 (Director not-approved outcome)."""
    pid = _to_admin_verified(act, HIGH_VALUE_BUDGET)
    _step(act, "Dean-RSPC", pid, "decide", "forward")
    assert _state(pid) == STATE["Forwarded to Director"]

    _step(act, "Director", pid, "authorize", "not_approve")

    final = _state(pid)
    assert final == STATE["Director Not Approved"]
    assert final != STATE["Approved"]
