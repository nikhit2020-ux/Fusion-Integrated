"""A8 — UC strategy: automated tests for the use cases that have an RSPC interface.

Generated from the frozen design a8_design/UC_DESIGN.json (Prompt B).
The only RSPC interface is the research-proposal API under /api/v1/rspc/
(submit, mine, queue, recommend, verify, decide, authorize). Identity comes
from the IAM session, replaced by the shared `stub_iam` fake (external
dependency only — the RSPC behaviour under test is not mocked).

Parts of an expected result that have no observable RSPC interface
(notification events, audit-log entries) are named in the docstring and not
asserted; everything observable is asserted as the specification states it.
"""
import pytest
from rest_framework.test import APIClient

from conftest import make_session
from modules.rspc.models import ProposalDecision, ResearchProposal

pytestmark = pytest.mark.django_db

BASE = "/api/v1/rspc/proposals/"
MINE = BASE + "mine/"
QUEUE = BASE + "queue/"

FACULTY_A, FACULTY_B = 2001, 2002
HOD, ADMIN, DEAN, DIRECTOR = 3001, 3002, 3003, 3004

ROLE_PERMS = {
    "Faculty": ("rspc.proposal.submit", "rspc.proposal.view_self"),
    "HoD": ("rspc.proposal.recommend", "rspc.proposal.view_queue"),
    "RSPC Admin": ("rspc.proposal.verify", "rspc.proposal.view_queue"),
    "Dean-RSPC": ("rspc.proposal.decide", "rspc.proposal.view_queue"),
    "Director": ("rspc.proposal.authorize", "rspc.proposal.view_queue"),
}


def as_role(stub_iam, role, uid, perms=None):
    """Authenticate the next requests as `uid` holding `role`'s RSPC grants."""
    stub_iam(make_session(user_id=uid, kind="faculty", modules=("rspc",),
                          roles=(role,), active_role=role,
                          permissions=ROLE_PERMS[role] if perms is None else perms))
    c = APIClient()
    c.credentials(HTTP_AUTHORIZATION="Token t")
    return c


def payload(**over):
    data = {
        "title": "Edge AI for crop monitoring",
        "objectives": "Build and evaluate a low-power crop-disease classifier.",
        "start_date": "2027-01-01",
        "end_date": "2028-12-31",
        "budget": "500000.00",
        "funding_agency": "DST-SERB",
        "resource_requirements": "2 GPUs, 1 JRF",
        "department": "CSE",
    }
    data.update(over)
    return {k: v for k, v in data.items() if v is not None}


def proposal(status="submitted", pi=FACULTY_A, **over):
    fields = dict(title="P", objectives="O", start_date="2027-01-01",
                  end_date="2028-01-01", budget="100000.00", funding_agency="DST",
                  resource_requirements="R", department="CSE")
    fields.update(over)
    return ResearchProposal.objects.create(pi_id=pi, status=status, **fields)


def ids(resp):
    return {row["id"] for row in resp.json()}


def act(client, pid, action, outcome, remarks="ok"):
    return client.post(f"{BASE}{pid}/{action}/", {"outcome": outcome, "remarks": remarks},
                       format="json")


def is_rejected_state_error(resp):
    return 400 <= resp.status_code < 500 and resp.status_code not in (401, 403)


# --------------------------------------------------------------------- UC-001
def test_UC_001_main_flow(stub_iam):
    """UC-001 | RSPC-UC-001 Main Flow — Faculty views own portfolio, status and histories.

    Not observable (no RSPC interface): separate audit-trail and financial
    transaction records; approval history (decisions with timestamps) and the
    represented financial field (budget) are asserted.
    """
    ongoing = proposal("submitted")
    completed = proposal("approved")
    ProposalDecision.objects.create(proposal=completed, stage="Dean-RSPC", actor_id=DEAN,
                                    outcome="approve", remarks="fine")
    before = {p.pk: p.status for p in ResearchProposal.objects.all()}

    resp = as_role(stub_iam, "Faculty", FACULTY_A).get(MINE)

    assert resp.status_code == 200
    rows = {r["id"]: r for r in resp.json()}
    assert set(rows) == {ongoing.pk, completed.pk}
    sel = rows[completed.pk]
    assert sel["status"] == "approved"
    assert "budget" in sel
    assert len(sel["decisions"]) == 1
    assert sel["decisions"][0]["decided_at"]
    assert {p.pk: p.status for p in ResearchProposal.objects.all()} == before


