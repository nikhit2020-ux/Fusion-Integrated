"""A8 — Business-Rule-based (BR) tests for RSPC.

Generated from the frozen design a8_design/BR_DESIGN.json
(SHA-256 aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca).
Each test carries its test_id and source_id in its name/docstring.

Interface used: the RSPC REST API under /api/v1/rspc/ (research-proposal workflow).
Identity/roles come from the Fusion IAM (an external service); it is replaced by the
shared `stub_iam` FakeIam from the root conftest, which is the authorized role-management
mechanism as seen by RSPC. RSPC behaviour itself is never mocked.
"""
from datetime import datetime

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from fusion_auth.client import IamSession
from modules.rspc.models import ResearchProposal
from modules.rspc.registry import ROLE_GRANTS

pytestmark = pytest.mark.django_db

BASE = "/api/v1/rspc/proposals/"
MINE = BASE + "mine/"
QUEUE = BASE + "queue/"

FACULTY_A, FACULTY_B, HOD, ADMIN, DEAN, DIRECTOR = 1001, 1002, 2001, 2002, 2003, 2004
ROLE_OF = {FACULTY_A: "Faculty", FACULTY_B: "Faculty", HOD: "HoD", ADMIN: "RSPC Admin",
           DEAN: "Dean-RSPC", DIRECTOR: "Director"}


def iam_session(user_id, roles):
    """Session as the IAM would supply it for `user_id` holding `roles`."""
    perms = frozenset(p for r in roles for p in ROLE_GRANTS[r])
    return IamSession(
        user_id=user_id, username=f"u{user_id}", display_name=f"User {user_id}",
        kind="faculty", active_role=roles[0] if roles else None, roles=tuple(roles),
        permissions=perms, modules=("rspc",) if roles else (),
    )


def valid_payload(**overrides):
    data = {
        "title": "Edge AI for crop monitoring",
        "objectives": "Build and evaluate a low-power crop-disease detector.",
        "start_date": "2026-12-01",
        "end_date": "2028-11-30",
        "budget": "1500000.00",
        "funding_agency": "SERB",
        "resource_requirements": "2 JRFs, GPU workstation, field sensors",
        "department": "CSE",
    }
    data.update(overrides)
    return data


class Rspc:
    """Drives the RSPC API as different actors; the IAM fake decides who is calling."""

    def __init__(self, fake):
        self.fake = fake
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token test-token")

    def as_user(self, user_id, roles=None):
        if roles is None:
            roles = [ROLE_OF[user_id]]
        self.fake.session = iam_session(user_id, roles)
        return self

    def as_role(self, user_id):
        return self.as_user(user_id)

    def post(self, user_id, url, data, roles=None):
        self.as_user(user_id, roles)
        return self.client.post(url, data, format="json")

    def get(self, user_id, url, roles=None):
        self.as_user(user_id, roles)
        return self.client.get(url)

    # -- workflow steps ------------------------------------------------------
    def submit(self, faculty=FACULTY_A, **overrides):
        r = self.post(faculty, BASE, valid_payload(**overrides))
        assert r.status_code == 201, r.content
        return r.json()["id"]

    def recommend(self, pid, outcome="recommended", remarks="", user=HOD):
        return self.post(user, f"{BASE}{pid}/recommend/",
                         {"outcome": outcome, "remarks": remarks})

    def verify(self, pid, outcome="eligible", remarks="", user=ADMIN):
        return self.post(user, f"{BASE}{pid}/verify/", {"outcome": outcome, "remarks": remarks})

    def decide(self, pid, outcome, remarks="", user=DEAN):
        return self.post(user, f"{BASE}{pid}/decide/", {"outcome": outcome, "remarks": remarks})

    def authorize(self, pid, outcome, remarks="", user=DIRECTOR):
        return self.post(user, f"{BASE}{pid}/authorize/",
                         {"outcome": outcome, "remarks": remarks})

    def to_admin(self, pid):
        assert self.recommend(pid).status_code == 200
        return pid

    def to_dean(self, pid):
        self.to_admin(pid)
        assert self.verify(pid).status_code == 200
        return pid

    def to_director(self, pid):
        self.to_dean(pid)
        assert self.decide(pid, "forward").status_code == 200
        return pid

    def queue_ids(self, user_id):
        r = self.get(user_id, QUEUE)
        assert r.status_code == 200, r.content
        return {p["id"] for p in r.json()}

    def mine(self, faculty=FACULTY_A):
        r = self.get(faculty, MINE)
        assert r.status_code == 200, r.content
        return {p["id"]: p for p in r.json()}


