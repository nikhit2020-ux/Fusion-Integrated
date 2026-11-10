"""A8 strategy FR — tests generated from the frozen a8_design/FR_DESIGN.json
(SHA-256 d4b25a61d72396e4239717456594047b75d50d98e57c62152fbeaf6a10bbc4c5).

One test per design case. Each docstring starts with "<test_id> | <source_id>".
The IAM is the only external dependency; it is replaced by the shared
`stub_iam` fake from the root conftest. RSPC behaviour is never mocked.
"""
import pytest
from django.urls import URLPattern, URLResolver
from rest_framework.test import APIClient

from conftest import make_session
from fusion_auth.permissions import _HasModuleGrant, _HasPermission
from modules.rspc.api import urls as rspc_urls
from modules.rspc.models import ResearchProposal
from modules.rspc.registry import ROLE_GRANTS

pytestmark = pytest.mark.django_db

BASE = "/api/v1/rspc/proposals/"

F1, F2, HOD, ADMIN, DEAN, DIRECTOR, OUTSIDER = 2001, 2002, 3001, 3002, 3003, 3004, 4001
ROLE_OF = {F1: "Faculty", F2: "Faculty", HOD: "HoD", ADMIN: "RSPC Admin",
           DEAN: "Dean-RSPC", DIRECTOR: "Director"}

VALID = {
    "title": "Edge AI for crop disease monitoring",
    "objectives": "Build and field-test a low-power crop disease classifier.",
    "start_date": "2027-01-01",
    "end_date": "2028-12-31",
    "budget": "500000.00",
    "funding_agency": "DST-SERB",
    "resource_requirements": "2 GPU workstations; 1 JRF",
    "department": "CSE",
}
MAX_BUDGET = "99999999.99"  # largest value the budget field can hold