def test_UC_002_alternative_A1(stub_iam):
    """UC-002 | RSPC-UC-001 Alternative A1 — view refreshes within the same authorized scope."""
    p1, p2 = proposal(pi=FACULTY_A), proposal("approved", pi=FACULTY_A)
    other = proposal(pi=FACULTY_B)
    c = as_role(stub_iam, "Faculty", FACULTY_A)

    first = c.get(MINE)
    second = c.get(MINE)

    assert first.status_code == second.status_code == 200
    rows = {r["id"]: r for r in second.json()}
    assert p2.pk in rows and rows[p2.pk]["status"] == "approved"
    assert ids(second) == {p1.pk, p2.pk}
    assert other.pk not in ids(first)
    assert ResearchProposal.objects.get(pk=p2.pk).status == "approved"


def test_UC_003_exception_E1(stub_iam):
    """UC-003 | RSPC-UC-001 Exception E1 — project outside the Faculty member's scope is denied."""
    foreign = proposal(pi=FACULTY_B)

    resp = as_role(stub_iam, "Faculty", FACULTY_A).get(MINE)

    assert resp.status_code == 200
    assert foreign.pk not in ids(resp)
    assert ResearchProposal.objects.get(pk=foreign.pk).status == "submitted"


# --------------------------------------------------------------------- UC-002
def test_UC_005_main_flow(stub_iam):
    """UC-005 | RSPC-UC-002 Main Flow — valid proposal is Submitted and routed to HoD review.

    Not observable (no RSPC interface): the proposal-submission notification event.
    """
    resp = as_role(stub_iam, "Faculty", FACULTY_A).post(BASE, payload(), format="json")

    assert resp.status_code == 201
    pid = resp.json()["id"]
    assert ResearchProposal.objects.get(pk=pid).status == "submitted"
    queue = as_role(stub_iam, "HoD", HOD).get(QUEUE)
    assert queue.status_code == 200
    assert pid in ids(queue)


def test_UC_006_alternative_A1(stub_iam):
    """UC-006 | RSPC-UC-002 Alternative A1 — Faculty saves and revises a draft before submission."""
    c = as_role(stub_iam, "Faculty", FACULTY_A)

    resp = c.post(BASE, payload(status="draft"), format="json")

    assert resp.status_code in (200, 201)
    pid = resp.json()["id"]
    assert ResearchProposal.objects.get(pk=pid).status == "draft"
    queue = as_role(stub_iam, "HoD", HOD).get(QUEUE)
    assert pid not in ids(queue)

    c = as_role(stub_iam, "Faculty", FACULTY_A)
    rev = c.patch(f"{BASE}{pid}/", {"title": "Revised title"}, format="json")
    assert rev.status_code == 200
    p = ResearchProposal.objects.get(pk=pid)
    assert p.title == "Revised title"
    assert p.status == "draft"


def test_UC_007_alternative_A2(stub_iam):
    """UC-007 | RSPC-UC-002 Alternative A2 — proposal needing correction stays unsubmitted until corrected."""
    draft = proposal("draft", budget=None)
    c = as_role(stub_iam, "Faculty", FACULTY_A)

    bad = c.post(BASE, payload(budget=None), format="json")

    assert bad.status_code == 400
    assert ResearchProposal.objects.get(pk=draft.pk).status == "draft"
    assert not ResearchProposal.objects.filter(status="submitted").exists()

    good = c.post(BASE, payload(), format="json")
    assert good.status_code == 201
    assert ResearchProposal.objects.get(pk=good.json()["id"]).status == "submitted"


def test_UC_008_exception_E1(stub_iam):
    """UC-008 | RSPC-UC-002 Exception E1 — submission blocked when a mandatory field is missing."""
    draft = proposal("draft", title="Keep me")
    before = ResearchProposal.objects.count()

    resp = as_role(stub_iam, "Faculty", FACULTY_A).post(
        BASE, payload(funding_agency=None), format="json")

    assert resp.status_code == 400
    assert ResearchProposal.objects.count() == before
    kept = ResearchProposal.objects.get(pk=draft.pk)
    assert (kept.status, kept.title) == ("draft", "Keep me")