def status_of(pid):
    return ResearchProposal.objects.get(pk=pid).status


def decisions_of(pid):
    return list(ResearchProposal.objects.get(pk=pid).decisions.order_by("decided_at", "id"))


@pytest.fixture
def rspc(stub_iam):
    return Rspc(stub_iam())


def not_automated(reason):
    return pytest.mark.skip(reason=f"NOT_AUTOMATED: {reason}")


# ---------------------------------------------------------------------------
# BR-RSPC-004 / 005 / 006 — Director routing and authorization
# ---------------------------------------------------------------------------

def test_BR_001_dean_forwards_director_required_request(rspc):
    """BR-001 | source_id: BR-RSPC-004 condition-true (Director action required).

    Dean-RSPC forwards an eligible proposal whose path requires Director action; it must
    move to the Director stage and not be finalized at Dean-RSPC. (The implementation
    represents the Director-required path through the Dean's 'forward' decision.)"""
    pid = rspc.to_dean(rspc.submit())

    r = rspc.decide(pid, "forward", remarks="Needs Director approval")

    assert r.status_code == 200, r.content
    assert status_of(pid) == "forwarded_to_director"
    assert status_of(pid) != "approved"
    assert pid in rspc.queue_ids(DIRECTOR)


def test_BR_002_director_records_large_funding_approval(rspc):
    """BR-002 | source_id: BR-RSPC-005 permitted (Director records approval of large
    funding request)."""
    pid = rspc.to_director(rspc.submit(budget="95000000.00"))

    r = rspc.authorize(pid, "approve", remarks="Approved by Director")

    assert r.status_code == 200, r.content
    assert status_of(pid) == "approved"
    final = decisions_of(pid)[-1]
    assert final.stage == "Director"
    assert final.actor_id == DIRECTOR
    assert final.outcome == "approve"


def test_BR_003_non_director_cannot_record_director_approval(rspc):
    """BR-003 | source_id: BR-RSPC-005 prohibited (non-Director records Director-stage
    approval)."""
    pid = rspc.to_director(rspc.submit(budget="95000000.00"))

    r = rspc.authorize(pid, "approve", user=DEAN)

    assert r.status_code == 403, r.content
    assert status_of(pid) == "forwarded_to_director"
    assert not any(d.stage == "Director" for d in decisions_of(pid))


@not_automated("RSPC exposes no expenditure-request interface at A8_BASE; only research "
               "proposals are implemented, so a high-value expenditure cannot be created or "
               "authorized.")
def test_BR_004_director_authorizes_high_value_expenditure():
    """BR-004 | source_id: BR-RSPC-006 permitted (Director authorizes high-value
    expenditure)."""


@not_automated("RSPC exposes no expenditure-request interface at A8_BASE; only research "
               "proposals are implemented, so a high-value expenditure cannot be created or "
               "authorized.")
def test_BR_005_non_director_cannot_authorize_high_value_expenditure():
    """BR-005 | source_id: BR-RSPC-006 prohibited (non-Director authorizes high-value
    expenditure)."""


# ---------------------------------------------------------------------------
# BR-RSPC-012 / 069 — research proposal route
# ---------------------------------------------------------------------------