@pytest.fixture
def api(stub_iam):
    """`api(uid)` returns a client acting as that user with their RSPC role;
    `api(uid, role=None)` acts with no RSPC role at all."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token a8")

    def as_user(uid, role="__default__"):
        role = ROLE_OF.get(uid) if role == "__default__" else role
        if role is None:
            stub_iam(make_session(user_id=uid, kind="faculty", permissions=(),
                                  modules=(), roles=(), active_role=None))
        else:
            stub_iam(make_session(user_id=uid, kind="faculty",
                                  permissions=ROLE_GRANTS[role], modules=("rspc",),
                                  roles=(role,), active_role=role))
        return client

    return as_user


# -- workflow helpers (each is one RSPC API call) -----------------------------
def submit(api, uid=F1, **overrides):
    return api(uid).post(BASE, {**VALID, **overrides}, format="json")


def submit_id(api, uid=F1, **overrides):
    r = submit(api, uid, **overrides)
    assert r.status_code == 201, r.content
    return r.json()["id"]


def act(api, uid, pid, step, outcome, remarks=""):
    return api(uid).post(f"{BASE}{pid}/{step}/", {"outcome": outcome, "remarks": remarks},
                         format="json")


def recommend(api, pid, outcome="recommended", remarks=""):
    return act(api, HOD, pid, "recommend", outcome, remarks)


def verify(api, pid, outcome="eligible", remarks=""):
    return act(api, ADMIN, pid, "verify", outcome, remarks)


def decide(api, pid, outcome, remarks="", uid=DEAN):
    return act(api, uid, pid, "decide", outcome, remarks)


def authorize(api, pid, outcome="approve", remarks=""):
    return act(api, DIRECTOR, pid, "authorize", outcome, remarks)


def ok(r):
    assert r.status_code == 200, r.content
    return r


def to_admin_stage(api, **overrides):
    pid = submit_id(api, **overrides)
    ok(recommend(api, pid))
    return pid


def to_dean_stage(api, **overrides):
    pid = to_admin_stage(api, **overrides)
    ok(verify(api, pid))
    return pid


def to_director_stage(api, **overrides):
    pid = to_dean_stage(api, **overrides)
    ok(decide(api, pid, "forward"))
    return pid


def mine(api, uid=F1):
    r = api(uid).get(f"{BASE}mine/")
    assert r.status_code == 200, r.content
    return {p["id"]: p for p in r.json()}


def queue_ids(api, uid):
    r = api(uid).get(f"{BASE}queue/")
    assert r.status_code == 200, r.content
    return {p["id"] for p in r.json()}


def status_of(pid):
    return ResearchProposal.objects.get(pk=pid).status


def rspc_routes():
    """(route string, view class) for every RSPC API endpoint."""
    out = []

    def walk(patterns, prefix=""):
        for p in patterns:
            if isinstance(p, URLResolver):
                walk(p.url_patterns, prefix + str(p.pattern))
            elif isinstance(p, URLPattern):
                out.append((prefix + str(p.pattern), p.callback.view_class))

    walk(rspc_urls.urlpatterns)
    return out


def skip_na(reason):
    return pytest.mark.skip(reason=f"NOT_AUTOMATED: {reason}")


NO_CONSULTANCY = "RSPC exposes no consultancy interface (only the research-proposal workflow exists)"
NO_STAFF = "RSPC exposes no staff-appointment/selection interface"
NO_FINANCE = "RSPC exposes no fund/expenditure/financial-request or transaction-record interface"
NO_PROCUREMENT = "RSPC exposes no procurement interface"
NO_REPORTS = "RSPC exposes no progress/utilization report or reporting-schedule interface"
NO_CLOSURE = "RSPC exposes no project closure/completion/archival interface"
NO_NOTIFY = "RSPC exposes no notification interface and the platform has no shared notification service"
NO_INTEGRATION = "RSPC exposes no integration or funding-agency tracking interface"


# == RSPC-CFR-001 Faculty access to own project information ===================
def test_fr_001_faculty_views_own_ongoing_and_completed_projects(api):
    """FR-001 | RSPC-CFR-001; RSPC-FR-004

    The implementation has no separate 'completed' state; the completed project
    is the one whose workflow has ended (final approval)."""
    ongoing = submit_id(api)
    completed = to_dean_stage(api)
    ok(decide(api, completed, "approve"))
    assert {ongoing, completed} <= set(mine(api, F1))


def test_fr_002_faculty_views_current_status_of_own_project(api):
    """FR-002 | RSPC-CFR-001; RSPC-FR-107"""
    pid = to_admin_stage(api)
    assert mine(api, F1)[pid]["status"] == status_of(pid) == "dept_recommended"


def test_fr_003_faculty_views_history_of_own_project(api):
    """FR-003 | RSPC-CFR-001; RSPC-FR-108"""
    pid = to_dean_stage(api)
    history = mine(api, F1)[pid]["decisions"]
    assert {(d["stage"], d["outcome"]) for d in history} == {
        ("HoD", "recommended"), ("RSPC Admin", "eligible")}


def test_fr_004_faculty_views_approval_history_of_own_project(api):
    """FR-004 | RSPC-CFR-001; RSPC-FR-005"""
    pid = submit_id(api)
    ok(recommend(api, pid, remarks="Fits department plan"))
    decisions = mine(api, F1)[pid]["decisions"]
    assert len(decisions) == 1
    assert decisions[0]["stage"] == "HoD"
    assert decisions[0]["outcome"] == "recommended"


def test_fr_005_faculty_views_audit_trail_of_own_project(api):
    """FR-005 | RSPC-CFR-001; RSPC-FR-109"""
    pid = to_dean_stage(api)
    trail = mine(api, F1)[pid]["decisions"]
    assert {(d["stage"], d["actor_id"]) for d in trail} == {("HoD", HOD), ("RSPC Admin", ADMIN)}
    assert all(d["decided_at"] for d in trail)


@skip_na(NO_FINANCE)
def test_fr_006_faculty_views_financial_transaction_records():
    """FR-006 | RSPC-CFR-001; RSPC-FR-006"""


def test_fr_007_faculty_cannot_see_another_faculty_members_projects(api):
    """FR-007 | RSPC-CFR-001; RSPC-FR-004; RSPC-FR-005; RSPC-FR-006; RSPC-FR-107; RSPC-FR-108; RSPC-FR-109

    The only read interfaces are the own-proposal list (which carries status and
    decision history) and the review queue; both are exercised as F2."""
    pid = to_admin_stage(api)
    assert pid not in mine(api, F2)
    assert api(F2).get(f"{BASE}queue/").status_code == 403


# == RSPC-CFR-002 Audit and compliance recordkeeping ==========================
@skip_na("RSPC exposes no interface for RSPC Admin to create/update audit or compliance records")
def test_fr_008_admin_maintains_audit_compliance_records():
    """FR-008 | RSPC-CFR-002; RSPC-FR-007"""


def test_fr_009_rspc_logs_submission_and_review_actions(api):
    """FR-009 | RSPC-CFR-002; RSPC-FR-088

    The proposal's decision records are the only RSPC log; they are read back
    by the authorized owner."""
    pid = submit_id(api)
    ok(recommend(api, pid, remarks="ok"))
    log = mine(api, F1)[pid]["decisions"]
    assert all(e["decided_at"] for e in log)
    logged_actors = {e["actor_id"] for e in log}
    assert F1 in logged_actors, "no log entry for the submission action"
    assert HOD in logged_actors, "no log entry for the review decision"


# == RSPC-CFR-003 Departmental review =========================================
def test_fr_010_hod_reviews_and_evaluates_feasibility_and_alignment(api):
    """FR-010 | RSPC-CFR-003; RSPC-FR-008; RSPC-FR-118; RSPC-FR-119"""
    pid = submit_id(api)
    assert pid in queue_ids(api, HOD)
    evaluation = ("Feasibility: feasible with existing lab capacity. "
                  "Alignment: aligned with the department AI thrust.")
    ok(recommend(api, pid, remarks=evaluation))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="HoD")
    assert "Feasibility: feasible" in d.remarks
    assert "Alignment: aligned" in d.remarks


def test_fr_011_hod_recommendation_recorded_and_moves_to_admin(api):
    """FR-011 | RSPC-CFR-003; RSPC-FR-009"""
    pid = submit_id(api)
    ok(recommend(api, pid, "recommended", "Strong departmental fit"))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="HoD")
    assert (d.outcome, d.remarks, d.actor_id) == ("recommended", "Strong departmental fit", HOD)
    assert status_of(pid) == "dept_recommended"
    assert pid in queue_ids(api, ADMIN)


@skip_na(NO_CONSULTANCY)
def test_fr_012_hod_reviews_consultancy_request():
    """FR-012 | RSPC-CFR-003; RSPC-FR-008; RSPC-FR-009; RSPC-FR-118; RSPC-FR-119"""


def test_fr_013_not_recommended_proposal_does_not_reach_admin(api):
    """FR-013 | RSPC-CFR-003; RSPC-FR-009"""
    pid = submit_id(api)
    ok(recommend(api, pid, "not_recommended", "Outside department focus"))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="HoD")
    assert (d.outcome, d.remarks) == ("not_recommended", "Outside department focus")
    assert status_of(pid) != "dept_recommended"
    assert pid not in queue_ids(api, ADMIN)


# == RSPC-CFR-004 Dean-RSPC ===================================================
def test_fr_014_dean_reviews_and_approves_proposal(api):
    """FR-014 | RSPC-CFR-004; RSPC-FR-010; RSPC-FR-011; RSPC-FR-126"""
    pid = to_dean_stage(api)
    assert pid in queue_ids(api, DEAN)
    ok(decide(api, pid, "approve", "Approved within Dean limits"))
    assert status_of(pid) == "approved"
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="Dean-RSPC")
    assert (d.outcome, d.remarks, d.actor_id) == ("approve", "Approved within Dean limits", DEAN)


@skip_na(NO_CONSULTANCY)
def test_fr_015_dean_reviews_consultancy_matter():
    """FR-015 | RSPC-CFR-004; RSPC-FR-010"""


def test_fr_016_dean_forwards_high_value_request_to_director(api):
    """FR-016 | RSPC-CFR-004; RSPC-FR-012"""
    pid = to_dean_stage(api, budget=MAX_BUDGET)
    ok(decide(api, pid, "forward", "High value; Director approval needed"))
    assert status_of(pid) == "forwarded_to_director"
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="Dean-RSPC")
    assert d.outcome == "forward"
    assert pid in queue_ids(api, DIRECTOR)


@skip_na(NO_STAFF)
def test_fr_017_dean_reviews_staff_appointment_request():
    """FR-017 | RSPC-CFR-004; RSPC-FR-120"""


@skip_na("RSPC exposes no budget-allocation entity or Dean review interface for it")
def test_fr_018_dean_reviews_budget_allocation():
    """FR-018 | RSPC-CFR-004; RSPC-FR-121"""


@skip_na(NO_FINANCE)
def test_fr_019_dean_reviews_financial_request():
    """FR-019 | RSPC-CFR-004; RSPC-FR-122"""


@skip_na(NO_PROCUREMENT)
def test_fr_020_dean_reviews_procurement_request():
    """FR-020 | RSPC-CFR-004; RSPC-FR-123"""


@skip_na(NO_CLOSURE)
def test_fr_021_dean_reviews_closure_record():
    """FR-021 | RSPC-CFR-004; RSPC-FR-124"""


def test_fr_022_dean_records_compliance_review(api):
    """FR-022 | RSPC-CFR-004; RSPC-FR-125

    The Dean's decision remarks are the only place a review outcome is stored."""
    pid = to_dean_stage(api)
    review = "Compliance review: compliant with DST-SERB and institute norms"
    ok(decide(api, pid, "approve", review))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="Dean-RSPC")
    assert d.remarks == review