def test_UC_009_exception_E2(stub_iam):
    """UC-009 | RSPC-UC-002 Exception E2 — unauthorized proposal submission is blocked."""
    no_grant = as_role(stub_iam, "HoD", HOD).post(BASE, payload(), format="json")
    assert no_grant.status_code == 403

    anon = APIClient().post(BASE, payload(), format="json")
    assert anon.status_code in (401, 403)

    assert ResearchProposal.objects.count() == 0


# --------------------------------------------------------------------- UC-003
def test_UC_010_main_flow_recommended(stub_iam):
    """UC-010 | RSPC-UC-003 Main Flow (recommended) — HoD recommends; request forwarded to RSPC Admin.

    Not observable (no RSPC interface): review/pending-action notification event.
    """
    p = proposal("submitted")
    hod = as_role(stub_iam, "HoD", HOD)
    assert p.pk in ids(hod.get(QUEUE))

    resp = act(hod, p.pk, "recommend", "recommended", "feasible")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "dept_recommended"
    d = ProposalDecision.objects.get(proposal=p)
    assert (d.stage, d.outcome, d.remarks, d.actor_id) == ("HoD", "recommended", "feasible", HOD)
    assert p.pk in ids(as_role(stub_iam, "RSPC Admin", ADMIN).get(QUEUE))


def test_UC_011_main_flow_not_recommended(stub_iam):
    """UC-011 | RSPC-UC-003 Main Flow (not recommended) — non-recommendation recorded, not advanced.

    Not observable (no RSPC interface): non-recommendation notification event.
    """
    p = proposal("submitted")

    resp = act(as_role(stub_iam, "HoD", HOD), p.pk, "recommend", "not_recommended", "misaligned")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "dept_not_recommended"
    d = ProposalDecision.objects.get(proposal=p)
    assert (d.outcome, d.remarks) == ("not_recommended", "misaligned")
    assert p.pk not in ids(as_role(stub_iam, "RSPC Admin", ADMIN).get(QUEUE))


def test_UC_013_exception_E1(stub_iam):
    """UC-013 | RSPC-UC-003 Exception E1 — unauthorized (Faculty) review is blocked."""
    p = proposal("submitted")

    resp = act(as_role(stub_iam, "Faculty", FACULTY_A), p.pk, "recommend", "recommended")

    assert resp.status_code == 403
    p.refresh_from_db()
    assert p.status == "submitted"
    assert not ProposalDecision.objects.filter(proposal=p).exists()


def test_UC_014_exception_E2(stub_iam):
    """UC-014 | RSPC-UC-003 Exception E2 — request not in HoD-review state cannot be acted on."""
    p = proposal("dept_recommended")

    resp = act(as_role(stub_iam, "HoD", HOD), p.pk, "recommend", "recommended")

    assert is_rejected_state_error(resp)
    p.refresh_from_db()
    assert p.status == "dept_recommended"
    assert not ProposalDecision.objects.filter(proposal=p).exists()


# --------------------------------------------------------------------- UC-004
def test_UC_015_main_flow(stub_iam):
    """UC-015 | RSPC-UC-004 Main Flow — RSPC Admin verifies and forwards to Dean-RSPC.

    Not observable (no RSPC interface): completeness/compliance display beyond the
    record itself; pending-action notification event.
    """
    p = proposal("dept_recommended")
    admin = as_role(stub_iam, "RSPC Admin", ADMIN)
    assert p.pk in ids(admin.get(QUEUE))

    resp = act(admin, p.pk, "verify", "eligible", "complete")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "admin_verified"
    d = ProposalDecision.objects.get(proposal=p)
    assert (d.stage, d.outcome, d.actor_id) == ("RSPC Admin", "eligible", ADMIN)
    assert p.pk in ids(as_role(stub_iam, "Dean-RSPC", DEAN).get(QUEUE))