def test_BR_006_full_route_with_director(rspc):
    """BR-006 | source_id: BR-RSPC-012 route with Director applicable; BR-RSPC-069
    condition-true."""
    pid = rspc.submit()
    assert status_of(pid) == "submitted"
    assert pid in rspc.queue_ids(HOD)

    assert rspc.recommend(pid).status_code == 200
    assert pid in rspc.queue_ids(ADMIN)
    assert pid not in rspc.queue_ids(HOD)

    assert rspc.verify(pid).status_code == 200
    assert pid in rspc.queue_ids(DEAN)
    assert pid not in rspc.queue_ids(ADMIN)

    assert rspc.decide(pid, "forward").status_code == 200
    assert pid in rspc.queue_ids(DIRECTOR)
    assert pid not in rspc.queue_ids(DEAN)

    assert rspc.authorize(pid, "approve").status_code == 200
    assert status_of(pid) == "approved"
    assert [d.stage for d in decisions_of(pid)] == ["HoD", "RSPC Admin", "Dean-RSPC",
                                                    "Director"]


def test_BR_007_director_not_applicable_finalized_at_dean(rspc):
    """BR-007 | source_id: BR-RSPC-012 stated exception (Director stage not applicable);
    BR-RSPC-069 condition-false; BR-RSPC-068 permitted."""
    pid = rspc.to_dean(rspc.submit())

    r = rspc.decide(pid, "approve", remarks="Within Dean authority")

    assert r.status_code == 200, r.content
    assert status_of(pid) == "approved"
    assert not any(d.stage == "Director" for d in decisions_of(pid))
    assert pid not in rspc.queue_ids(DIRECTOR)


def test_BR_008_later_stage_cannot_act_before_stage_reached(rspc):
    """BR-008 | source_id: BR-RSPC-012 out-of-order stage action prohibited."""
    pid = rspc.submit()

    r = rspc.decide(pid, "approve")

    assert 400 <= r.status_code < 500, r.content
    assert status_of(pid) == "submitted"
    assert decisions_of(pid) == []


# ---------------------------------------------------------------------------
# BR-RSPC-013 / 014 — proposal validation
# ---------------------------------------------------------------------------

def test_BR_009_complete_proposal_submitted(rspc):
    """BR-009 | source_id: BR-RSPC-013 condition-true (all mandatory fields complete)."""
    r = rspc.post(FACULTY_A, BASE, valid_payload())

    assert r.status_code == 201, r.content
    pid = r.json()["id"]
    assert status_of(pid) == "submitted"
    assert pid in rspc.queue_ids(HOD)


MANDATORY_FIELDS = {
    "objectives": ["objectives"],
    "timelines": ["start_date", "end_date"],
    "budget": ["budget"],
    "funding source": ["funding_agency"],
    "resource requirements": ["resource_requirements"],
}


@pytest.mark.parametrize("label", list(MANDATORY_FIELDS))
def test_BR_010_missing_mandatory_field_rejected(rspc, label):
    """BR-010 | source_id: BR-RSPC-013 condition-false (a mandatory field missing)."""
    fields = MANDATORY_FIELDS[label]
    payload = valid_payload()
    for f in fields:
        payload.pop(f)

    r = rspc.post(FACULTY_A, BASE, payload)

    assert r.status_code == 400, r.content
    body = r.content.decode()
    assert any(f in body for f in fields), body
    assert ResearchProposal.objects.count() == 0
    assert rspc.queue_ids(HOD) == set()


# The validations RSPC represents on proposal values (serializer): budget > 0 and
# end date not before start date.
POLICY_VIOLATIONS = {
    "budget must be positive": {"budget": "0.00"},
    "end date after start date": {"start_date": "2027-06-01", "end_date": "2027-01-01"},
}


@pytest.mark.parametrize("label", list(POLICY_VIOLATIONS))
def test_BR_011_represented_policy_validation_fails(rspc, label):
    """BR-011 | source_id: BR-RSPC-014 represented validation fails; BR-RSPC-070
    represented policy applied."""
    r = rspc.post(FACULTY_A, BASE, valid_payload(**POLICY_VIOLATIONS[label]))

    assert r.status_code == 400, r.content
    assert ResearchProposal.objects.count() == 0