def test_fr_023_dean_cannot_finally_approve_beyond_limit(api):
    """FR-023 | RSPC-CFR-004; RSPC-FR-126

    No limit value is defined anywhere, so the largest budget the system can
    hold is used as the over-limit proposal."""
    pid = to_dean_stage(api, budget=MAX_BUDGET)
    decide(api, pid, "approve", "Attempted final approval")
    assert status_of(pid) != "approved"


# == RSPC-CFR-005 Director ====================================================
def test_fr_024_director_reviews_and_approves_routed_request(api):
    """FR-024 | RSPC-CFR-005; RSPC-FR-127"""
    pid = to_director_stage(api)
    assert pid in queue_ids(api, DIRECTOR)
    ok(authorize(api, pid, "approve", "Approved by Director"))
    assert status_of(pid) == "approved"
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="Director")
    assert (d.outcome, d.remarks, d.actor_id) == ("approve", "Approved by Director", DIRECTOR)


def test_fr_025_director_approves_large_funding_request(api):
    """FR-025 | RSPC-CFR-005; RSPC-FR-013

    The large funding request is a research proposal with the largest budget."""
    pid = to_director_stage(api, budget=MAX_BUDGET)
    ok(authorize(api, pid, "approve"))
    assert status_of(pid) == "approved"
    assert ResearchProposal.objects.get(pk=pid).decisions.filter(
        stage="Director", outcome="approve").exists()