def test_UC_017_exception_E1(stub_iam):
    """UC-017 | RSPC-UC-004 Exception E1 — incomplete/non-compliant request is not forwarded."""
    p = proposal("dept_recommended")

    resp = act(as_role(stub_iam, "RSPC Admin", ADMIN), p.pk, "verify", "not_eligible", "missing docs")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status not in ("admin_verified", "approved", "forwarded_to_director")
    assert ProposalDecision.objects.get(proposal=p).outcome == "not_eligible"
    assert p.pk not in ids(as_role(stub_iam, "Dean-RSPC", DEAN).get(QUEUE))


def test_UC_018_exception_E2(stub_iam):
    """UC-018 | RSPC-UC-004 Exception E2 — unauthorized verification/forwarding is blocked."""
    p = proposal("dept_recommended")

    for role, uid in (("Faculty", FACULTY_A), ("HoD", HOD)):
        resp = act(as_role(stub_iam, role, uid), p.pk, "verify", "eligible")
        assert resp.status_code == 403

    p.refresh_from_db()
    assert p.status == "dept_recommended"


# --------------------------------------------------------------------- UC-005
def test_UC_019_main_flow_approve(stub_iam):
    """UC-019 | RSPC-UC-005 Main Flow (approve within limits) — Dean-RSPC approves.

    Not observable (no RSPC interface): approval notification event.
    """
    p = proposal("admin_verified")
    ProposalDecision.objects.create(proposal=p, stage="RSPC Admin", actor_id=ADMIN,
                                    outcome="eligible")
    dean = as_role(stub_iam, "Dean-RSPC", DEAN)
    row = next(r for r in dean.get(QUEUE).json() if r["id"] == p.pk)
    assert row["decisions"]

    resp = act(dean, p.pk, "decide", "approve", "within limits")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "approved"
    d = p.decisions.get(stage="Dean-RSPC")
    assert (d.outcome, d.remarks) == ("approve", "within limits")


def test_UC_020_main_flow_forward(stub_iam):
    """UC-020 | RSPC-UC-005 Main Flow (forward to Director) — Dean-RSPC forwards to Director.

    Not observable (no RSPC interface): escalation/pending-action notification event.
    """
    p = proposal("admin_verified")

    resp = act(as_role(stub_iam, "Dean-RSPC", DEAN), p.pk, "decide", "forward", "high value")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "forwarded_to_director"
    assert p.decisions.get(stage="Dean-RSPC").outcome == "forward"
    assert p.pk in ids(as_role(stub_iam, "Director", DIRECTOR).get(QUEUE))


def test_UC_021_main_flow_not_approved(stub_iam):
    """UC-021 | RSPC-UC-005 Main Flow (not approved) — rejection recorded, request in rejected state.

    Not observable (no RSPC interface): rejection notification event.
    """
    p = proposal("admin_verified")

    resp = act(as_role(stub_iam, "Dean-RSPC", DEAN), p.pk, "decide", "not_approve", "out of scope")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "dean_not_approved"
    d = p.decisions.get(stage="Dean-RSPC")
    assert (d.outcome, d.remarks) == ("not_approve", "out of scope")


def test_UC_023_exception_E1(stub_iam):
    """UC-023 | RSPC-UC-005 Exception E1 — unauthorized Dean-RSPC decision is blocked."""
    p = proposal("admin_verified")

    for role, uid in (("HoD", HOD), ("Faculty", FACULTY_A)):
        resp = act(as_role(stub_iam, role, uid), p.pk, "decide", "approve")
        assert resp.status_code == 403

    p.refresh_from_db()
    assert p.status == "admin_verified"
    assert not p.decisions.exists()


def test_UC_024_exception_E2(stub_iam):
    """UC-024 | RSPC-UC-005 Exception E2 — request outside the Dean-RSPC stage cannot be decided."""
    p = proposal("submitted")

    resp = act(as_role(stub_iam, "Dean-RSPC", DEAN), p.pk, "decide", "approve")

    assert is_rejected_state_error(resp)
    p.refresh_from_db()
    assert p.status == "submitted"
    assert not p.decisions.exists()