def test_BR_012_represented_policy_validation_passes(rspc):
    """BR-012 | source_id: BR-RSPC-014 represented validation passes."""
    r = rspc.post(FACULTY_A, BASE, valid_payload(budget="10.00", start_date="2027-01-01",
                                                 end_date="2027-06-01"))

    assert r.status_code == 201, r.content
    pid = r.json()["id"]
    assert status_of(pid) == "submitted"
    assert pid in rspc.queue_ids(HOD)


# ---------------------------------------------------------------------------
# BR-RSPC-015 / 016 — decision records
# ---------------------------------------------------------------------------

def test_BR_013_each_decision_has_timestamp(rspc):
    """BR-013 | source_id: BR-RSPC-015."""
    pid = rspc.submit()
    before = timezone.now()
    assert rspc.recommend(pid).status_code == 200
    assert rspc.verify(pid).status_code == 200
    assert rspc.decide(pid, "approve").status_code == 200
    after = timezone.now()

    decisions = rspc.mine()[pid]["decisions"]

    assert len(decisions) == 3
    for d in decisions:
        assert d["decided_at"], d
        ts = datetime.fromisoformat(d["decided_at"].replace("Z", "+00:00"))
        assert before <= ts <= after


def test_BR_014_each_decision_keeps_remarks(rspc):
    """BR-014 | source_id: BR-RSPC-016."""
    pid = rspc.submit()
    assert rspc.recommend(pid, remarks="HoD: aligned with dept goals").status_code == 200
    assert rspc.verify(pid, remarks="Admin: documents complete").status_code == 200
    assert rspc.decide(pid, "approve", remarks="Dean: approved").status_code == 200

    decisions = rspc.mine()[pid]["decisions"]

    assert {d["stage"]: d["remarks"] for d in decisions} == {
        "HoD": "HoD: aligned with dept goals",
        "RSPC Admin": "Admin: documents complete",
        "Dean-RSPC": "Dean: approved",
    }


# ---------------------------------------------------------------------------
# Request types with no interface at A8_BASE
# ---------------------------------------------------------------------------

@not_automated("RSPC exposes no consultancy interface at A8_BASE.")
def test_BR_015_consultancy_route_with_hod_and_director():
    """BR-015 | source_id: BR-RSPC-022 HoD and Director stages applicable."""


@not_automated("RSPC exposes no consultancy interface at A8_BASE.")
def test_BR_016_consultancy_route_without_hod_and_director():
    """BR-016 | source_id: BR-RSPC-022 stated exception (HoD and Director stages not
    applicable)."""


@not_automated("RSPC exposes no staff-appointment interface at A8_BASE.")
def test_BR_017_staff_appointment_finalized_at_dean():
    """BR-017 | source_id: BR-RSPC-026 Director not applicable."""


@not_automated("RSPC exposes no staff-appointment interface at A8_BASE.")
def test_BR_018_staff_appointment_routed_to_director():
    """BR-018 | source_id: BR-RSPC-026 Director applicable."""


@not_automated("RSPC exposes no fund-utilization/expenditure request interface and no "
               "delegated-power configuration at A8_BASE.")
def test_BR_019_financial_request_within_delegated_powers():
    """BR-019 | source_id: BR-RSPC-032 within delegated powers; BR-RSPC-033
    condition-false."""


@not_automated("RSPC exposes no fund-utilization/expenditure request interface and no "
               "delegated-power configuration at A8_BASE.")
def test_BR_020_financial_request_beyond_delegated_powers():
    """BR-020 | source_id: BR-RSPC-032 beyond delegated powers; BR-RSPC-033
    condition-true."""


@not_automated("RSPC exposes no financial-request or audit-log interface at A8_BASE.")
def test_BR_021_financial_lifecycle_events_logged():
    """BR-021 | source_id: BR-RSPC-034."""