@skip_na(NO_FINANCE)
def test_fr_026_director_authorizes_high_value_expenditure():
    """FR-026 | RSPC-CFR-005; RSPC-FR-014"""


def test_fr_027_director_records_regulation_adherence_review(api):
    """FR-027 | RSPC-CFR-005; RSPC-FR-128"""
    pid = to_director_stage(api)
    review = "Regulation adherence: meets institute and DST-SERB regulations"
    ok(authorize(api, pid, "approve", review))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="Director")
    assert d.remarks == review


# == RSPC-CFR-006/007/008 Proposal submission, routing, decisions =============
def test_fr_028_faculty_submits_proposal_with_all_core_data(api):
    """FR-028 | RSPC-CFR-006; RSPC-FR-015; RSPC-FR-016; RSPC-FR-017; RSPC-FR-018; RSPC-FR-019; RSPC-FR-020"""
    r = submit(api)
    assert r.status_code == 201, r.content
    got = mine(api, F1)[r.json()["id"]]
    assert got["pi_id"] == F1
    for field in ("objectives", "start_date", "end_date", "budget", "funding_agency",
                  "resource_requirements"):
        assert got[field] == VALID[field], field


def test_fr_029_valid_proposal_routed_to_hod(api):
    """FR-029 | RSPC-CFR-007; RSPC-FR-021"""
    pid = submit_id(api)
    assert status_of(pid) == "submitted"
    assert pid in queue_ids(api, HOD)


def test_fr_030_proposal_routed_hod_admin_dean_director_in_order(api):
    """FR-030 | RSPC-CFR-007; RSPC-FR-021"""
    pid = submit_id(api)
    ok(recommend(api, pid))
    assert status_of(pid) == "dept_recommended"
    ok(verify(api, pid))
    assert status_of(pid) == "admin_verified"
    ok(decide(api, pid, "forward"))
    assert status_of(pid) == "forwarded_to_director"
    ok(authorize(api, pid, "approve"))
    assert status_of(pid) == "approved"
    stages = list(ResearchProposal.objects.get(pk=pid).decisions
                  .order_by("decided_at", "id").values_list("stage", flat=True))
    assert stages == ["HoD", "RSPC Admin", "Dean-RSPC", "Director"]


def test_fr_031_later_stage_cannot_act_before_hod(api):
    """FR-031 | RSPC-CFR-007; RSPC-FR-021"""
    pid = submit_id(api)
    assert decide(api, pid, "approve").status_code >= 400
    assert verify(api, pid).status_code >= 400
    assert status_of(pid) == "submitted"


def test_fr_032_proposal_with_empty_mandatory_fields_rejected(api):
    """FR-032 | RSPC-CFR-007; RSPC-FR-022"""
    empty = {k: "" for k in VALID}
    r = api(F1).post(BASE, empty, format="json")
    assert r.status_code == 400
    assert not ResearchProposal.objects.exists()


def test_fr_033_proposal_violating_policy_validation_rejected(api):
    """FR-033 | RSPC-CFR-007; RSPC-FR-023

    Represented policy validation used: the budget must be greater than zero."""
    r = submit(api, budget="0")
    assert r.status_code == 400
    assert not ResearchProposal.objects.exists()