# --------------------------------------------------------------------- UC-006
def test_UC_025_main_flow_approve(stub_iam):
    """UC-025 | RSPC-UC-006 Main Flow (approve) — Director approves a routed request.

    Not observable (no RSPC interface): approval notification event.
    """
    p = proposal("forwarded_to_director")
    ProposalDecision.objects.create(proposal=p, stage="Dean-RSPC", actor_id=DEAN, outcome="forward")
    director = as_role(stub_iam, "Director", DIRECTOR)
    row = next(r for r in director.get(QUEUE).json() if r["id"] == p.pk)
    assert row["decisions"]

    resp = act(director, p.pk, "authorize", "approve", "strategic")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "approved"
    d = p.decisions.get(stage="Director")
    assert (d.outcome, d.remarks, d.actor_id) == ("approve", "strategic", DIRECTOR)


def test_UC_026_main_flow_reject(stub_iam):
    """UC-026 | RSPC-UC-006 Main Flow (reject) — Director rejects a routed request.

    Not observable (no RSPC interface): rejection notification event.
    """
    p = proposal("forwarded_to_director")

    resp = act(as_role(stub_iam, "Director", DIRECTOR), p.pk, "authorize", "not_approve", "no")

    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "director_not_approved"
    assert p.decisions.get(stage="Director").outcome == "not_approve"


def test_UC_027_alternative_A1(stub_iam):
    """UC-027 | RSPC-UC-006 Alternative A1 — high-value request is approved only after the Director decision."""
    p = proposal("admin_verified", budget="9000000.00")

    fwd = act(as_role(stub_iam, "Dean-RSPC", DEAN), p.pk, "decide", "forward", "large funding")
    assert fwd.status_code == 200
    p.refresh_from_db()
    assert p.status != "approved"

    resp = act(as_role(stub_iam, "Director", DIRECTOR), p.pk, "authorize", "approve")
    assert resp.status_code == 200
    p.refresh_from_db()
    assert p.status == "approved"


def test_UC_028_exception_E1(stub_iam):
    """UC-028 | RSPC-UC-006 Exception E1 — unauthorized (Dean-RSPC) Director action is blocked."""
    p = proposal("forwarded_to_director")

    resp = act(as_role(stub_iam, "Dean-RSPC", DEAN), p.pk, "authorize", "approve")

    assert resp.status_code == 403
    p.refresh_from_db()
    assert p.status == "forwarded_to_director"
    assert not p.decisions.exists()


def test_UC_029_exception_E2(stub_iam):
    """UC-029 | RSPC-UC-006 Exception E2 — request not routed to Director cannot be decided by Director."""
    p = proposal("admin_verified")

    resp = act(as_role(stub_iam, "Director", DIRECTOR), p.pk, "authorize", "approve")

    assert is_rejected_state_error(resp)
    p.refresh_from_db()
    assert p.status == "admin_verified"
    assert not p.decisions.exists()


# --------------------------------------------------------------------- UC-018
def test_UC_070_main_flow(stub_iam):
    """UC-070 | RSPC-UC-018 Main Flow — authorized role assignment takes effect immediately.

    The role change is supplied by the IAM session (Fusion role management, an
    external dependency faked by stub_iam). Not observable (no RSPC interface):
    the RSPC log entry of the role change.
    """
    p = proposal("submitted")
    uid = 4001

    before = act(as_role(stub_iam, "Faculty", uid), p.pk, "recommend", "recommended")
    assert before.status_code == 403

    after = act(as_role(stub_iam, "HoD", uid), p.pk, "recommend", "recommended")
    assert after.status_code == 200
    p.refresh_from_db()
    assert p.status == "dept_recommended"


def test_UC_071_alternative_A1(stub_iam):
    """UC-071 | RSPC-UC-018 Alternative A1 — reassignment of RSPC Admin from U1 to U2 takes effect.

    Not observable (no RSPC interface): the RSPC log entry of the reassignment.
    """
    p = proposal("dept_recommended")
    u1, u2 = 4101, 4102

    old = act(as_role(stub_iam, "RSPC Admin", u1, perms=()), p.pk, "verify", "eligible")
    assert old.status_code == 403

    new = act(as_role(stub_iam, "RSPC Admin", u2), p.pk, "verify", "eligible")
    assert new.status_code == 200
    p.refresh_from_db()
    assert p.status == "admin_verified"
    assert p.decisions.get().actor_id == u2