@not_automated("RSPC exposes no procurement-request interface and no sanctioned-budget "
               "record at A8_BASE.")
def test_BR_022_procurement_within_sanctioned_budget():
    """BR-022 | source_id: BR-RSPC-035 within sanctioned budget."""


@not_automated("RSPC exposes no procurement-request interface and no sanctioned-budget "
               "record at A8_BASE.")
def test_BR_023_procurement_exceeding_sanctioned_budget():
    """BR-023 | source_id: BR-RSPC-035 exceeds sanctioned budget."""


@not_automated("RSPC exposes no procurement-request interface at A8_BASE.")
def test_BR_024_procurement_hierarchy_followed():
    """BR-024 | source_id: BR-RSPC-036 permitted (represented hierarchy followed)."""


@not_automated("RSPC exposes no procurement-request interface at A8_BASE.")
def test_BR_025_procurement_hierarchy_bypass_blocked():
    """BR-025 | source_id: BR-RSPC-036 prohibited (hierarchy bypass)."""


@not_automated("RSPC exposes no reporting-schedule, report-status or reminder interface "
               "at A8_BASE.")
def test_BR_026_report_due_and_reminder_on_schedule():
    """BR-026 | source_id: BR-RSPC-037 schedule due date reached."""


@not_automated("RSPC exposes no reporting-schedule, report-status or reminder interface "
               "at A8_BASE.")
def test_BR_027_no_report_due_before_schedule():
    """BR-027 | source_id: BR-RSPC-037 schedule due date not reached."""


@not_automated("RSPC exposes no progress-report interface at A8_BASE.")
def test_BR_028_authorized_actor_sees_progress_reports():
    """BR-028 | source_id: BR-RSPC-038 authorized actor."""


@not_automated("RSPC exposes no progress-report interface at A8_BASE.")
def test_BR_029_unauthorized_actor_denied_progress_reports():
    """BR-029 | source_id: BR-RSPC-038 unauthorized actor."""


@not_automated("RSPC exposes no utilization-report interface at A8_BASE.")
def test_BR_030_authorized_actor_sees_utilization_reports():
    """BR-030 | source_id: BR-RSPC-039 authorized actor."""


@not_automated("RSPC exposes no utilization-report interface at A8_BASE.")
def test_BR_031_unauthorized_actor_denied_utilization_reports():
    """BR-031 | source_id: BR-RSPC-039 unauthorized actor."""


@not_automated("RSPC exposes no project-closure or archival interface at A8_BASE.")
def test_BR_032_closure_approved_project_archived():
    """BR-032 | source_id: BR-RSPC-043 closure approved."""


@not_automated("RSPC exposes no project-closure or archival interface at A8_BASE.")
def test_BR_033_closure_not_approved_project_not_archived():
    """BR-033 | source_id: BR-RSPC-043 closure not approved."""


@not_automated("RSPC exposes no integration interface or integration configuration at "
               "A8_BASE.")
def test_BR_034_configured_integration_processed():
    """BR-034 | source_id: BR-RSPC-045 configured integration."""


@not_automated("RSPC exposes no integration interface or integration configuration at "
               "A8_BASE.")
def test_BR_035_unconfigured_integration_not_processed():
    """BR-035 | source_id: BR-RSPC-045 unconfigured integration."""


# ---------------------------------------------------------------------------
# BR-RSPC-048 / 049 / 050 — access control and audit
# ---------------------------------------------------------------------------

def test_BR_036_owner_sees_own_proposal(rspc):
    """BR-036 | source_id: BR-RSPC-048 authorized scope.

    RSPC has no single-proposal detail endpoint; the 'mine' list returns each proposal's
    full details, so the details of P-A are read from it."""
    pid = rspc.submit(faculty=FACULTY_A, title="P-A")

    mine = rspc.mine(FACULTY_A)

    assert pid in mine
    assert mine[pid]["title"] == "P-A"
    assert mine[pid]["pi_id"] == FACULTY_A