def test_fr_034_decision_recorded_with_timestamp_and_remarks(api):
    """FR-034 | RSPC-CFR-008; RSPC-FR-024; RSPC-FR-025"""
    pid = submit_id(api)
    ok(recommend(api, pid, remarks="Recommended with minor budget notes"))
    d = mine(api, F1)[pid]["decisions"][0]
    assert d["decided_at"]
    assert d["remarks"] == "Recommended with minor budget notes"


# == RSPC-CFR-009..011 Consultancy ============================================
@skip_na(NO_CONSULTANCY)
def test_fr_035_faculty_registers_consultancy():
    """FR-035 | RSPC-CFR-009; RSPC-FR-027; RSPC-FR-028; RSPC-FR-029; RSPC-FR-030; RSPC-FR-031; RSPC-FR-032"""


@skip_na(NO_CONSULTANCY)
def test_fr_036_consultancy_routed_by_approval_path():
    """FR-036 | RSPC-CFR-010; RSPC-FR-033"""


@skip_na(NO_CONSULTANCY)
def test_fr_037_consultancy_payments_settlements_financial_history():
    """FR-037 | RSPC-CFR-011; RSPC-FR-034; RSPC-FR-036; RSPC-FR-037"""


@skip_na(NO_CONSULTANCY)
def test_fr_038_consultancy_deliverables_tracked():
    """FR-038 | RSPC-CFR-011; RSPC-FR-035"""


@skip_na(NO_CONSULTANCY)
def test_fr_039_consultancy_approval_history():
    """FR-039 | RSPC-CFR-011; RSPC-FR-038"""


@skip_na(NO_CONSULTANCY)
def test_fr_040_consultancy_history_only_for_authorized_users():
    """FR-040 | RSPC-CFR-011; RSPC-FR-037; RSPC-FR-038"""


# == RSPC-CFR-012..014 Staff appointments =====================================
@skip_na(NO_STAFF)
def test_fr_041_faculty_requests_staff_appointment():
    """FR-041 | RSPC-CFR-012; RSPC-FR-039"""


@skip_na(NO_STAFF)
def test_fr_042_admin_manages_advertisement_and_application_records():
    """FR-042 | RSPC-CFR-012; RSPC-FR-040; RSPC-FR-041"""


@skip_na(NO_STAFF)
def test_fr_043_admin_manages_stipend_structure_and_workflow_records():
    """FR-043 | RSPC-CFR-012; RSPC-FR-042; RSPC-FR-131"""


@skip_na(NO_STAFF)
def test_fr_044_appointment_duration_records():
    """FR-044 | RSPC-CFR-012; RSPC-FR-046"""


@skip_na(NO_STAFF)
def test_fr_045_appointment_payment_records():
    """FR-045 | RSPC-CFR-012; RSPC-FR-047"""


@skip_na(NO_STAFF)
def test_fr_046_appointment_compliance_records():
    """FR-046 | RSPC-CFR-012; RSPC-FR-048"""


@skip_na(NO_STAFF)
def test_fr_047_admin_maintains_selection_records():
    """FR-047 | RSPC-CFR-012; RSPC-FR-129"""


@skip_na(NO_STAFF)
def test_fr_048_faculty_records_selection_participation():
    """FR-048 | RSPC-CFR-013; RSPC-FR-043"""


@skip_na(NO_STAFF)
def test_fr_049_faculty_submits_selection_recommendation():
    """FR-049 | RSPC-CFR-013; RSPC-FR-044"""


@skip_na(NO_STAFF)
def test_fr_050_staff_appointment_routed_dean_then_director():
    """FR-050 | RSPC-CFR-014; RSPC-FR-045"""


# == RSPC-CFR-015/016 Finance =================================================
@skip_na(NO_FINANCE)
def test_fr_051_faculty_submits_fund_utilization_request():
    """FR-051 | RSPC-CFR-015; RSPC-FR-049"""


@skip_na(NO_FINANCE)
def test_fr_052_faculty_submits_expenditure_request():
    """FR-052 | RSPC-CFR-015; RSPC-FR-050"""


@skip_na(NO_FINANCE)
def test_fr_053_admin_verifies_fund_request():
    """FR-053 | RSPC-CFR-015; RSPC-FR-051"""


@skip_na(NO_FINANCE)
def test_fr_054_admin_verifies_expenditure_request():
    """FR-054 | RSPC-CFR-015; RSPC-FR-052"""