def test_BR_037_other_faculty_cannot_see_proposal(rspc):
    """BR-037 | source_id: BR-RSPC-048 outside authorized scope."""
    pid = rspc.submit(faculty=FACULTY_A, title="P-A")

    assert pid not in rspc.mine(FACULTY_B)
    r = rspc.get(FACULTY_B, f"{BASE}{pid}/")
    assert r.status_code in (403, 404), r.content
    assert b"P-A" not in r.content


def test_BR_038_hod_may_record_recommendation(rspc):
    """BR-038 | source_id: BR-RSPC-049 permitted action."""
    pid = rspc.submit()

    r = rspc.recommend(pid, remarks="Recommended")

    assert r.status_code == 200, r.content
    d = decisions_of(pid)
    assert len(d) == 1 and d[0].stage == "HoD" and d[0].actor_id == HOD


def test_BR_039_faculty_cannot_record_hod_decision(rspc):
    """BR-039 | source_id: BR-RSPC-049 unauthorized action blocked."""
    pid = rspc.submit()

    r = rspc.recommend(pid, user=FACULTY_A)

    assert r.status_code == 403, r.content
    assert status_of(pid) == "submitted"
    assert decisions_of(pid) == []


def test_BR_040_submission_and_decision_logged(rspc):
    """BR-040 | source_id: BR-RSPC-050.

    The proposal's decision history (returned with the proposal) is the RSPC audit/history
    record available through the interface."""
    before = timezone.now()
    pid = rspc.submit()
    assert rspc.recommend(pid, remarks="ok").status_code == 200

    log = rspc.mine()[pid]["decisions"]

    submission = [e for e in log if e["actor_id"] == FACULTY_A]
    decision = [e for e in log if e["actor_id"] == HOD]
    assert submission, f"no submission entry in audit log: {log}"
    assert decision, f"no decision entry in audit log: {log}"
    for e in submission + decision:
        assert e["outcome"]
        assert datetime.fromisoformat(e["decided_at"].replace("Z", "+00:00")) >= before


# ---------------------------------------------------------------------------
# BR-RSPC-053 / 054 / 055 — role assignment through the authorized mechanism (IAM)
# ---------------------------------------------------------------------------

NEW_USER, USER_U, USER_V = 3001, 3002, 3003


def test_BR_041_assignment_via_iam_applied(rspc):
    """BR-041 | source_id: BR-RSPC-053 authorized mechanism."""
    pid = rspc.submit()
    url = f"{BASE}{pid}/recommend/"
    # No RSPC role yet.
    assert rspc.post(NEW_USER, url, {"outcome": "recommended"}, roles=[]).status_code == 403

    # The authorized IAM now assigns HoD to the user.
    r = rspc.post(NEW_USER, url, {"outcome": "recommended"}, roles=["HoD"])

    assert r.status_code == 200, r.content
    assert status_of(pid) == "dept_recommended"


def test_BR_042_self_assignment_outside_iam_not_applied(rspc):
    """BR-042 | source_id: BR-RSPC-053 unauthorized source."""
    pid = rspc.to_dean(rspc.submit())
    claimed = {"outcome": "approve", "role": "Dean-RSPC", "roles": ["Dean-RSPC"],
               "active_role": "Dean-RSPC", "permissions": ["rspc.proposal.decide"]}

    r = rspc.post(FACULTY_A, f"{BASE}{pid}/decide/", claimed)

    assert r.status_code == 403, r.content
    assert status_of(pid) == "admin_verified"


def test_BR_043_reassignment_via_iam_applied(rspc):
    """BR-043 | source_id: BR-RSPC-054 authorized mechanism."""
    pid = rspc.submit()
    url = f"{BASE}{pid}/recommend/"
    # Before: U holds HoD, V does not.
    assert rspc.post(USER_V, url, {"outcome": "recommended"},
                     roles=["Faculty"]).status_code == 403

    # The authorized IAM reassigns HoD from U to V.
    r = rspc.post(USER_V, url, {"outcome": "recommended"}, roles=["HoD"])

    assert r.status_code == 200, r.content
    assert status_of(pid) == "dept_recommended"