@skip_na(NO_FINANCE)
def test_fr_055_dean_approves_financial_request_within_powers():
    """FR-055 | RSPC-CFR-016; RSPC-FR-053"""


@skip_na(NO_FINANCE)
def test_fr_056_high_value_financial_request_escalated_to_director():
    """FR-056 | RSPC-CFR-016; RSPC-FR-054"""


@skip_na(NO_FINANCE)
def test_fr_057_financial_lifecycle_logged():
    """FR-057 | RSPC-CFR-016; RSPC-FR-055"""


# == RSPC-CFR-017 Procurement =================================================
@skip_na(NO_PROCUREMENT)
def test_fr_058_faculty_requests_equipment_procurement():
    """FR-058 | RSPC-CFR-017; RSPC-FR-056"""


@skip_na(NO_PROCUREMENT)
def test_fr_059_faculty_requests_consumables_procurement():
    """FR-059 | RSPC-CFR-017; RSPC-FR-057"""


@skip_na(NO_PROCUREMENT)
def test_fr_060_procurement_within_budget_accepted():
    """FR-060 | RSPC-CFR-017; RSPC-FR-058"""


@skip_na(NO_PROCUREMENT)
def test_fr_061_procurement_over_budget_rejected():
    """FR-061 | RSPC-CFR-017; RSPC-FR-058"""


@skip_na(NO_PROCUREMENT)
def test_fr_062_procurement_hierarchy_enforced():
    """FR-062 | RSPC-CFR-017; RSPC-FR-059"""


@skip_na(NO_PROCUREMENT)
def test_fr_063_faculty_tracks_procurement_status():
    """FR-063 | RSPC-CFR-017; RSPC-FR-060"""


# == RSPC-CFR-018/019 Reporting ===============================================
@skip_na(NO_REPORTS)
def test_fr_064_faculty_submits_progress_report():
    """FR-064 | RSPC-CFR-018; RSPC-FR-061"""


@skip_na(NO_REPORTS)
def test_fr_065_faculty_submits_utilization_report():
    """FR-065 | RSPC-CFR-018; RSPC-FR-062"""


@skip_na(NO_REPORTS)
def test_fr_066_reporting_schedule_enforced():
    """FR-066 | RSPC-CFR-018; RSPC-FR-063"""


@skip_na(NO_REPORTS)
def test_fr_067_historical_reports_accessible():
    """FR-067 | RSPC-CFR-019; RSPC-FR-066; RSPC-FR-067"""


@skip_na(NO_REPORTS)
def test_fr_068_historical_reports_only_for_authorized():
    """FR-068 | RSPC-CFR-019; RSPC-FR-066; RSPC-FR-067"""


# == RSPC-CFR-020 Closure =====================================================
@skip_na(NO_CLOSURE)
def test_fr_069_faculty_submits_closure_report():
    """FR-069 | RSPC-CFR-020; RSPC-FR-068"""


@skip_na(NO_CLOSURE)
def test_fr_070_faculty_submits_completion_report():
    """FR-070 | RSPC-CFR-020; RSPC-FR-069"""


@skip_na(NO_CLOSURE)
def test_fr_071_financial_settlement_verification():
    """FR-071 | RSPC-CFR-020; RSPC-FR-070"""


@skip_na(NO_CLOSURE)
def test_fr_072_asset_declaration_verification():
    """FR-072 | RSPC-CFR-020; RSPC-FR-071"""


@skip_na(NO_CLOSURE)
def test_fr_073_closure_approval_and_remarks_recorded():
    """FR-073 | RSPC-CFR-020; RSPC-FR-072; RSPC-FR-130"""


@skip_na(NO_CLOSURE)
def test_fr_074_closed_project_archived_with_audit_trail():
    """FR-074 | RSPC-CFR-020; RSPC-FR-073"""


# == RSPC-CFR-021 Notifications ===============================================
@skip_na(NO_NOTIFY)
def test_fr_075_submission_notification():
    """FR-075 | RSPC-CFR-021; RSPC-FR-074"""


@skip_na(NO_NOTIFY)
def test_fr_076_review_stage_notification():
    """FR-076 | RSPC-CFR-021; RSPC-FR-026"""


@skip_na(NO_NOTIFY)
def test_fr_077_approval_notification():
    """FR-077 | RSPC-CFR-021; RSPC-FR-075"""


@skip_na(NO_NOTIFY)
def test_fr_078_rejection_notification():
    """FR-078 | RSPC-CFR-021; RSPC-FR-132"""


@skip_na(NO_NOTIFY)
def test_fr_079_pending_action_notification():
    """FR-079 | RSPC-CFR-021; RSPC-FR-076"""