def test_BR_044_reassignment_outside_iam_not_applied(rspc):
    """BR-044 | source_id: BR-RSPC-054 unauthorized source."""
    pid = rspc.submit()
    transfer = {"outcome": "recommended", "role": "HoD", "roles": ["HoD"],
                "reassign_from": USER_U, "reassign_to": USER_V}

    r_v = rspc.post(USER_V, f"{BASE}{pid}/recommend/", transfer, roles=["Faculty"])

    assert r_v.status_code == 403, r_v.content
    assert status_of(pid) == "submitted"
    r_u = rspc.post(USER_U, f"{BASE}{pid}/recommend/", {"outcome": "recommended"},
                    roles=["HoD"])
    assert r_u.status_code == 200, r_u.content


def test_BR_045_role_change_effective_immediately(rspc):
    """BR-045 | source_id: BR-RSPC-055."""
    p1 = rspc.submit()
    p2 = rspc.submit()
    # U is HoD and can act.
    assert pid_ok(rspc.post(USER_U, f"{BASE}{p1}/recommend/", {"outcome": "recommended"},
                            roles=["HoD"]))
    # IAM: HoD role moves from U to V. Immediately afterwards:
    r_u = rspc.post(USER_U, f"{BASE}{p2}/recommend/", {"outcome": "recommended"},
                    roles=["Faculty"])
    r_v = rspc.post(USER_V, f"{BASE}{p2}/recommend/", {"outcome": "recommended"},
                    roles=["HoD"])

    assert r_u.status_code == 403, r_u.content
    assert r_v.status_code == 200, r_v.content
    assert [d.actor_id for d in decisions_of(p2)] == [USER_V]


def pid_ok(response):
    return response.status_code == 200


# ---------------------------------------------------------------------------
# Scope boundaries
# ---------------------------------------------------------------------------

@not_automated("RSPC exposes no staff-appointment or stipend-status interface at A8_BASE.")
def test_BR_046_no_hr_or_payroll_execution():
    """BR-046 | source_id: BR-RSPC-058."""


@not_automated("RSPC exposes no financial-request or transaction-record interface at "
               "A8_BASE.")
def test_BR_047_no_accounting_or_payment_execution():
    """BR-047 | source_id: BR-RSPC-059."""


@not_automated("RSPC exposes no procurement-status or asset-declaration interface at "
               "A8_BASE.")
def test_BR_048_no_procurement_or_inventory_execution():
    """BR-048 | source_id: BR-RSPC-060."""


@not_automated("RSPC triggers no notification events and exposes no notification "
               "interface at A8_BASE.")
def test_BR_049_notification_triggered_on_submission():
    """BR-049 | source_id: BR-RSPC-061 notification triggered."""


@not_automated("RSPC triggers no notification events and exposes no notification "
               "interface at A8_BASE, so recording of the event under an email-delivery "
               "failure cannot be observed.")
def test_BR_050_delivery_failure_does_not_fail_rspc_action():
    """BR-050 | source_id: BR-RSPC-061 stated exception (external delivery failure)."""


@not_automated("RSPC exposes no external funding-agency submission/disbursement tracking "
               "interface at A8_BASE.")
def test_BR_051_external_funding_agency_tracking_only():
    """BR-051 | source_id: BR-RSPC-062."""


def test_BR_052_unauthenticated_request_rejected(stub_iam):
    """BR-052 | source_id: BR-RSPC-063."""
    stub_iam()  # IAM present, but the request carries no credential
    ResearchProposal.objects.create(title="secret", objectives="x", pi_id=FACULTY_A,
                                    status="submitted")

    r = APIClient().get(MINE)

    assert r.status_code == 401, r.content
    assert b"secret" not in r.content