@skip_na(NO_NOTIFY)
def test_fr_080_escalation_notification():
    """FR-080 | RSPC-CFR-021; RSPC-FR-077"""


@skip_na(NO_NOTIFY)
def test_fr_081_reporting_deadline_notification():
    """FR-081 | RSPC-CFR-021; RSPC-FR-078"""


@skip_na(NO_NOTIFY)
def test_fr_082_pending_report_reminders():
    """FR-082 | RSPC-CFR-021; RSPC-FR-064; RSPC-FR-065"""


@skip_na(NO_NOTIFY)
def test_fr_083_financial_approval_notification():
    """FR-083 | RSPC-CFR-021; RSPC-FR-079"""


@skip_na(NO_NOTIFY)
def test_fr_084_compliance_requirement_notification():
    """FR-084 | RSPC-CFR-021; RSPC-FR-080"""


@skip_na(NO_NOTIFY)
def test_fr_085_dashboard_delivery():
    """FR-085 | RSPC-CFR-021; RSPC-FR-081"""


@skip_na(NO_NOTIFY)
def test_fr_086_email_notification_triggered():
    """FR-086 | RSPC-CFR-021; RSPC-FR-082"""


@skip_na(NO_NOTIFY + "; the hand-off to a platform mechanism cannot be observed")
def test_fr_087_notification_infrastructure_external():
    """FR-087 | RSPC-CFR-021; RSPC-FR-099"""


# == RSPC-CFR-022 Integration =================================================
@skip_na(NO_INTEGRATION)
def test_fr_088_fusion_module_integration():
    """FR-088 | RSPC-CFR-022; RSPC-FR-083"""


@skip_na(NO_INTEGRATION)
def test_fr_089_agency_submission_tracking_recorded():
    """FR-089 | RSPC-CFR-022; RSPC-FR-084"""


@skip_na(NO_INTEGRATION)
def test_fr_090_agency_disbursement_tracking_recorded():
    """FR-090 | RSPC-CFR-022; RSPC-FR-085"""


def test_fr_091_rspc_has_no_external_agency_execution_operation():
    """FR-091 | RSPC-CFR-022; RSPC-FR-100"""
    for route, view in rspc_routes():
        text = f"{route} {view.__name__}".lower()
        for word in ("agency", "disburs", "sanction", "remit"):
            assert word not in text, (route, view.__name__)


# == RSPC-CFR-023/024 Role-based access =======================================
def test_fr_092_user_without_rspc_role_gets_no_project_data(api):
    """FR-092 | RSPC-CFR-023; RSPC-FR-086"""
    submit_id(api)
    outsider = api(OUTSIDER, role=None)
    for url in (f"{BASE}mine/", f"{BASE}queue/"):
        r = outsider.get(url)
        assert r.status_code == 403, url
        assert "title" not in r.content.decode()


def test_fr_093_faculty_cannot_perform_dean_approval(api):
    """FR-093 | RSPC-CFR-023; RSPC-FR-087"""
    pid = to_dean_stage(api)
    assert decide(api, pid, "approve", uid=F1).status_code == 403
    assert status_of(pid) == "admin_verified"


def test_fr_094_rspc_has_no_auth_or_rbac_administration(api):
    """FR-094 | RSPC-CFR-023; RSPC-FR-101"""
    routes = rspc_routes()
    assert routes
    for route, view in routes:
        text = f"{route} {view.__name__}".lower()
        for word in ("login", "logout", "password", "token", "role", "permission", "grant"):
            assert word not in text, (route, view.__name__)
        perms = view.permission_classes
        assert any(issubclass(p, _HasModuleGrant) for p in perms), view.__name__
        assert any(issubclass(p, _HasPermission) for p in perms), view.__name__


def test_fr_095_role_assignment_takes_effect_immediately(api):
    """FR-095 | RSPC-CFR-024; RSPC-FR-091; RSPC-FR-093

    The role-management mechanism is the IAM; its session is what assigns roles."""
    assert api(OUTSIDER, role=None).post(BASE, VALID, format="json").status_code == 403
    assert api(OUTSIDER, role="Faculty").post(BASE, VALID, format="json").status_code == 201


def test_fr_096_role_reassignment_takes_effect_immediately(api):
    """FR-096 | RSPC-CFR-024; RSPC-FR-092; RSPC-FR-093"""
    assert api(OUTSIDER, role="Faculty").post(BASE, VALID, format="json").status_code == 201
    as_hod = api(OUTSIDER, role="HoD")
    assert as_hod.post(BASE, VALID, format="json").status_code == 403
    assert as_hod.get(f"{BASE}queue/").status_code == 200