@not_automated("RSPC exposes no proposal/project update interface at A8_BASE, so a "
               "lifecycle-permitted update cannot be attempted.")
def test_BR_053_update_permitted_in_lifecycle_state():
    """BR-053 | source_id: BR-RSPC-065 update permitted in current lifecycle state."""


@not_automated("RSPC exposes no proposal/project update interface at A8_BASE, so a "
               "lifecycle-prohibited update cannot be attempted.")
def test_BR_054_update_not_permitted_in_lifecycle_state():
    """BR-054 | source_id: BR-RSPC-065 update not permitted in current lifecycle state."""


# ---------------------------------------------------------------------------
# BR-RSPC-066 / 067 / 068 / 070 — forwarding and Dean authority
# ---------------------------------------------------------------------------

def test_BR_055_eligible_verification_forwarded(rspc):
    """BR-055 | source_id: BR-RSPC-066 eligible verification outcome."""
    pid = rspc.to_admin(rspc.submit())

    r = rspc.verify(pid, "eligible")

    assert r.status_code == 200, r.content
    assert pid in rspc.queue_ids(DEAN)


def test_BR_056_ineligible_verification_not_advanced(rspc):
    """BR-056 | source_id: BR-RSPC-066 ineligible verification outcome."""
    pid = rspc.to_admin(rspc.submit())

    r = rspc.verify(pid, "not_eligible", remarks="Missing compliance documents")

    assert r.status_code == 200, r.content
    assert pid not in rspc.queue_ids(DEAN)
    assert status_of(pid) != "admin_verified"


def test_BR_057_recommended_forwarded(rspc):
    """BR-057 | source_id: BR-RSPC-067 recommended."""
    pid = rspc.submit()

    r = rspc.recommend(pid, "recommended")

    assert r.status_code == 200, r.content
    assert [d.outcome for d in decisions_of(pid)] == ["recommended"]
    assert pid in rspc.queue_ids(ADMIN)


def test_BR_058_not_recommended_recorded_not_forwarded(rspc):
    """BR-058 | source_id: BR-RSPC-067 not recommended."""
    pid = rspc.submit()

    r = rspc.recommend(pid, "not_recommended", remarks="Out of department scope")

    assert r.status_code == 200, r.content
    d = decisions_of(pid)
    assert len(d) == 1 and d[0].outcome == "not_recommended"
    assert d[0].remarks == "Out of department scope"
    assert pid not in rspc.queue_ids(ADMIN)


@not_automated("A8_BASE represents no Dean-RSPC authority limit or Director-required "
               "condition, so a request 'outside Dean authority' cannot be set up; the "
               "precondition cannot be established through the available interfaces.")
def test_BR_059_dean_cannot_finalize_outside_authority():
    """BR-059 | source_id: BR-RSPC-068 outside authority (forward/escalate); BR-RSPC-004
    Dean does not finalize."""


def test_BR_060_dean_cannot_approve_ineligible_request(rspc):
    """BR-060 | source_id: BR-RSPC-068 ineligible request."""
    pid = rspc.to_admin(rspc.submit())
    assert rspc.verify(pid, "not_eligible").status_code == 200

    r = rspc.decide(pid, "approve")

    assert 400 <= r.status_code < 500, r.content
    assert status_of(pid) != "approved"


def test_BR_061_unrepresented_policy_not_invented(rspc):
    """BR-061 | source_id: BR-RSPC-070 unrepresented external policy not invented."""
    r = rspc.post(FACULTY_A, BASE, valid_payload(budget="99999999.99"))
    assert r.status_code == 201, r.content
    pid = r.json()["id"]

    assert rspc.recommend(pid).status_code == 200
    assert rspc.verify(pid).status_code == 200
    assert rspc.decide(pid, "approve").status_code == 200

    assert status_of(pid) == "approved"
    assert not any(d.stage == "Director" for d in decisions_of(pid))