@skip_na("RSPC exposes no role-change log; role changes are only visible as the IAM session")
def test_fr_097_role_changes_logged():
    """FR-097 | RSPC-CFR-024; RSPC-FR-094; RSPC-FR-095"""


# == RSPC-CFR-025..027 Scope boundaries =======================================
@skip_na(NO_STAFF + "; the precondition (an appointment with payment records) cannot be created")
def test_fr_098_no_hr_payroll_processing():
    """FR-098 | RSPC-CFR-025; RSPC-FR-096"""


@skip_na(NO_FINANCE + "; the precondition (an approved financial request) cannot be created")
def test_fr_099_no_payment_execution():
    """FR-099 | RSPC-CFR-026; RSPC-FR-097"""


@skip_na(NO_PROCUREMENT + "; the precondition (an approved procurement request) cannot be created")
def test_fr_100_no_procurement_execution():
    """FR-100 | RSPC-CFR-027; RSPC-FR-098"""


# == RSPC-CFR-028 Lifecycle-permitted updates =================================
@skip_na("RSPC exposes no interface to update project details, milestones, progress or utilization")
def test_fr_101_faculty_updates_project_where_permitted():
    """FR-101 | RSPC-CFR-028; RSPC-FR-103; RSPC-FR-104; RSPC-FR-105; RSPC-FR-106"""


@skip_na("RSPC exposes no update interface and no closed/archived project state")
def test_fr_102_update_refused_where_lifecycle_forbids():
    """FR-102 | RSPC-CFR-028; RSPC-FR-103; RSPC-FR-104; RSPC-FR-105; RSPC-FR-106"""


# == RSPC-CFR-029 RSPC Admin verification and forwarding ======================
def test_fr_103_admin_verifies_proposal_completeness(api):
    """FR-103 | RSPC-CFR-029; RSPC-FR-110"""
    pid = to_admin_stage(api)
    assert pid in queue_ids(api, ADMIN)
    ok(verify(api, pid, "eligible", "Completeness: all mandatory sections present"))
    d = ResearchProposal.objects.get(pk=pid).decisions.get(stage="RSPC Admin")
    assert (d.outcome, d.remarks) == ("eligible", "Completeness: all mandatory sections present")


@skip_na(NO_CONSULTANCY)
def test_fr_104_admin_verifies_consultancy_completeness():
    """FR-104 | RSPC-CFR-029; RSPC-FR-111"""


@skip_na(NO_STAFF)
def test_fr_105_admin_verifies_staff_request_completeness():
    """FR-105 | RSPC-CFR-029; RSPC-FR-112"""


@skip_na(NO_FINANCE)
def test_fr_106_admin_verifies_fund_and_expenditure_completeness():
    """FR-106 | RSPC-CFR-029; RSPC-FR-113"""


@skip_na(NO_PROCUREMENT)
def test_fr_107_admin_verifies_procurement_completeness():
    """FR-107 | RSPC-CFR-029; RSPC-FR-114"""


@skip_na(NO_CLOSURE)
def test_fr_108_admin_verifies_closure_completeness():
    """FR-108 | RSPC-CFR-029; RSPC-FR-115"""


def test_fr_109_admin_records_requirements_check(api):
    """FR-109 | RSPC-CFR-029; RSPC-FR-116"""
    pid = to_admin_stage(api)
    check = "Requirements check: meets DST-SERB and institute requirements"
    ok(verify(api, pid, "eligible", check))
    admin = [d for d in mine(api, F1)[pid]["decisions"] if d["stage"] == "RSPC Admin"]
    assert [d["remarks"] for d in admin] == [check]


def test_fr_110_admin_forwards_eligible_proposal_to_dean(api):
    """FR-110 | RSPC-CFR-029; RSPC-FR-117"""
    pid = to_admin_stage(api)
    ok(verify(api, pid, "eligible"))
    assert status_of(pid) == "admin_verified"
    assert pid in queue_ids(api, DEAN)
    assert ResearchProposal.objects.get(pk=pid).decisions.filter(stage="RSPC Admin").exists()


def test_fr_111_ineligible_proposal_not_forwarded(api):
    """FR-111 | RSPC-CFR-029; RSPC-FR-117"""
    pid = to_admin_stage(api)
    ok(verify(api, pid, "not_eligible", "Budget justification missing"))
    assert verify(api, pid, "eligible").status_code >= 400
    assert status_of(pid) != "admin_verified"
    assert pid not in queue_ids(api, DEAN)
