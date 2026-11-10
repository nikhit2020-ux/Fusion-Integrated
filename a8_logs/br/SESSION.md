# A8 — Strategy BR — Claude Code session transcript

Exported from the Claude desktop app (Code tab) session export, converted to Markdown.
Model: Claude Opus 5.5. Thinking blocks are not included.

## User — 2026-11-10T20:57:46.393Z

Read specs_rspc/A8_HANDOFF_CLAUDE.md and do strategy BR, starting with Step A.

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T20:57:48.427Z

```json
{
  "items": [
    {
      "content": "Read the A8 handoff doc",
      "status": "in_progress"
    },
    {
      "content": "Execute strategy BR Step A",
      "status": "pending"
    }
  ],
  "scope": "first_task"
}
```

#### Tool result

````
Plan shown (2 steps).
````

### Tool call: `Bash` — 2026-11-10T20:57:49.013Z

```json
{
  "command": "cat specs_rspc/A8_HANDOFF_CLAUDE.md; ls specs_rspc",
  "description": "Read the handoff doc and list specs folder"
}
```

#### Tool result

````
# Assignment 8 — Specification-Driven AI-Assisted Testing (RSPC) — Claude version

Student: Nikhit Jino (24BCS287), pair partner 24BCS277. Module: RSPC.
**The AI model for this assignment is you: Claude Opus 5.5 in Claude Code** (same model and
effort setting for all four strategies). You generate the test designs and the test code
yourself, following the assignment's exact Prompt A / B / C templates below.

Read this whole file first. Then do only the part Nikhit asks for in this session.

## 0. Rules that protect the study (non-negotiable)
1. **One strategy per Claude Code session.** Nikhit starts a fresh session for FR, UC, BR, WF.
   Never read another strategy's design, tests, results or logs.
2. **Design before code.** Until `<S>_DESIGN.json` is frozen, you may read ONLY:
   this file, `specs_rspc/a8_plain/01_*` (Problem Statement) and that strategy's spec file.
   Do NOT open, grep, list or summarise anything under `modules/`, `client/`, `config/`,
   `core/`, `fusion_auth/`, `tests/`, `registry/`, `openapi/`, git history, or any other spec.
3. **Hidden from you at all times:** `modules/rspc/tests/` (Assignment-7 tests),
   `specs_rspc/logs/`, `specs_rspc/FINAL_REPORT*`, `specs_rspc/a8_qwen_aborted/`,
   `specs_rspc/06_*` (traceability — not used in A8).
4. **Never modify production code** (anything outside `tests/a8/`, `a8_design/`,
   `a8_results/`, `a8_logs/`, `a8_snapshots/`).
5. After the design is frozen, never add/remove/merge/rewrite test cases or expected results.
   No xfail. Do not mock the behaviour under test.
6. **Repair limit:** after writing the tests (Prompt B) you may NOT iterate on them by
   yourself. Only test-code/setup errors that stop execution may be repaired, using at most
   **two Prompt C rounds per strategy**, each logged with the exact error.
7. Do not push or open a PR without Nikhit's OK.

## 1. Environment
- WSL Ubuntu 24.04; repo `/home/nikhit/Documents/Fusion/Fusion-Integrated`.
- Frozen base: tag `a8-base` (4f8c1c7) on branch `a8-24bcs287`. Package for coverage: `modules.rspc`.
- Specs as plain text: `specs_rspc/a8_plain/` (01 Problem Statement, 02 Requirement Registry
  CFR/AFR, 03 Use Cases, 04 Business Rules, 05 Workflows).
- Postgres must be running (Nikhit runs `sudo service postgresql start`). Use `.venv/bin/pytest`.
- Folders: `tests/a8/{fr,uc,br,wf}/`, `a8_design/`, `a8_results/<s>/`, `a8_logs/<s>/`,
  `a8_snapshots/<s>/{raw,final}/`. Create missing ones (with `__init__.py` under `tests/`).

| Strategy | Spec file used (plus 01 Problem Statement) |
|---|---|
| FR | 02 Requirement Registry (CFR/AFR) |
| UC | 03 Use Case Specifications |
| BR | 04 Business Rule Specifications |
| WF | 05 Workflow Specifications |

## 2. Per-strategy procedure
Record the start time in `a8_logs/<s>/LOG.md` and log every step there.

### Step A — design (Prompt A, apply it to yourself exactly)
```
You are designing automated specification-based tests for the RSPC (Research, Sponsored Projects & Consultancy) Fusion ERP module.

Source of truth: Use ONLY the supplied Problem Statement and <STRATEGY SPECIFICATION>.

Do NOT inspect implementation code.
Do NOT infer behavior from implementation.
Do NOT introduce behavior unsupported by the supplied specification.

Generate the minimum non-redundant set of test cases needed to satisfy the strategy-specific adequacy rule in Section 7. Do not stop at an arbitrary number, do not omit an explicit test obligation to reduce the test count, and do not invent unsupported behavior. Prefer observable behavior that can subsequently be automated using pytest/pytest-django.

For every test case output exactly these fields:
- test_id
- source_id
- purpose
- preconditions
- action_or_input
- expected_result
- test_type
- source_id must identify the exact obligation covered (for example: AFR-03, UC-05 Main Flow, UC-05 Alternative A1, BR-07 condition-false, WF-02 approval-rejected path).

Output ONLY a valid JSON array. Do not provide explanation or additional prose.

<SECTION 7 INSTRUCTION>
```
`<STRATEGY SPECIFICATION>` = "Functional Requirements (CFR/AFR)" / "Use Case Specifications" /
"Business Rule Specifications" / "Workflow Specifications". Section 7 instruction (verbatim):
- FR: `Cover every testable CFR/AFR with at least one test. Add a separate negative/boundary/validation/authorization case only where the requirement explicitly defines such a condition or outcome.`
- UC: `Cover the main success flow of every Use Case and every explicitly specified alternative/exception flow with at least one test. Do not invent additional flows.`
- BR: `Cover every Business Rule with at least one test. Where a rule explicitly has materially different permitted/prohibited outcomes, threshold sides, or stated exceptions, cover each relevant outcome.`
- WF: `Cover every explicitly specified distinct workflow path/decision outcome. Ensure every important stated transition is exercised at least once; do not enumerate unsupported combinations.`

Write the prompt (with the filled placeholders) to `a8_logs/<s>/PROMPT_A.txt`, then produce the
JSON array and save it unchanged as `a8_design/<S>_DESIGN.json`. Use test_id format `<S>-NNN`.
The Section-7 rule is an adequacy rule: if the spec has e.g. both CFR and AFR IDs, every
testable ID must appear as a source_id (a test may cite several closely related IDs).

### Step B — freeze
1. List every obligation of that strategy from the spec (FR: every CFR and AFR ID;
   UC: every UC main flow + every explicit alternative/exception flow; BR: every BR plus its
   stated distinct outcomes; WF: every distinct path/decision outcome / important transition).
   Write `a8_logs/<s>/obligations.md`: each obligation → test_id(s), and covered/total.
2. If something is missing, you may complete the design **once**, before freezing, by
   appending cases for the missing obligations only (log it). Untestable obligations
   (e.g. purely organisational statements) are listed with the reason.
3. Freeze: write the SHA-256 of the JSON to `a8_logs/<s>/FROZEN.txt`. Never edit it again.
4. Stop and tell Nikhit the counts. Continue only when he says "continue".

### Step C — implement (Prompt B, apply it to yourself exactly)
Only now may you read the implementation (still never `modules/rspc/tests/`).
```
You are given:
1. the frozen A8_BASE Fusion implementation, and
2. the frozen <STRATEGY>_DESIGN.json.

Convert these test designs into executable automated backend tests using pytest/pytest-django.

Rules:
- Implement exactly the supplied test cases.
- Do not add, remove, merge or reinterpret test cases.
- Preserve each specified expected result.
- Do not modify production code.
- Use the Django isolated test database.
- Reuse existing Fusion test infrastructure where appropriate.
- Do not mock the behavior being tested; mocks may be used only for unavailable external dependencies.
- Do not use xfail to hide failures.
- Every test must contain its test_id and source_id in its name or docstring.
- Store generated tests only under tests/a8/<strategy>/.

If a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.
```
Save the prompt to `a8_logs/<s>/PROMPT_B.txt`. Useful infrastructure: root `conftest.py`
(`FakeIam`, `stub_iam`), the API at `api/v1/rspc/`, permission codes in `modules/rspc/registry.py`.
Implementation note: the RSPC code implements only the research-proposal workflow
(CW-RSPC-01). Behaviour specified for consultancy, staff, finance, procurement, closure,
notifications, reports, etc. has no interface → `NOT_AUTOMATED: <reason>` skip, as the template
says. Where an interface exists, assert the spec's expected result even if you suspect the
code differs (that is how defects are found).
Write all tests, then copy them to `a8_snapshots/<s>/raw/`. **Do not run or edit them yet.**

### Step D — make executable (Prompt C, max 2 rounds)
Run `.venv/bin/pytest tests/a8/<s> --collect-only -q`. If (and only if) syntax/import/
fixture/setup errors stop execution, start a repair round: write to `a8_logs/<s>/PROMPT_C_<n>.txt`
```
The generated test suite cannot execute because of the following test-code/setup error:

<PASTE EXACT ERROR>

Repair the TEST CODE/TEST SETUP only.
Do not modify production code.
Do not alter test intent or expected results.
Do not add or remove test cases.
Do not introduce new specification information.
Make only the minimum changes required to make the frozen tests executable.
```
and apply only that. A setup error that only appears at run time (e.g. a fixture error in the
`ERROR` state) also counts. Assertion failures are NOT repairable. Max 2 rounds; afterwards
leave remaining problems and record them. Copy final tests to `a8_snapshots/<s>/final/`.

### Step E — execute (exact command, repo root)
```
.venv/bin/pytest tests/a8/<s> \
  --junitxml=a8_results/<s>/junit.xml \
  --cov=modules.rspc --cov-branch \
  --cov-report=xml:a8_results/<s>/coverage.xml \
  --cov-report=term-missing \
  > a8_results/<s>/pytest.log 2>&1
```
From coverage.xml compute line and branch coverage for production code only (exclude
`modules/rspc/tests/*` and `modules/rspc/migrations/*`) → `a8_results/<s>/coverage_summary.md`.
Never edit the machine-generated files.

### Step F — examine failures
For every failed/errored test, in `a8_logs/<s>/failures.md`: test_id, source_id, error summary,
and the four checks — (1) expected behaviour directly supported by the cited spec (quote it);
(2) test correctly implemented and set up; (3) reproducible (re-run alone twice);
(4) observed behaviour contradicts expected. All four yes → **Confirmed Implementation Defect**;
otherwise classify (test defect / spec ambiguity / environment). One underlying problem = one
defect. Append to the shared `a8_logs/DEFECTS.md` (create if missing; it is the only file you may
read across strategies, and only in this step), marking which strategies exposed each defect.

### Step G — wrap up
`a8_logs/<s>/SUMMARY.md`: obligations covered/total, test cases automated, executable,
passed, failed, skipped/NOT_AUTOMATED, line %, branch %, candidate failures, confirmed defects,
repair rounds used, elapsed minutes, deviations. Verify
`git diff --stat a8-base -- modules config client registry openapi core fusion_auth` is empty.
Commit only `tests/a8/<s> a8_design/<S>_DESIGN.json a8_results/<s> a8_logs a8_snapshots/<s>`.
Then tell Nikhit to run `/export a8_logs/<s>/SESSION.md` and start a new session for the next strategy.

## 3. Final session (after WF)
Fill the workbook: copy `specs_rspc/Assignment_8_Data_Collection_v2.xlsx` to
`a8_results/Assignment_8_Data_Collection_24BCS287.xlsx`; fill only input cells, keep formulas,
read dropdown lists before writing. Pair & Controls: module RSPC, rolls 24BCS287 / 24BCS277,
model `Claude Opus 5.5`, runtime `Claude Code`, config = the effort setting used, A8_BASE hash,
package `modules.rspc`, order `FR, UC, BR, WF`, same model Yes. Leave Pair/Sub-team ID for Nikhit.
Fill Strategy Summary, Defect Log and Artifact Index (AI Interaction Log = `a8_logs/<s>/SESSION.md`)
from the logs. Record any deviation factually. Show Nikhit `git status`; do not push.
00_RSPC_CORE_CONTEXT.md
00_RSPC_PROMPTS.md
01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.md
02_RSPC_Requirement_Registry_CFR_AFR_v1.3_SYNCHRONIZED.md
03_RSPC_Use_Case_Specifications_v1.3_SYNCHRONIZED.md
04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.md
05_RSPC_Workflow_Specifications_v2.1_SYNCHRONIZED.md
06_RSPC_Traceability_Matrix_v1.3_SYNCHRONIZED.md
A8_HANDOFF_CLAUDE.md
A8_HANDOFF_OPUS.md
CLAUDE_CODE_HANDOFF.md
a8_plain
a8_qwen_aborted
drafts
logs
prompts
tools
````

### Tool call: `Bash` — 2026-11-10T20:57:53.611Z

```json
{
  "command": "ls specs_rspc/a8_plain/; date '+%Y-%m-%d %H:%M:%S %Z'; mkdir -p a8_logs/br a8_design; wc -c specs_rspc/a8_plain/01_* specs_rspc/a8_plain/04_*",
  "description": "List plain specs, record start time, create folders"
}
```

#### Tool result

````
01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt
02_RSPC_Requirement_Registry_CFR_AFR_v1.3_SYNCHRONIZED.txt
03_RSPC_Use_Case_Specifications_v1.3_SYNCHRONIZED.txt
04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.txt
05_RSPC_Workflow_Specifications_v2.1_SYNCHRONIZED.txt
=494
2026-11-10 20:57:55 UTC
11387 specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt
26181 specs_rspc/a8_plain/04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.txt
37568 total
````

### Tool call: `Bash` — 2026-11-10T20:57:57.620Z

```json
{
  "command": "cat specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt",
  "description": "Read the Problem Statement"
}
```

### Tool call: `Bash` — 2026-11-10T20:57:57.824Z

```json
{
  "command": "cat specs_rspc/a8_plain/04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.txt",
  "description": "Read the Business Rule Specifications"
}
```

#### Tool result

````
*Problem Statement - Synchronized Baseline v1.0*

Field | Value

Project | Fusion ERP / CS3010-SE-Lab
Module | RSPC - Research, Sponsored Projects & Consultancy
Artifact | Problem Statement
Version | v1.0 SYNCHRONIZED
Synchronization Date | 2026-08-22
Synchronization Decision | No semantic rewrite required; source PS retained as the governing evidence baseline.

# 1. Overview

The Research, Sponsored Projects & Consultancy (RSPC) Module is a Fusion
ERP module used to digitize, streamline, and govern institutional
research projects, sponsored funding, and consultancy activities
undertaken by faculty members at IIITDM Jabalpur.

The module supports proposal submission, consultancy registration,
multi-level review and approval, financial and fund-request tracking,
staff appointment request handling, procurement request tracking,
progress and utilization reporting, project closure, notifications,
audit trails, and role-based access to RSPC information.

RSPC uses Fusion platform services such as dashboard access, RBAC,
notification delivery, and integration mechanisms. Platform-wide
authentication, identity management, email delivery infrastructure, and
external system ownership remain outside RSPC unless explicitly recorded
as RSPC events, records, validations, notifications, or reports.

The module records and tracks RSPC workflow information. Execution of
external institutional work, such as payroll payment, accounting
disbursement, procurement execution, HR master-data management, or
external funding-agency actions, remains outside RSPC unless explicitly
represented in RSPC as request status, approval, compliance record,
transaction record, report, or notification information.

# 2. Actors

## 2.1 Faculty

Submits funded research project proposals with required project, budget,
funding-source, timeline, and resource information.

Registers consultancy projects with client, scope, deliverable,
timeline, and financial-term information.

Updates project details, milestones, progress information, and
utilization information where permitted by the project lifecycle.

Submits progress reports, utilization reports, completion reports, and
closure reports.

Requests project-based staff appointments and participates in selection
processes where the RSPC workflow requires Faculty involvement.

Submits or records staff-selection recommendations where required by the
RSPC appointment process.

Requests and tracks procurement of project equipment and consumables
through RSPC request/status records.

Submits, views, and tracks project fund-utilization, expenditure, and
financial records within sanctioned provisions.

Views approval history, project status, project history, audit trails,
and financial transaction records for the Faculty member's own projects.

## 2.2 RSPC Admin

Verifies completeness of submitted proposals, consultancy records,
staff-appointment requests, financial requests, procurement requests,
and closure records where applicable.

Checks submitted records for compliance with institutional and
funding-agency requirements configured or referenced for the RSPC
process.

Performs initial scrutiny of financial and fund requests before
forwarding eligible requests.

Manages RSPC operational records for project-based staff appointments,
application records, selection records, appointment duration, stipend
workflow records, and compliance records.

Forwards eligible requests to the Dean-RSPC or other applicable
approving authority according to the RSPC approval path.

Maintains structured RSPC records for audit, compliance, and reporting.

## 2.3 Head of Department (HoD)

Reviews faculty project and consultancy requests assigned to the
department-level review stage.

Evaluates departmental feasibility and alignment for submitted requests.

Records departmental recommendations and forwards recommended requests
to the Dean-RSPC stage as applicable.

## 2.4 Dean-RSPC

Reviews research project proposals, consultancy requests,
staff-appointment requests, budget allocations, financial requests,
procurement requests, and closure records where routed to the Dean-RSPC
stage.

Approves eligible requests within delegated or defined limits.

Reviews compliance with institutional and funding-agency policies
represented in the RSPC process.

Forwards high-value, strategic, or otherwise applicable requests to the
Director where required by the RSPC approval path.

## 2.5 Director

Reviews significant, high-value, strategic, or escalated RSPC requests
routed to the Director stage.

Approves large funding requests and high-value expenditures where such
approval is required by institutional rules.

Ensures adherence to institutional and external funding regulations for
requests routed to the Director stage.

# 3. Functional Scope

## 3.1 Research Project Proposal Management

Faculty members submit detailed research project proposals including
objectives, timelines, budget, funding source, and resource
requirements.

RSPC routes research project proposals through the structured approval
path: Faculty to HoD to RSPC Admin to Dean-RSPC to Director where
applicable.

RSPC validates mandatory proposal fields and configured policy
requirements before or during submission/review processing.

RSPC records decisions with timestamps and remarks at applicable review
stages.

RSPC sends notifications at proposal submission, review, approval,
rejection, escalation, and pending-action stages where applicable.

## 3.2 Consultancy Project Management

Faculty members register consultancy projects with client details,
scope, deliverables, timelines, and financial terms.

RSPC routes consultancy project records through the institutional
approval path represented in the module.

RSPC tracks consultancy payments, deliverables, settlements, approval
history, and financial history as RSPC records.

RSPC maintains complete consultancy financial and approval history for
audit and reporting.

## 3.3 Staff Appointment and Selection Management

Faculty members request project-based staff appointments.

RSPC Admin manages RSPC records for advertisement, applications, stipend
structures, appointment duration, and compliance information.

Faculty members conduct or participate in selection processes and submit
recommendations where the RSPC appointment workflow requires Faculty
involvement.

RSPC routes staff-appointment approvals through Dean-RSPC and Director
where applicable.

RSPC maintains appointment duration, stipend workflow records,
payment-related records, and compliance records. Payroll or payment
execution is outside RSPC unless recorded as RSPC status or transaction
information.

## 3.4 Financial and Fund Management

Faculty members submit fund-utilization and expenditure requests.

RSPC Admin performs initial financial verification of submitted fund and
expenditure requests.

Dean-RSPC approves eligible requests within delegated financial powers.

RSPC escalates high-value requests to the Director where the configured
approval path requires Director approval.

RSPC logs financial request, verification, approval, escalation, and
transaction-record information for audit and reporting.

Actual accounting ledger ownership, bank payment execution, and
disbursement execution remain outside RSPC unless represented as RSPC
records or status updates.

## 3.5 Inventory and Procurement Requests

Faculty members request procurement of project equipment and
consumables.

RSPC validates procurement requests against sanctioned project budgets
represented in the module.

RSPC enforces the approval hierarchy for procurement requests.

RSPC allows procurement status to be tracked through the system.

Purchase execution, vendor management, stock master management, and
physical inventory control remain outside RSPC unless represented as
RSPC request/status information.

## 3.6 Progress Reporting and Monitoring

Faculty members submit periodic progress reports and utilization
reports.

RSPC enforces configured reporting schedules based on applicable
funding-agency or institutional norms.

RSPC sends reminders to stakeholders for pending report submissions.

RSPC keeps historical reports accessible throughout the project
lifecycle to authorized actors.

## 3.7 Project Closure Management

Faculty members submit project closure and completion reports.

RSPC supports verification of financial settlement records and asset
declaration records during closure processing.

RSPC records closure approvals and closure-related remarks.

RSPC archives completed projects with complete audit trails.

## 3.8 Notifications and Communication

RSPC triggers automated notifications for proposal submission and
approval events.

RSPC triggers notifications for pending actions and escalations.

RSPC triggers notifications for reporting deadlines.

RSPC triggers notifications for financial approvals.

RSPC triggers notifications for compliance requirements represented in
the module.

RSPC notifications are delivered through Fusion dashboards and
system-generated emails; platform-level email delivery infrastructure
remains outside RSPC scope.

## 3.9 Integration and Compliance

RSPC may exchange, reference, or record information needed for RSPC
workflows through integration with other Fusion modules.

RSPC may track external funding-agency submission and disbursement
status where such information is represented in the module.

RSPC enforces role-based access to RSPC data using Fusion roles and
permissions.

RSPC maintains logs for audit, transparency, and regulatory compliance.

External funding agency systems, external agency decisions, external
disbursement execution, and external policy ownership remain outside
RSPC unless represented as RSPC records, validations, notifications, or
reports.

# 4. Security and Role Management

Access to RSPC project data is role-based.

Users can perform only actions permitted by their assigned RSPC roles.

RSPC uses role assignments and reassignment information provided through
Fusion or institutional authority.

RSPC records role changes relevant to RSPC access where such changes are
represented in the module.

Role changes take effect immediately for RSPC access when assigned in
the applicable Fusion role-management mechanism.

Platform-wide authentication, user-account administration, and HR
master-data ownership remain outside RSPC.

# 5. Scope Boundaries

RSPC does not perform payroll execution, bank payment execution,
accounting ledger ownership, procurement execution, vendor management,
stock master management, HR master-data management, or platform-wide
user-account administration.

RSPC may record, validate, route, approve, track, notify, report, or
audit RSPC-related information associated with staff appointments,
stipends, finances, procurement, projects, consultancy, progress
reports, and closure.

External funding-agency policies, institutional rules, financial limits,
reporting schedules, selection rules, and approval thresholds are
outside RSPC unless RSPC explicitly validates, restricts, routes,
records, notifies, escalates, or reports based on them.

The System is not treated as a regular primary actor in later use cases
derived from this problem statement. System behavior appears as internal
validation, state update, notification, escalation, postcondition,
maintained data, or reporting behavior.
````

#### Tool result

````
Business Rule Specifications v1.3 SYNCHRONIZED

Field | Value

Project | Fusion ERP / CS3010-SE-Lab
Module | RSPC
Artifact | Business Rule Specifications
Version | v1.3 SYNCHRONIZED
Date | 2026-08-30
Active BR Count | 38
Retired Legacy BR Count | 32
Rule Principle | Only reusable governing logic is retained as BR; functional/data obligations remain AFR/UC behavior; traceability is CFR/AFR-aware.

# Active Business Rules

Rule ID / Name
Rule Type
Rule Statement
Applies To
Condition / Trigger
Required Outcome / Constraint
Exceptions / Exclusions
Source / Rationale
Related CFRs / AFRs / UCs / WFs
Status / Notes

BR-RSPC-004

Forward Applicable High-Value or Strategic Requests to Director
Routing
Dean-RSPC shall forward a high-value, strategic, or otherwise
applicable RSPC request to Director when the represented approval path
requires Director action.
Research, consultancy, staff appointment, financial, procurement,
and closure requests where the represented path includes Director.
Dean-RSPC is reviewing an eligible routed request and Director
action is required by the represented path.
The request is forwarded to the Director stage rather than finalized
at Dean-RSPC.
Exact thresholds/criteria remain external unless explicitly
represented/configured in RSPC.
PS 2.4 Dean-RSPC; PS 5 Scope Boundaries

Active

BR-RSPC-005

Director Approval for Large Funding Requests
Authorization
Director approval is required for large funding requests where
institutional rules represented in the RSPC approval path require
Director approval.
Large funding requests routed to Director.
A funding request meets the represented condition for Director
approval.
Only Director may record the required final Director approval at
that stage.
Exact monetary threshold remains external unless
represented/configured in RSPC.
PS 2.5 Director; PS 5 Scope Boundaries

Active

BR-RSPC-006

Director Authorization for High-Value Expenditures
Authorization
Director authorization is required for high-value expenditures where
institutional rules represented in the RSPC approval path require
Director authorization.
High-value expenditure requests routed to Director.
An expenditure request meets the represented condition for Director
authorization.
Only Director may record the required authorization at that
stage.
Exact monetary threshold remains external unless
represented/configured in RSPC.
PS 2.5 Director; PS 5 Scope Boundaries

Active

BR-RSPC-012

Research Proposal Approval Route
Routing
Research project proposals shall follow the represented route
Faculty -> HoD -> RSPC Admin -> Dean-RSPC -> Director where
applicable.
Research-project proposal processing.
A Faculty proposal is submitted.
RSPC advances the proposal through the stated stages, with Director
used only when applicable.
Director stage is conditional; exact applicability depends on
represented institutional rules.
PS 3.1 Research Project Proposal Management

Active

BR-RSPC-013

Mandatory Research Proposal Fields
Validation
RSPC shall not advance a research-project proposal as submitted when
mandatory proposal fields represented in RSPC are incomplete.
Research-project proposal submission.
Faculty attempts to submit a proposal.
Submission/advancement occurs only after mandatory-field validation
passes.
Which fields are mandatory is determined by the represented proposal
configuration; the PS names objectives, timelines, budget, funding
source, and resource requirements as required proposal information.
PS 3.1 Research Project Proposal Management

Active

BR-RSPC-014

Represented Proposal Policy Validation
Validation
RSPC shall enforce a proposal policy validation only when the
applicable institutional or funding-agency policy is explicitly
represented/configured as an RSPC validation.
Research-project proposal submission/review.
A represented policy validation applies to the proposal.
RSPC evaluates the validation and prevents invalid advancement where
the represented validation requires it.
External policy values not represented in RSPC are not invented by
the module.
PS 3.1; PS 5 Scope Boundaries

Active

BR-RSPC-015

Timestamp Proposal Review Decisions
Record/Compliance
RSPC shall record a timestamp for each applicable research-proposal
review/approval decision represented in the process.
Research-project proposal review stages.
An applicable proposal review/approval decision is recorded.
The decision record includes a timestamp.
Applies only to proposal decision stages represented in RSPC.
PS 3.1 Research Project Proposal Management

Active

BR-RSPC-016

Record Proposal Decision Remarks
Record/Compliance
RSPC shall record remarks for each applicable research-proposal
review/approval decision represented in the process.
Research-project proposal review stages.
An applicable proposal review/approval decision is recorded.
The decision record includes the applicable remarks.
Applies only to proposal decision stages represented in RSPC.
PS 3.1 Research Project Proposal Management

Active

BR-RSPC-022

Consultancy Approval Route Follows Represented Institutional Policy
Routing
Consultancy project records shall be routed according to the
institutional approval path represented in RSPC.
Consultancy project registration/approval.
A consultancy record is submitted.
RSPC advances the consultancy through only those approval stages
represented as applicable.
HoD and/or Director stages are conditional where the represented
institutional path makes them applicable.
PS 3.2 Consultancy Project Management; PS 2.3-2.5

Active

BR-RSPC-026

Staff Appointment Approval Route
Routing
Project-based staff-appointment approvals shall be routed through
Dean-RSPC and Director where applicable in the represented appointment
path.
Project staff appointment processing.
An eligible appointment request reaches the approval phase.
RSPC routes the request to Dean-RSPC and, where applicable,
Director.
Exact applicability/thresholds remain external unless
represented/configured in RSPC.
PS 3.3 Staff Appointment and Selection Management

Active

BR-RSPC-032

Dean Financial Approval Limited to Delegated Powers
Authorization
Dean-RSPC may approve a financial request only within delegated
financial powers represented for the RSPC process.
Fund-utilization and expenditure requests.
A verified financial request reaches Dean-RSPC.
Requests within delegated powers may be approved at Dean-RSPC;
others follow the represented escalation path.
Exact delegated limits remain external unless
represented/configured.
PS 3.4 Financial and Fund Management

Active

BR-RSPC-033

Escalate High-Value Financial Requests to Director
Routing
RSPC shall escalate a high-value financial request to Director when
the represented approval path requires Director approval.
Fund-utilization and expenditure requests.
A verified financial request meets the represented
Director-escalation condition.
The request is routed to Director.
Exact high-value threshold remains external unless
represented/configured.
PS 3.4 Financial and Fund Management

Active

BR-RSPC-034

Audit Financial Request Lifecycle Events
Record/Compliance
RSPC shall log financial request, verification, approval,
escalation, and transaction-record information for audit and
reporting.
Financial/fund management.
A financial request or its
verification/decision/escalation/transaction record changes.
The relevant lifecycle event is retained in the RSPC audit/reporting
record.
Actual accounting-ledger and payment execution remain external.
PS 3.4 Financial and Fund Management

Active

BR-RSPC-035

Procurement Request Must Match Sanctioned Budget
Validation
RSPC shall validate a project procurement request against the
sanctioned project budget represented in the module before advancing it
as eligible.
Equipment and consumables procurement requests.
A procurement request is submitted/verified.
Only a request passing the represented sanctioned-budget validation
is advanced as eligible.
Budget data/limits are used only when represented in RSPC.
PS 3.5 Inventory and Procurement Requests

Active

BR-RSPC-036

Procurement Approval Hierarchy
Routing/Authorization
RSPC shall enforce the approval hierarchy represented for
procurement requests.
Equipment and consumables procurement requests.
An eligible procurement request advances to approval.
RSPC routes the request only through the approval stages represented
as applicable.
Exact approval thresholds/levels remain external unless
represented/configured.
PS 3.5 Inventory and Procurement Requests

Active

BR-RSPC-037

Represented Reporting Schedule
Timing
RSPC shall enforce reporting schedules configured from applicable
funding-agency or institutional norms.
Progress and utilization reporting.
A project has a represented reporting schedule.
Due/pending report status and reminders are based on the represented
schedule.
External schedule norms not represented/configured in RSPC are not
invented.
PS 3.6 Progress Reporting and Monitoring; PS 5 Scope Boundaries

Active

BR-RSPC-038

Authorized Access to Historical Progress Reports
Access/Authorization
Historical progress reports shall remain accessible throughout the
project lifecycle only to actors authorized for those records.
Progress-report history.
An actor requests historical progress reports.
RSPC displays the reports only within the actor's authorized
role/project scope.
None beyond role/project authorization.
PS 3.6; PS 3.9; PS 4

Active

BR-RSPC-039

Authorized Access to Historical Utilization Reports
Access/Authorization
Historical utilization reports shall remain accessible throughout
the project lifecycle only to actors authorized for those records.
Utilization-report history.
An actor requests historical utilization reports.
RSPC displays the reports only within the actor's authorized
role/project scope.
None beyond role/project authorization.
PS 3.6; PS 3.9; PS 4

Active

BR-RSPC-043

Archive Approved Completed Projects with Audit Trail
Lifecycle/Record
When a project is completed and its closure is approved in the
represented RSPC process, RSPC shall archive the project with its
complete RSPC audit trail.
Project closure.
Closure approval is recorded for a completed project.
The project is archived as closed with the RSPC audit trail
retained.
RSPC does not perform external settlement or inventory operations as
part of archival.
PS 3.7 Project Closure Management

Active

BR-RSPC-045

Integration Only Where Explicitly Configured
Integration/Scope
RSPC shall exchange, reference, or record information through
another Fusion module or external integration only where that
integration is explicitly represented/configured for RSPC.
Fusion-module and external integrations.
An integration attempts to exchange or supply RSPC-relevant
information.
Only represented/configured integration information is processed as
an RSPC integration.
RSPC does not assume ownership of the connected system's business
process.
PS 1 Overview; PS 3.9 Integration and Compliance

Active

BR-RSPC-048

Role-Based Access to RSPC Data
Access/Authorization
Access to RSPC project and process data shall be restricted by the
user's assigned RSPC role and authorized record scope.
All RSPC data access.
A user requests RSPC information.
Only authorized data are displayed or made available.
Platform-wide authentication/role administration remains outside
RSPC.
PS 3.9; PS 4

Active

BR-RSPC-049

Actions Restricted by Assigned RSPC Role
Access/Authorization
RSPC shall permit a user to perform only those RSPC actions allowed
by the user's assigned RSPC role.
All RSPC actor actions.
A user attempts an RSPC action.
Unauthorized actions are blocked.
Platform-wide RBAC administration remains outside RSPC.
PS 3.9; PS 4

Active

BR-RSPC-050

Maintain RSPC Audit and Compliance Logs
Record/Compliance
RSPC shall maintain logs needed for audit, transparency, and
regulatory compliance for RSPC-managed records and events.
RSPC lifecycle events and records.
An auditable RSPC event/record change occurs.
The relevant log/audit information is retained.
Logging is limited to RSPC-owned/represented information.
PS 3.9 Integration and Compliance

Active

BR-RSPC-053

Accept Role Assignment Only from Authorized Role-Management
Mechanism
Authorization/Scope
RSPC shall apply role-assignment information only when it is
supplied through the applicable authorized Fusion or institutional
role-management mechanism.
RSPC role synchronization.
Role-assignment information is supplied to RSPC.
Authorized role-assignment information is applied to RSPC
access.
RSPC does not create or administer platform-wide
roles/accounts.
PS 4 Security and Role Management; PS 5

Active

BR-RSPC-054

Accept Role Reassignment Only from Authorized Role-Management
Mechanism
Authorization/Scope
RSPC shall apply role-reassignment information only when it is
supplied through the applicable authorized Fusion or institutional
role-management mechanism.
RSPC role synchronization.
Role-reassignment information is supplied to RSPC.
Authorized role-reassignment information is applied to RSPC
access.
RSPC does not create or administer platform-wide
roles/accounts.
PS 4 Security and Role Management; PS 5

Active

BR-RSPC-055

Immediate RSPC Effect of Authorized Role Change
Lifecycle/Authorization
An authorized RSPC role change supplied through the applicable
role-management mechanism shall take effect immediately for RSPC
access.
RSPC role synchronization.
An authorized role assignment/reassignment is received.
RSPC access restrictions reflect the new role immediately.
Platform role-management execution itself remains external.
PS 4 Security and Role Management

Active

BR-RSPC-058

No HR or Payroll Execution in RSPC
Scope Boundary
RSPC shall not perform HR master-data management or payroll/payment
execution for project-based staff appointments.
Staff appointment/selection.
RSPC processes project-staff appointment information.
RSPC limits behavior to request, selection, stipend/payment-related
status/records, compliance, and approval tracking.
External HR/payroll systems/processes remain outside RSPC.
PS 1; PS 3.3; PS 5

Active

BR-RSPC-059

No Accounting or Bank-Payment Execution in RSPC
Scope Boundary
RSPC shall not own accounting-ledger processing, bank-payment
execution, or disbursement execution for project finances.
Financial management and closure settlement records.
RSPC processes financial/settlement information.
RSPC limits behavior to request, verification, approval, tracking,
status, transaction-record, and reporting information.
External accounts/payment execution remains outside RSPC.
PS 1; PS 3.4; PS 5

Active

BR-RSPC-060

No Procurement or Inventory Execution in RSPC
Scope Boundary
RSPC shall not perform purchase execution, vendor management,
stock-master management, or physical inventory control beyond RSPC
request/status/approval tracking.
Procurement and closure asset records.
RSPC processes procurement or asset-declaration information.
RSPC limits behavior to request, validation, approval, status
tracking, and recorded asset information.
External procurement/inventory execution remains outside RSPC.
PS 1; PS 3.5; PS 5

Active

BR-RSPC-061

Notification Delivery Infrastructure Remains External
Scope Boundary
RSPC may trigger dashboard and system-generated email notification
events, but platform-level email-delivery infrastructure remains outside
RSPC ownership.
RSPC notifications.
An RSPC notification event is triggered.
RSPC records/triggers the notification through represented Fusion
channels without assuming ownership of platform email
infrastructure.
External delivery failure does not expand RSPC scope.
PS 1; PS 3.8; PS 5

Active

BR-RSPC-062

External Funding-Agency Processes Remain External
Scope Boundary
RSPC shall not own external funding-agency decisions, submission
execution, or disbursement execution beyond RSPC records, validations,
notifications, reports, or represented submission/disbursement tracking
information.
External funding-agency interaction.
RSPC receives or references external funding-agency
information.
RSPC stores/tracks only the represented information and does not
execute the external agency process.
None.
PS 1; PS 3.9; PS 5

Active

BR-RSPC-063

Platform Authentication and RBAC Administration Remain External
Scope Boundary
RSPC shall not own platform-wide authentication, user-account
administration, or platform-wide RBAC administration beyond applying
RSPC role/action restrictions from the applicable Fusion/institutional
mechanism.
All RSPC access and role synchronization.
RSPC uses Fusion authentication/role information.
RSPC consumes and enforces RSPC-relevant access information without
administering the platform identity/RBAC system.
None.
PS 1; PS 4; PS 5

Active

BR-RSPC-065

Project Updates Must Be Lifecycle-Permitted
Lifecycle/Authorization
Faculty may update project details, milestones, progress
information, or utilization information only where the current project
lifecycle permits the requested update.
Faculty project maintenance.
Faculty attempts to update an existing project.
RSPC exposes/saves only updates permitted in the current lifecycle
state.
Exact lifecycle editability rules remain external/configured unless
represented in RSPC.
PS 2.1 Faculty; PS 5 Scope Boundaries

Active

BR-RSPC-066

Forward Only Eligible Verified Requests
Routing/Eligibility
RSPC Admin shall forward a request to the next applicable approving
authority only when the required RSPC completeness/compliance
verification has produced an eligible outcome.
Research/consultancy/staff/financial/procurement/closure
verification.
RSPC Admin completes required verification.
Eligible requests advance; ineligible requests do not advance as
eligible.
Eligibility details depend on represented/configured
requirements.
PS 2.2 RSPC Admin

Active

BR-RSPC-067

Forward Recommended Department Requests
Routing
HoD shall forward a project or consultancy request to the next
applicable stage only when the departmental recommendation is recorded
as recommended.
Department-level project/consultancy review.
HoD completes department-level review.
Recommended requests advance; non-recommended requests are recorded
without being forwarded as recommended.
Consultancy HoD stage applies only where
represented/applicable.
PS 2.3 HoD

Active

BR-RSPC-068

Dean Approval Limited to Eligible Requests and Delegated/Defined
Authority
Authorization
Dean-RSPC may approve only an eligible routed RSPC request that
falls within the delegated or defined authority represented for that
request; otherwise the represented forwarding/escalation path
applies.
Dean-RSPC decisions across RSPC request types.
An eligible request reaches Dean-RSPC.
Dean-RSPC records approval only within represented authority, or
forwards/escalates where the represented path requires it.
Exact limits remain external unless represented/configured.
PS 2.4 Dean-RSPC; PS 5

Active

BR-RSPC-069

Director Stage Only for Applicable Significant or Escalated
Requests
Routing
The Director stage shall be used only for significant, high-value,
strategic, escalated, or otherwise applicable requests routed under the
represented RSPC approval path.
Director-routed RSPC requests.
A request is considered for Director routing.
Only requests meeting the represented Director-routing condition
enter the Director stage.
Exact criteria/thresholds remain external unless
represented/configured.
PS 2.4-2.5; PS 5

Active

BR-RSPC-070

External Policy Values Are Not Invented
Scope/Validation
External funding-agency policies, institutional rules, financial
limits, reporting schedules, selection rules, and approval thresholds
shall affect RSPC behavior only when RSPC explicitly represents them as
a validation, restriction, routing condition, record requirement,
notification, escalation, or report rule.
All policy-governed RSPC processing.
An external policy/threshold would affect RSPC behavior.
RSPC uses only explicitly represented/configured policy
semantics.
Unrepresented external policy values remain outside the RSPC
specification.
PS 5 Scope Boundaries

Active

# Retired Legacy BR IDs

BR ID | Disposition

BR-RSPC-001 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-002 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-003 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-007 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-008 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-009 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-010 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-011 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-017 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-018 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-019 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-020 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-021 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-023 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-024 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-025 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-027 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-028 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-029 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-030 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-031 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-040 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-041 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-042 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-044 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-046 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-047 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-051 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-052 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-056 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-057 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
BR-RSPC-064 | Retired from active BR baseline: legacy statement was a functional/data obligation, duplicate rule, or representation/modeling statement rather than reusable governing logic.
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T20:58:38.691Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 2 is in progress.
````

### Tool call: `Bash` — 2026-11-10T20:58:46.996Z

```json
{
  "command": "cat > a8_logs/br/PROMPT_A.txt <<'EOF'\nYou are designing automated specification-based tests for the RSPC (Research, Sponsored Projects & Consultancy) Fusion ERP module.\n\nSource of truth: Use ONLY the supplied Problem Statement and Business Rule Specifications.\n\nDo NOT inspect implementation code.\nDo NOT infer behavior from implementation.\nDo NOT introduce behavior unsupported by the supplied specification.\n\nGenerate the minimum non-redundant set of test cases needed to satisfy the strategy-specific adequacy rule in Section 7. Do not stop at an arbitrary number, do not omit an explicit test obligation to reduce the test count, and do not invent unsupported behavior. Prefer observable behavior that can subsequently be automated using pytest/pytest-django.\n\nFor every test case output exactly these fields:\n- test_id\n- source_id\n- purpose\n- preconditions\n- action_or_input\n- expected_result\n- test_type\n- source_id must identify the exact obligation covered (for example: AFR-03, UC-05 Main Flow, UC-05 Alternative A1, BR-07 condition-false, WF-02 approval-rejected path).\n\nOutput ONLY a valid JSON array. Do not provide explanation or additional prose.\n\nCover every Business Rule with at least one test. Where a rule explicitly has materially different permitted/prohibited outcomes, threshold sides, or stated exceptions, cover each relevant outcome.\n\n[Supplied inputs: specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt and specs_rspc/a8_plain/04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.txt]\nEOF\ncat > a8_logs/br/LOG.md <<'EOF'\n# A8 — Strategy BR — Log\n\n- Model: Claude Opus 5.5 (Claude Code), same model/effort as FR and UC sessions.\n- Start time: 2026-11-10 20:57:55 UTC\n\n## Step A — design\n- 20:57 Read `specs_rspc/A8_HANDOFF_CLAUDE.md`.\n- 20:58 Read only `specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt` and\n  `specs_rspc/a8_plain/04_RSPC_Business_Rule_Specifications_v1.3_SYNCHRONIZED.txt`.\n  No implementation code, tests, other specs, other strategies' files or git history were opened.\n- Spec lists 38 active BRs (004–006, 012–016, 022, 026, 032–039, 043, 045, 048–050, 053–055,\n  058–063, 065–070); 32 retired legacy IDs carry no rule statement and are not test obligations.\n- Wrote `a8_logs/br/PROMPT_A.txt` (Prompt A with BR placeholders filled, Section-7 BR rule verbatim).\nEOF",
  "description": "Write Prompt A and start the BR log"
}
```

#### Tool result

````
(Bash completed with no output)
````

## Claude — 2026-11-10T20:58:46.695Z

Now the design JSON (Prompt A output).

### Tool call: `Write` — 2026-11-10T21:00:24.482Z

```json
{
  "file_path": "/home/nikhit/Documents/Fusion/Fusion-Integrated/a8_design/BR_DESIGN.json",
  "content": "[\n  {\n    \"test_id\": \"BR-001\",\n    \"source_id\": \"BR-RSPC-004 condition-true (Director action required)\",\n    \"purpose\": \"Verify that Dean-RSPC forwards a request whose represented approval path requires Director action to the Director stage instead of finalizing it.\",\n    \"preconditions\": \"An eligible research project proposal has passed HoD and RSPC Admin stages and is pending at the Dean-RSPC stage; the represented approval path for this proposal requires Director action. Dean-RSPC user is authenticated.\",\n    \"action_or_input\": \"Dean-RSPC records a favourable decision / forwards the proposal.\",\n    \"expected_result\": \"The proposal moves to the Director stage and is pending Director action; it is not recorded as finally approved at Dean-RSPC.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-002\",\n    \"source_id\": \"BR-RSPC-005 permitted (Director records approval of large funding request)\",\n    \"purpose\": \"Verify that the Director can record the required final approval for a large funding request at the Director stage.\",\n    \"preconditions\": \"A large funding request meeting the represented Director-approval condition is pending at the Director stage. Director user is authenticated.\",\n    \"action_or_input\": \"Director records approval of the request.\",\n    \"expected_result\": \"The approval is accepted and recorded as the Director's final approval; the request is shown as approved.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-003\",\n    \"source_id\": \"BR-RSPC-005 prohibited (non-Director records Director-stage approval)\",\n    \"purpose\": \"Verify that a user without the Director role cannot record the required Director approval for a large funding request.\",\n    \"preconditions\": \"A large funding request meeting the represented Director-approval condition is pending at the Director stage. A Dean-RSPC user (not Director) is authenticated.\",\n    \"action_or_input\": \"Dean-RSPC user attempts to record the final approval at the Director stage.\",\n    \"expected_result\": \"The action is rejected as unauthorized; the request remains pending at the Director stage and is not marked approved.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-004\",\n    \"source_id\": \"BR-RSPC-006 permitted (Director authorizes high-value expenditure)\",\n    \"purpose\": \"Verify that the Director can record the required authorization for a high-value expenditure request at the Director stage.\",\n    \"preconditions\": \"A high-value expenditure request meeting the represented Director-authorization condition is pending at the Director stage. Director user is authenticated.\",\n    \"action_or_input\": \"Director records authorization of the expenditure request.\",\n    \"expected_result\": \"The authorization is accepted and recorded; the expenditure request is shown as authorized/approved.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-005\",\n    \"source_id\": \"BR-RSPC-006 prohibited (non-Director authorizes high-value expenditure)\",\n    \"purpose\": \"Verify that a user without the Director role cannot record the required Director authorization for a high-value expenditure.\",\n    \"preconditions\": \"A high-value expenditure request meeting the represented Director-authorization condition is pending at the Director stage. An RSPC Admin or Dean-RSPC user (not Director) is authenticated.\",\n    \"action_or_input\": \"The non-Director user attempts to record authorization at the Director stage.\",\n    \"expected_result\": \"The action is rejected as unauthorized; the expenditure request remains pending at the Director stage and is not authorized.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-006\",\n    \"source_id\": \"BR-RSPC-012 route with Director applicable; BR-RSPC-069 condition-true\",\n    \"purpose\": \"Verify that a research proposal requiring the Director stage advances in order Faculty -> HoD -> RSPC Admin -> Dean-RSPC -> Director.\",\n    \"preconditions\": \"Faculty, HoD, RSPC Admin, Dean-RSPC and Director users exist with their RSPC roles; the proposal meets the represented Director-routing condition.\",\n    \"action_or_input\": \"Faculty submits a complete proposal; HoD recommends/forwards; RSPC Admin verifies as eligible and forwards; Dean-RSPC forwards; Director approves.\",\n    \"expected_result\": \"After each action the proposal is at the next stated stage (HoD, then RSPC Admin, then Dean-RSPC, then Director); after the Director decision the proposal is approved. No stage is skipped.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-007\",\n    \"source_id\": \"BR-RSPC-012 stated exception (Director stage not applicable); BR-RSPC-069 condition-false; BR-RSPC-068 permitted\",\n    \"purpose\": \"Verify that a research proposal for which the Director stage is not applicable is finalized at Dean-RSPC without entering the Director stage.\",\n    \"preconditions\": \"A proposal that does not meet the represented Director-routing condition has passed HoD and RSPC Admin (eligible) and is pending at Dean-RSPC; it is within Dean-RSPC's represented authority.\",\n    \"action_or_input\": \"Dean-RSPC approves the proposal.\",\n    \"expected_result\": \"The proposal is recorded as approved at Dean-RSPC and never enters the Director stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-008\",\n    \"source_id\": \"BR-RSPC-012 out-of-order stage action prohibited\",\n    \"purpose\": \"Verify that a later-stage approver cannot act on a proposal that has not yet reached that stage.\",\n    \"preconditions\": \"A Faculty proposal has just been submitted and is pending at the HoD stage. Dean-RSPC user is authenticated.\",\n    \"action_or_input\": \"Dean-RSPC attempts to approve/forward the proposal while it is still at the HoD stage.\",\n    \"expected_result\": \"The action is rejected; the proposal remains at the HoD stage and its status is unchanged.\",\n    \"test_type\": \"routing-negative\"\n  },\n  {\n    \"test_id\": \"BR-009\",\n    \"source_id\": \"BR-RSPC-013 condition-true (all mandatory fields complete)\",\n    \"purpose\": \"Verify that a proposal with all mandatory fields is accepted as submitted and advances.\",\n    \"preconditions\": \"Faculty user is authenticated.\",\n    \"action_or_input\": \"Faculty submits a proposal with objectives, timelines, budget, funding source and resource requirements all provided.\",\n    \"expected_result\": \"Submission succeeds; the proposal is recorded as submitted and advances to the HoD review stage.\",\n    \"test_type\": \"validation-positive\"\n  },\n  {\n    \"test_id\": \"BR-010\",\n    \"source_id\": \"BR-RSPC-013 condition-false (a mandatory field missing)\",\n    \"purpose\": \"Verify that a proposal is not advanced as submitted when any of the mandatory fields named in the PS is incomplete.\",\n    \"preconditions\": \"Faculty user is authenticated.\",\n    \"action_or_input\": \"For each mandatory field in turn (objectives, timelines, budget, funding source, resource requirements), Faculty submits an otherwise complete proposal with that field missing/blank.\",\n    \"expected_result\": \"Each submission is rejected with a validation error identifying the incomplete field; no proposal is recorded as submitted or advanced to HoD.\",\n    \"test_type\": \"validation-negative\"\n  },\n  {\n    \"test_id\": \"BR-011\",\n    \"source_id\": \"BR-RSPC-014 represented validation fails; BR-RSPC-070 represented policy applied\",\n    \"purpose\": \"Verify that a represented/configured proposal policy validation prevents advancement of a proposal that violates it.\",\n    \"preconditions\": \"A proposal policy validation is explicitly represented/configured in RSPC (e.g. a configured limit on a proposal attribute). Faculty user is authenticated.\",\n    \"action_or_input\": \"Faculty submits an otherwise complete proposal that violates the represented policy validation.\",\n    \"expected_result\": \"The proposal is not advanced; a validation error referencing the policy is returned.\",\n    \"test_type\": \"validation-negative\"\n  },\n  {\n    \"test_id\": \"BR-012\",\n    \"source_id\": \"BR-RSPC-014 represented validation passes\",\n    \"purpose\": \"Verify that a proposal satisfying the represented policy validation advances normally.\",\n    \"preconditions\": \"The same represented/configured proposal policy validation as BR-011 exists. Faculty user is authenticated.\",\n    \"action_or_input\": \"Faculty submits a complete proposal that satisfies the represented policy validation.\",\n    \"expected_result\": \"The proposal is accepted as submitted and advances to the HoD stage.\",\n    \"test_type\": \"validation-positive\"\n  },\n  {\n    \"test_id\": \"BR-013\",\n    \"source_id\": \"BR-RSPC-015\",\n    \"purpose\": \"Verify that every recorded research-proposal review/approval decision carries a timestamp.\",\n    \"preconditions\": \"A submitted proposal; HoD, RSPC Admin, Dean-RSPC users exist.\",\n    \"action_or_input\": \"HoD, RSPC Admin and Dean-RSPC each record their decision on the proposal; then retrieve the proposal's decision/approval history.\",\n    \"expected_result\": \"Each decision record in the history includes a non-empty timestamp corresponding to when the decision was recorded.\",\n    \"test_type\": \"record\"\n  },\n  {\n    \"test_id\": \"BR-014\",\n    \"source_id\": \"BR-RSPC-016\",\n    \"purpose\": \"Verify that every recorded research-proposal review/approval decision retains the remarks entered with it.\",\n    \"preconditions\": \"A submitted proposal; HoD, RSPC Admin, Dean-RSPC users exist.\",\n    \"action_or_input\": \"HoD, RSPC Admin and Dean-RSPC each record their decision with distinct remarks text; then retrieve the decision/approval history.\",\n    \"expected_result\": \"Each decision record includes exactly the remarks entered by that reviewer.\",\n    \"test_type\": \"record\"\n  },\n  {\n    \"test_id\": \"BR-015\",\n    \"source_id\": \"BR-RSPC-022 HoD and Director stages applicable\",\n    \"purpose\": \"Verify that a consultancy record whose represented path includes HoD and Director passes through those stages.\",\n    \"preconditions\": \"The represented institutional path for the consultancy makes the HoD and Director stages applicable. Faculty and approver users exist.\",\n    \"action_or_input\": \"Faculty submits the consultancy record; each applicable approver acts in turn.\",\n    \"expected_result\": \"The consultancy passes through the HoD stage and the Director stage as part of its approval; it is approved only after the Director stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-016\",\n    \"source_id\": \"BR-RSPC-022 stated exception (HoD and Director stages not applicable)\",\n    \"purpose\": \"Verify that a consultancy record is routed only through represented applicable stages, skipping HoD and Director when they are not applicable.\",\n    \"preconditions\": \"The represented institutional path for the consultancy does not make the HoD or Director stages applicable.\",\n    \"action_or_input\": \"Faculty submits the consultancy record; the applicable approvers act.\",\n    \"expected_result\": \"The consultancy never enters the HoD or Director stage and is finalized at the last applicable stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-017\",\n    \"source_id\": \"BR-RSPC-026 Director not applicable\",\n    \"purpose\": \"Verify that an eligible staff-appointment request is routed to Dean-RSPC and finalized there when Director is not applicable.\",\n    \"preconditions\": \"An eligible project staff-appointment request has reached the approval phase; the represented appointment path does not make Director applicable.\",\n    \"action_or_input\": \"The request reaches the approval phase; Dean-RSPC approves.\",\n    \"expected_result\": \"The request is routed to Dean-RSPC and recorded as approved there without entering the Director stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-018\",\n    \"source_id\": \"BR-RSPC-026 Director applicable\",\n    \"purpose\": \"Verify that an eligible staff-appointment request is routed through Dean-RSPC and then Director when Director is applicable.\",\n    \"preconditions\": \"An eligible project staff-appointment request has reached the approval phase; the represented appointment path makes Director applicable.\",\n    \"action_or_input\": \"Dean-RSPC acts on the request, then Director approves.\",\n    \"expected_result\": \"The request is routed to Dean-RSPC, then to Director, and is approved only after the Director decision.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-019\",\n    \"source_id\": \"BR-RSPC-032 within delegated powers; BR-RSPC-033 condition-false\",\n    \"purpose\": \"Verify that a verified financial request within Dean-RSPC's represented delegated powers can be approved at Dean-RSPC and is not escalated.\",\n    \"preconditions\": \"Delegated financial powers for Dean-RSPC are represented/configured; a verified fund-utilization/expenditure request with amount within the delegated limit is at Dean-RSPC.\",\n    \"action_or_input\": \"Dean-RSPC approves the request.\",\n    \"expected_result\": \"The request is recorded as approved at Dean-RSPC and is not routed to Director.\",\n    \"test_type\": \"threshold-within\"\n  },\n  {\n    \"test_id\": \"BR-020\",\n    \"source_id\": \"BR-RSPC-032 beyond delegated powers; BR-RSPC-033 condition-true\",\n    \"purpose\": \"Verify that a verified financial request beyond Dean-RSPC's delegated powers is not approved at Dean-RSPC and is escalated to Director.\",\n    \"preconditions\": \"Delegated financial powers for Dean-RSPC are represented/configured; a verified request with amount exceeding the delegated limit (meeting the Director-escalation condition) is at Dean-RSPC.\",\n    \"action_or_input\": \"Dean-RSPC attempts to approve the request / the request is processed at Dean-RSPC.\",\n    \"expected_result\": \"Dean-RSPC approval is not recorded as final; the request is routed to the Director stage.\",\n    \"test_type\": \"threshold-exceeded\"\n  },\n  {\n    \"test_id\": \"BR-021\",\n    \"source_id\": \"BR-RSPC-034\",\n    \"purpose\": \"Verify that financial request, verification, approval, escalation and transaction-record events are logged for audit.\",\n    \"preconditions\": \"Faculty, RSPC Admin, Dean-RSPC and Director users exist; delegated limits represented such that the request escalates.\",\n    \"action_or_input\": \"Faculty submits a financial request; RSPC Admin verifies it; it is escalated to Director; Director approves; a transaction record is recorded. Then retrieve the audit/reporting record.\",\n    \"expected_result\": \"The audit record contains one entry for each lifecycle event (request, verification, escalation, approval, transaction record) with actor and time.\",\n    \"test_type\": \"audit\"\n  },\n  {\n    \"test_id\": \"BR-022\",\n    \"source_id\": \"BR-RSPC-035 within sanctioned budget\",\n    \"purpose\": \"Verify that a procurement request within the sanctioned project budget is advanced as eligible.\",\n    \"preconditions\": \"A project with a sanctioned budget represented in RSPC; Faculty is the project owner.\",\n    \"action_or_input\": \"Faculty submits a procurement request whose cost is within the remaining sanctioned budget.\",\n    \"expected_result\": \"The request passes budget validation and is advanced as eligible to approval.\",\n    \"test_type\": \"validation-positive\"\n  },\n  {\n    \"test_id\": \"BR-023\",\n    \"source_id\": \"BR-RSPC-035 exceeds sanctioned budget\",\n    \"purpose\": \"Verify that a procurement request exceeding the sanctioned project budget is not advanced as eligible.\",\n    \"preconditions\": \"A project with a sanctioned budget represented in RSPC; Faculty is the project owner.\",\n    \"action_or_input\": \"Faculty submits a procurement request whose cost exceeds the remaining sanctioned budget.\",\n    \"expected_result\": \"The request fails budget validation and is not advanced as eligible; a validation message is returned.\",\n    \"test_type\": \"validation-negative\"\n  },\n  {\n    \"test_id\": \"BR-024\",\n    \"source_id\": \"BR-RSPC-036 permitted (represented hierarchy followed)\",\n    \"purpose\": \"Verify that an eligible procurement request is routed through the represented approval stages in order.\",\n    \"preconditions\": \"An eligible procurement request; a represented procurement approval hierarchy; approver users exist.\",\n    \"action_or_input\": \"Each applicable approver in the represented hierarchy acts in order.\",\n    \"expected_result\": \"The request moves through exactly the represented stages in order and is approved after the final applicable stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-025\",\n    \"source_id\": \"BR-RSPC-036 prohibited (hierarchy bypass)\",\n    \"purpose\": \"Verify that a procurement request cannot be approved by an approver outside its current applicable stage.\",\n    \"preconditions\": \"An eligible procurement request pending at the first applicable approval stage.\",\n    \"action_or_input\": \"An approver of a later stage (e.g. Director) attempts to approve the request before earlier stages are complete.\",\n    \"expected_result\": \"The action is rejected; the request remains at its current stage.\",\n    \"test_type\": \"routing-negative\"\n  },\n  {\n    \"test_id\": \"BR-026\",\n    \"source_id\": \"BR-RSPC-037 schedule due date reached\",\n    \"purpose\": \"Verify that a report becomes due/pending and a reminder is raised according to the represented reporting schedule.\",\n    \"preconditions\": \"A project with a represented reporting schedule whose next report due date has been reached; no report submitted for that period.\",\n    \"action_or_input\": \"Evaluate the project's report status / run the reminder processing.\",\n    \"expected_result\": \"The report for the period is shown as due/pending and a reminder notification is generated for the responsible Faculty.\",\n    \"test_type\": \"timing\"\n  },\n  {\n    \"test_id\": \"BR-027\",\n    \"source_id\": \"BR-RSPC-037 schedule due date not reached\",\n    \"purpose\": \"Verify that no due/pending status or reminder is generated before the represented schedule's due date.\",\n    \"preconditions\": \"A project with a represented reporting schedule whose next due date is in the future.\",\n    \"action_or_input\": \"Evaluate the project's report status / run the reminder processing.\",\n    \"expected_result\": \"No report is shown as pending/overdue for that period and no reminder is generated.\",\n    \"test_type\": \"timing\"\n  },\n  {\n    \"test_id\": \"BR-028\",\n    \"source_id\": \"BR-RSPC-038 authorized actor\",\n    \"purpose\": \"Verify that an authorized actor can access historical progress reports throughout the project lifecycle.\",\n    \"preconditions\": \"A project owned by Faculty A with several submitted progress reports, including after the project has advanced to a later lifecycle state (e.g. closed).\",\n    \"action_or_input\": \"Faculty A requests the project's historical progress reports.\",\n    \"expected_result\": \"All historical progress reports of the project are returned.\",\n    \"test_type\": \"access-positive\"\n  },\n  {\n    \"test_id\": \"BR-029\",\n    \"source_id\": \"BR-RSPC-038 unauthorized actor\",\n    \"purpose\": \"Verify that an actor outside the authorized role/project scope cannot access historical progress reports.\",\n    \"preconditions\": \"A project owned by Faculty A with submitted progress reports; Faculty B has no role on the project.\",\n    \"action_or_input\": \"Faculty B requests the project's historical progress reports.\",\n    \"expected_result\": \"Access is denied (or no reports of that project are returned).\",\n    \"test_type\": \"access-negative\"\n  },\n  {\n    \"test_id\": \"BR-030\",\n    \"source_id\": \"BR-RSPC-039 authorized actor\",\n    \"purpose\": \"Verify that an authorized actor can access historical utilization reports throughout the project lifecycle.\",\n    \"preconditions\": \"A project owned by Faculty A with several submitted utilization reports, including after the project has advanced to a later lifecycle state.\",\n    \"action_or_input\": \"Faculty A requests the project's historical utilization reports.\",\n    \"expected_result\": \"All historical utilization reports of the project are returned.\",\n    \"test_type\": \"access-positive\"\n  },\n  {\n    \"test_id\": \"BR-031\",\n    \"source_id\": \"BR-RSPC-039 unauthorized actor\",\n    \"purpose\": \"Verify that an actor outside the authorized role/project scope cannot access historical utilization reports.\",\n    \"preconditions\": \"A project owned by Faculty A with submitted utilization reports; Faculty B has no role on the project.\",\n    \"action_or_input\": \"Faculty B requests the project's historical utilization reports.\",\n    \"expected_result\": \"Access is denied (or no reports of that project are returned).\",\n    \"test_type\": \"access-negative\"\n  },\n  {\n    \"test_id\": \"BR-032\",\n    \"source_id\": \"BR-RSPC-043 closure approved\",\n    \"purpose\": \"Verify that a completed project whose closure is approved is archived as closed with its audit trail retained.\",\n    \"preconditions\": \"A completed project with a prior audit trail and a submitted closure record pending final closure approval.\",\n    \"action_or_input\": \"The applicable approver records closure approval.\",\n    \"expected_result\": \"The project is shown as archived/closed and its complete RSPC audit trail remains retrievable.\",\n    \"test_type\": \"lifecycle\"\n  },\n  {\n    \"test_id\": \"BR-033\",\n    \"source_id\": \"BR-RSPC-043 closure not approved\",\n    \"purpose\": \"Verify that a project is not archived when closure approval has not been recorded.\",\n    \"preconditions\": \"A completed project with a submitted closure record still pending approval (or rejected).\",\n    \"action_or_input\": \"Retrieve the project's status without closure approval being recorded.\",\n    \"expected_result\": \"The project is not archived/closed.\",\n    \"test_type\": \"lifecycle-negative\"\n  },\n  {\n    \"test_id\": \"BR-034\",\n    \"source_id\": \"BR-RSPC-045 configured integration\",\n    \"purpose\": \"Verify that information supplied through an explicitly configured integration is processed as RSPC integration data.\",\n    \"preconditions\": \"An integration source is explicitly represented/configured for RSPC.\",\n    \"action_or_input\": \"The configured integration supplies RSPC-relevant information.\",\n    \"expected_result\": \"The information is accepted and recorded in RSPC.\",\n    \"test_type\": \"integration-positive\"\n  },\n  {\n    \"test_id\": \"BR-035\",\n    \"source_id\": \"BR-RSPC-045 unconfigured integration\",\n    \"purpose\": \"Verify that information from an integration not configured for RSPC is not processed.\",\n    \"preconditions\": \"An integration source that is not represented/configured for RSPC.\",\n    \"action_or_input\": \"The unconfigured source supplies RSPC-relevant information.\",\n    \"expected_result\": \"The information is rejected/ignored and no RSPC record is created or changed.\",\n    \"test_type\": \"integration-negative\"\n  },\n  {\n    \"test_id\": \"BR-036\",\n    \"source_id\": \"BR-RSPC-048 authorized scope\",\n    \"purpose\": \"Verify that a user can view RSPC project data within their authorized role and record scope.\",\n    \"preconditions\": \"Faculty A owns proposal P-A.\",\n    \"action_or_input\": \"Faculty A requests the list of proposals and the details of P-A.\",\n    \"expected_result\": \"P-A is included in the list and its details are returned.\",\n    \"test_type\": \"access-positive\"\n  },\n  {\n    \"test_id\": \"BR-037\",\n    \"source_id\": \"BR-RSPC-048 outside authorized scope\",\n    \"purpose\": \"Verify that a user cannot view RSPC data outside their authorized role and record scope.\",\n    \"preconditions\": \"Faculty A owns proposal P-A; Faculty B has only the Faculty role and no relation to P-A.\",\n    \"action_or_input\": \"Faculty B requests the list of proposals and the details of P-A.\",\n    \"expected_result\": \"P-A is not included in Faculty B's list and the detail request is denied (or reports not found).\",\n    \"test_type\": \"access-negative\"\n  },\n  {\n    \"test_id\": \"BR-038\",\n    \"source_id\": \"BR-RSPC-049 permitted action\",\n    \"purpose\": \"Verify that a user can perform an RSPC action allowed by their assigned role.\",\n    \"preconditions\": \"A proposal pending at the HoD stage; user with the HoD role for the department.\",\n    \"action_or_input\": \"HoD records a recommendation on the proposal.\",\n    \"expected_result\": \"The action is accepted and the decision is recorded.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-039\",\n    \"source_id\": \"BR-RSPC-049 unauthorized action blocked\",\n    \"purpose\": \"Verify that a user cannot perform an RSPC action not allowed by their assigned role.\",\n    \"preconditions\": \"A proposal pending at the HoD stage; a user holding only the Faculty role.\",\n    \"action_or_input\": \"The Faculty user attempts to record the HoD decision on the proposal.\",\n    \"expected_result\": \"The action is blocked as unauthorized; the proposal and its decision history are unchanged.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-040\",\n    \"source_id\": \"BR-RSPC-050\",\n    \"purpose\": \"Verify that auditable RSPC events/record changes are retained in the RSPC audit log.\",\n    \"preconditions\": \"Faculty and reviewer users exist.\",\n    \"action_or_input\": \"Faculty submits a proposal and a reviewer records a decision; retrieve the RSPC audit/history log for the proposal.\",\n    \"expected_result\": \"The log contains entries for the submission and the decision, each identifying the actor, action and time.\",\n    \"test_type\": \"audit\"\n  },\n  {\n    \"test_id\": \"BR-041\",\n    \"source_id\": \"BR-RSPC-053 authorized mechanism\",\n    \"purpose\": \"Verify that a role assignment supplied through the authorized Fusion role-management mechanism is applied to RSPC access.\",\n    \"preconditions\": \"A user without any RSPC role.\",\n    \"action_or_input\": \"Assign the HoD RSPC role to the user through the authorized Fusion role-management mechanism; the user then attempts an HoD action.\",\n    \"expected_result\": \"The assignment is applied; the user is permitted to perform the HoD action.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-042\",\n    \"source_id\": \"BR-RSPC-053 unauthorized source\",\n    \"purpose\": \"Verify that role-assignment information not supplied through the authorized mechanism is not applied.\",\n    \"preconditions\": \"A user holding only the Faculty role.\",\n    \"action_or_input\": \"Supply role-assignment information outside the authorized mechanism (e.g. the user attempts to assign themselves the Dean-RSPC role through an RSPC request), then attempt a Dean-RSPC action.\",\n    \"expected_result\": \"The assignment is not applied; the Dean-RSPC action is blocked.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-043\",\n    \"source_id\": \"BR-RSPC-054 authorized mechanism\",\n    \"purpose\": \"Verify that a role reassignment supplied through the authorized mechanism is applied to RSPC access.\",\n    \"preconditions\": \"User U holds the HoD RSPC role; user V holds no HoD role.\",\n    \"action_or_input\": \"Reassign the HoD role from U to V through the authorized Fusion role-management mechanism; V attempts an HoD action.\",\n    \"expected_result\": \"The reassignment is applied; V is permitted to perform the HoD action.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-044\",\n    \"source_id\": \"BR-RSPC-054 unauthorized source\",\n    \"purpose\": \"Verify that role-reassignment information not supplied through the authorized mechanism is not applied.\",\n    \"preconditions\": \"User U holds the HoD RSPC role; user V holds only the Faculty role.\",\n    \"action_or_input\": \"Supply reassignment information outside the authorized mechanism (e.g. V or U attempts to transfer the HoD role through an RSPC request), then V attempts an HoD action.\",\n    \"expected_result\": \"The reassignment is not applied; V's HoD action is blocked and U retains HoD access.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-045\",\n    \"source_id\": \"BR-RSPC-055\",\n    \"purpose\": \"Verify that an authorized role change takes effect immediately for RSPC access (new access granted, old access withdrawn).\",\n    \"preconditions\": \"User U holds the HoD role and can perform HoD actions; a proposal is pending at the HoD stage.\",\n    \"action_or_input\": \"Through the authorized mechanism, remove U's HoD role and grant it to V; immediately (no re-login or delay) U and V each attempt the HoD action.\",\n    \"expected_result\": \"U's attempt is blocked and V's attempt is permitted, without any waiting period.\",\n    \"test_type\": \"authorization\"\n  },\n  {\n    \"test_id\": \"BR-046\",\n    \"source_id\": \"BR-RSPC-058\",\n    \"purpose\": \"Verify that RSPC processing of staff-appointment information is limited to records/status and does not execute HR or payroll actions.\",\n    \"preconditions\": \"An approved project staff appointment with stipend information.\",\n    \"action_or_input\": \"Record a stipend/payment-related status update for the appointment in RSPC.\",\n    \"expected_result\": \"RSPC stores the status/record only; no HR master-data change or payroll/payment execution is performed by RSPC.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-047\",\n    \"source_id\": \"BR-RSPC-059\",\n    \"purpose\": \"Verify that RSPC processing of financial/settlement information is limited to request, approval, status and transaction records without accounting or bank-payment execution.\",\n    \"preconditions\": \"An approved financial request.\",\n    \"action_or_input\": \"Record a transaction/settlement record for the request in RSPC.\",\n    \"expected_result\": \"RSPC stores the transaction/status record only; no ledger posting, bank payment or disbursement execution is performed by RSPC.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-048\",\n    \"source_id\": \"BR-RSPC-060\",\n    \"purpose\": \"Verify that RSPC processing of procurement or asset-declaration information is limited to request/validation/approval/status records.\",\n    \"preconditions\": \"An approved procurement request.\",\n    \"action_or_input\": \"Record a procurement status update / asset declaration in RSPC.\",\n    \"expected_result\": \"RSPC stores the status/asset record only; no purchase order, vendor or stock-master operation is executed by RSPC.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-049\",\n    \"source_id\": \"BR-RSPC-061 notification triggered\",\n    \"purpose\": \"Verify that an RSPC notification event is recorded/triggered through the represented Fusion channels.\",\n    \"preconditions\": \"Faculty and HoD users exist.\",\n    \"action_or_input\": \"Faculty submits a proposal (a notification-triggering RSPC event).\",\n    \"expected_result\": \"A notification event for the responsible reviewer is recorded/triggered through the Fusion dashboard (and email) channel.\",\n    \"test_type\": \"notification\"\n  },\n  {\n    \"test_id\": \"BR-050\",\n    \"source_id\": \"BR-RSPC-061 stated exception (external delivery failure)\",\n    \"purpose\": \"Verify that a failure of the external email-delivery infrastructure does not affect the RSPC action or expand RSPC behaviour.\",\n    \"preconditions\": \"The platform email-delivery service is unavailable / raises a delivery failure.\",\n    \"action_or_input\": \"Faculty submits a proposal (a notification-triggering RSPC event).\",\n    \"expected_result\": \"The RSPC submission still succeeds and the RSPC notification event is recorded; RSPC does not fail the action because of the external delivery failure.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-051\",\n    \"source_id\": \"BR-RSPC-062\",\n    \"purpose\": \"Verify that RSPC only stores/tracks represented external funding-agency information and does not execute the external agency process.\",\n    \"preconditions\": \"A project with a represented external funding-agency submission/disbursement tracking field.\",\n    \"action_or_input\": \"Record an external funding-agency submission or disbursement status in RSPC.\",\n    \"expected_result\": \"The status is stored as tracking information only; no external agency submission or disbursement is executed by RSPC.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-052\",\n    \"source_id\": \"BR-RSPC-063\",\n    \"purpose\": \"Verify that RSPC consumes Fusion authentication/role information and enforces it without administering platform identity.\",\n    \"preconditions\": \"RSPC endpoints are available.\",\n    \"action_or_input\": \"Send an unauthenticated request to an RSPC data endpoint.\",\n    \"expected_result\": \"The request is rejected as unauthenticated by the Fusion authentication mechanism; no RSPC data is returned.\",\n    \"test_type\": \"scope-boundary\"\n  },\n  {\n    \"test_id\": \"BR-053\",\n    \"source_id\": \"BR-RSPC-065 update permitted in current lifecycle state\",\n    \"purpose\": \"Verify that Faculty can update project details when the current lifecycle state permits the update.\",\n    \"preconditions\": \"Faculty A owns a proposal/project in a lifecycle state that permits editing (e.g. draft / returned for revision).\",\n    \"action_or_input\": \"Faculty A updates the project details.\",\n    \"expected_result\": \"The update is saved and the new values are returned.\",\n    \"test_type\": \"lifecycle\"\n  },\n  {\n    \"test_id\": \"BR-054\",\n    \"source_id\": \"BR-RSPC-065 update not permitted in current lifecycle state\",\n    \"purpose\": \"Verify that Faculty cannot update project details when the current lifecycle state does not permit the update.\",\n    \"preconditions\": \"Faculty A owns a proposal/project in a lifecycle state that does not permit editing (e.g. submitted and under review, or closed).\",\n    \"action_or_input\": \"Faculty A attempts to update the project details.\",\n    \"expected_result\": \"The update is rejected; stored values are unchanged.\",\n    \"test_type\": \"lifecycle-negative\"\n  },\n  {\n    \"test_id\": \"BR-055\",\n    \"source_id\": \"BR-RSPC-066 eligible verification outcome\",\n    \"purpose\": \"Verify that RSPC Admin forwards a request to the next approving authority when verification is eligible.\",\n    \"preconditions\": \"A proposal recommended by HoD and pending RSPC Admin verification.\",\n    \"action_or_input\": \"RSPC Admin records an eligible verification outcome and forwards.\",\n    \"expected_result\": \"The request advances to the Dean-RSPC stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-056\",\n    \"source_id\": \"BR-RSPC-066 ineligible verification outcome\",\n    \"purpose\": \"Verify that a request with an ineligible verification outcome does not advance as eligible.\",\n    \"preconditions\": \"A proposal recommended by HoD and pending RSPC Admin verification.\",\n    \"action_or_input\": \"RSPC Admin records an ineligible (incomplete/non-compliant) verification outcome.\",\n    \"expected_result\": \"The request does not advance to the Dean-RSPC stage; it is not shown as eligible.\",\n    \"test_type\": \"routing-negative\"\n  },\n  {\n    \"test_id\": \"BR-057\",\n    \"source_id\": \"BR-RSPC-067 recommended\",\n    \"purpose\": \"Verify that HoD forwards a request to the next stage when the departmental recommendation is recorded as recommended.\",\n    \"preconditions\": \"A submitted proposal pending at the HoD stage.\",\n    \"action_or_input\": \"HoD records the recommendation as recommended.\",\n    \"expected_result\": \"The recommendation is recorded and the request advances to the RSPC Admin stage.\",\n    \"test_type\": \"routing\"\n  },\n  {\n    \"test_id\": \"BR-058\",\n    \"source_id\": \"BR-RSPC-067 not recommended\",\n    \"purpose\": \"Verify that a non-recommended request is recorded without being forwarded as recommended.\",\n    \"preconditions\": \"A submitted proposal pending at the HoD stage.\",\n    \"action_or_input\": \"HoD records the recommendation as not recommended.\",\n    \"expected_result\": \"The non-recommendation is recorded in the decision history; the request does not advance to the RSPC Admin stage as recommended.\",\n    \"test_type\": \"routing-negative\"\n  },\n  {\n    \"test_id\": \"BR-059\",\n    \"source_id\": \"BR-RSPC-068 outside authority (forward/escalate); BR-RSPC-004 Dean does not finalize\",\n    \"purpose\": \"Verify that Dean-RSPC cannot record final approval of an eligible request outside its represented authority; the forwarding/escalation path applies.\",\n    \"preconditions\": \"An eligible request at Dean-RSPC whose represented path requires Director action (outside Dean-RSPC authority).\",\n    \"action_or_input\": \"Dean-RSPC attempts to record final approval of the request.\",\n    \"expected_result\": \"Final approval at Dean-RSPC is not recorded; the request is forwarded/escalated to the Director stage (or remains pending) and is not shown as approved.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-060\",\n    \"source_id\": \"BR-RSPC-068 ineligible request\",\n    \"purpose\": \"Verify that Dean-RSPC cannot approve a request that has not been routed to Dean-RSPC as eligible.\",\n    \"preconditions\": \"A request whose RSPC Admin verification outcome is ineligible (or not yet verified).\",\n    \"action_or_input\": \"Dean-RSPC attempts to approve the request.\",\n    \"expected_result\": \"The approval is rejected; the request is not marked approved.\",\n    \"test_type\": \"authorization-negative\"\n  },\n  {\n    \"test_id\": \"BR-061\",\n    \"source_id\": \"BR-RSPC-070 unrepresented external policy not invented\",\n    \"purpose\": \"Verify that an external policy/threshold that is not represented/configured in RSPC does not alter RSPC behaviour.\",\n    \"preconditions\": \"No proposal policy validation and no Director-escalation threshold is represented/configured in RSPC.\",\n    \"action_or_input\": \"Faculty submits a complete proposal with a large budget value and it is processed by the reviewers.\",\n    \"expected_result\": \"The proposal is processed on the stated route without any validation failure or Director escalation attributed to an unrepresented external policy value.\",\n    \"test_type\": \"scope-boundary\"\n  }\n]\n"
}
```

#### Tool result

````
File created successfully at: /home/nikhit/Documents/Fusion/Fusion-Integrated/a8_design/BR_DESIGN.json (file state is current in your context — no need to Read it back)
````

### Tool call: `Bash` — 2026-11-10T21:00:30.537Z

```json
{
  "command": "python3 -c \"\nimport json;d=json.load(open('a8_design/BR_DESIGN.json'));print(len(d));import re\nids=sorted({m for t in d for m in re.findall(r'BR-RSPC-\\d{3}',t['source_id'])});print(len(ids),ids)\nassert all(set(t)=={'test_id','source_id','purpose','preconditions','action_or_input','expected_result','test_type'} for t in d)\"\ncat >> a8_logs/br/LOG.md <<'EOF'\n- 21:10 Generated the design (Prompt A output) and saved unchanged as `a8_design/BR_DESIGN.json`:\n  61 test cases BR-001..BR-061, valid JSON, exactly the 7 required fields each.\n  All 38 active BR IDs appear as source_id. Rules with explicit permitted/prohibited outcomes,\n  threshold sides or stated exceptions have one case per outcome.\n- Step A complete. Not yet frozen (Step B: obligations.md, gap check, SHA-256).\nEOF",
  "description": "Validate the design JSON and log Step A"
}
```

#### Tool result

````
61
38 ['BR-RSPC-004', 'BR-RSPC-005', 'BR-RSPC-006', 'BR-RSPC-012', 'BR-RSPC-013', 'BR-RSPC-014', 'BR-RSPC-015', 'BR-RSPC-016', 'BR-RSPC-022', 'BR-RSPC-026', 'BR-RSPC-032', 'BR-RSPC-033', 'BR-RSPC-034', 'BR-RSPC-035', 'BR-RSPC-036', 'BR-RSPC-037', 'BR-RSPC-038', 'BR-RSPC-039', 'BR-RSPC-043', 'BR-RSPC-045', 'BR-RSPC-048', 'BR-RSPC-049', 'BR-RSPC-050', 'BR-RSPC-053', 'BR-RSPC-054', 'BR-RSPC-055', 'BR-RSPC-058', 'BR-RSPC-059', 'BR-RSPC-060', 'BR-RSPC-061', 'BR-RSPC-062', 'BR-RSPC-063', 'BR-RSPC-065', 'BR-RSPC-066', 'BR-RSPC-067', 'BR-RSPC-068', 'BR-RSPC-069', 'BR-RSPC-070']
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:00:33.619Z

```json
{
  "recap": "Step A for BR is done: a8_design/BR_DESIGN.json has 61 test cases, and all 38 active business rules appear as a source_id. The design is not frozen yet, and nothing is committed.",
  "ask": "Shall I go on to Step B (obligations list, gap check, freeze)?",
  "actions": [
    {
      "label": "Do Step B"
    }
  ]
}
```

#### Tool result

````
Shown in the next-step box. Your closing message is your answer to the user: write it now, in full, as the last thing you say this turn. The box asks your question, so do not ask it again.
````

## Claude — 2026-11-10T21:00:43.017Z

Step A for strategy BR is done. The design is in [a8_design/BR_DESIGN.json](a8_design/BR_DESIGN.json): 61 test cases (BR-001 to BR-061). It's valid JSON and each case has exactly the seven required fields.

**What I read:** only the handoff file, the Problem Statement (`a8_plain/01_*`) and the Business Rule spec (`a8_plain/04_*`). I opened no implementation code, tests, other specs, other strategies' files or git history.

**Coverage:**
- The spec has 38 active business rules, and every one appears as a `source_id`. The 32 retired legacy IDs have no rule text, so I didn't treat them as test obligations.
- Where a rule states different outcomes, there is a separate case for each, per the Section-7 rule. For example:
  - Director-only approvals (BR-RSPC-005 and 006): one case where the Director approves, one where someone else tries and is blocked.
  - Missing mandatory proposal fields (BR-RSPC-013).
  - The Dean's delegated limit (BR-RSPC-032/033): one case within the limit, one over it.
  - The procurement budget check (BR-RSPC-035).
  - Access by an authorized vs. unauthorized user (BR-RSPC-038, 039 and 048).
  - Role changes through the proper role-management route vs. any other route (BR-RSPC-053 and 054).
  - Edits allowed vs. not allowed in the current project state (BR-RSPC-065).
  - HoD recommends vs. doesn't recommend (BR-RSPC-067).
  - Admin verification eligible vs. ineligible (BR-RSPC-066).
- Stated exceptions also get their own cases: the Director stage not applying (BR-RSPC-012, 022 and 026), and email delivery failing (BR-RSPC-061).
- The six scope-boundary rules (BR-RSPC-058 to 063) each have one case.

**Logs:** the filled-in Prompt A is in [a8_logs/br/PROMPT_A.txt](a8_logs/br/PROMPT_A.txt), and [a8_logs/br/LOG.md](a8_logs/br/LOG.md) records the start time (20:57:55 UTC) and these steps.

Nothing is frozen or committed yet. Step B would write `obligations.md`, check for gaps (and add cases once if any obligation is missing), then save the SHA-256 to `FROZEN.txt`.

## User — 2026-11-10T21:01:30.015Z

Do Step B

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:01:34.258Z

```json
{
  "items": [
    {
      "content": "Write obligations.md with coverage mapping",
      "status": "in_progress"
    },
    {
      "content": "Check gaps and freeze with SHA-256",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (2 steps).
````

### Tool call: `Bash` — 2026-11-10T21:01:55.960Z

```json
{
  "command": "cat > a8_logs/br/obligations.md <<'EOF'\n# BR obligations → test cases (Step B)\n\nSource: `04_RSPC_Business_Rule_Specifications_v1.3` (38 active BRs) + Problem Statement.\nObligation = each active BR, split into each explicitly stated distinct outcome\n(permitted/prohibited, threshold side, condition true/false, stated exception) per the Section-7 BR rule.\nRetired legacy IDs (32) have no rule statement and are not obligations.\n\n| # | Obligation | Test(s) | Covered |\n|---|---|---|---|\n| 1 | BR-RSPC-004 Dean forwards Director-required request to Director (not finalized at Dean) | BR-001, BR-059 | yes |\n| 2 | BR-RSPC-005 permitted: Director records approval of large funding request | BR-002 | yes |\n| 3 | BR-RSPC-005 prohibited: only Director may record it | BR-003 | yes |\n| 4 | BR-RSPC-006 permitted: Director authorizes high-value expenditure | BR-004 | yes |\n| 5 | BR-RSPC-006 prohibited: only Director may authorize | BR-005 | yes |\n| 6 | BR-RSPC-012 route F→HoD→Admin→Dean→Director (Director applicable) | BR-006 | yes |\n| 7 | BR-RSPC-012 exception: Director stage not applicable | BR-007 | yes |\n| 8 | BR-RSPC-012 stages followed in order (no stage skipped) | BR-008 (also BR-006) | yes |\n| 9 | BR-RSPC-013 mandatory fields complete → submitted/advanced | BR-009 | yes |\n| 10 | BR-RSPC-013 mandatory field incomplete → not advanced (objectives, timelines, budget, funding source, resource requirements) | BR-010 | yes |\n| 11 | BR-RSPC-014 represented validation fails → advancement prevented | BR-011 | yes |\n| 12 | BR-RSPC-014 represented validation passes → advances | BR-012 | yes |\n| 13 | BR-RSPC-015 decision timestamp recorded | BR-013 | yes |\n| 14 | BR-RSPC-016 decision remarks recorded | BR-014 | yes |\n| 15 | BR-RSPC-022 consultancy: HoD/Director stages applicable | BR-015 | yes |\n| 16 | BR-RSPC-022 exception: HoD/Director stages not applicable | BR-016 | yes |\n| 17 | BR-RSPC-026 staff appointment → Dean-RSPC (Director not applicable) | BR-017 | yes |\n| 18 | BR-RSPC-026 staff appointment → Dean-RSPC → Director (applicable) | BR-018 | yes |\n| 19 | BR-RSPC-032 within delegated powers → Dean approves | BR-019 | yes |\n| 20 | BR-RSPC-032 beyond delegated powers → escalation path | BR-020 | yes |\n| 21 | BR-RSPC-033 condition true → routed to Director | BR-020 | yes |\n| 22 | BR-RSPC-033 condition false → not routed to Director | BR-019 | yes |\n| 23 | BR-RSPC-034 financial lifecycle events logged (request, verification, approval, escalation, transaction) | BR-021 | yes |\n| 24 | BR-RSPC-035 within sanctioned budget → eligible | BR-022 | yes |\n| 25 | BR-RSPC-035 exceeds sanctioned budget → not eligible | BR-023 | yes |\n| 26 | BR-RSPC-036 represented procurement hierarchy followed | BR-024 | yes |\n| 27 | BR-RSPC-036 hierarchy bypass blocked | BR-025 | yes |\n| 28 | BR-RSPC-037 due date reached → pending status + reminder | BR-026 | yes |\n| 29 | BR-RSPC-037 due date not reached → no pending/reminder | BR-027 | yes |\n| 30 | BR-RSPC-038 authorized actor sees historical progress reports (whole lifecycle) | BR-028 | yes |\n| 31 | BR-RSPC-038 unauthorized actor denied | BR-029 | yes |\n| 32 | BR-RSPC-039 authorized actor sees historical utilization reports (whole lifecycle) | BR-030 | yes |\n| 33 | BR-RSPC-039 unauthorized actor denied | BR-031 | yes |\n| 34 | BR-RSPC-043 closure approved → archived with audit trail | BR-032 | yes |\n| 35 | BR-RSPC-043 closure not approved → not archived | BR-033 | yes |\n| 36 | BR-RSPC-045 configured integration processed | BR-034 | yes |\n| 37 | BR-RSPC-045 unconfigured integration not processed | BR-035 | yes |\n| 38 | BR-RSPC-048 authorized data displayed | BR-036 | yes |\n| 39 | BR-RSPC-048 data outside scope not displayed | BR-037 | yes |\n| 40 | BR-RSPC-049 permitted action allowed | BR-038 | yes |\n| 41 | BR-RSPC-049 unauthorized action blocked | BR-039 | yes |\n| 42 | BR-RSPC-050 audit/compliance log retained | BR-040 | yes |\n| 43 | BR-RSPC-053 assignment via authorized mechanism applied | BR-041 | yes |\n| 44 | BR-RSPC-053 assignment from other source not applied | BR-042 | yes |\n| 45 | BR-RSPC-054 reassignment via authorized mechanism applied | BR-043 | yes |\n| 46 | BR-RSPC-054 reassignment from other source not applied | BR-044 | yes |\n| 47 | BR-RSPC-055 authorized role change effective immediately | BR-045 | yes |\n| 48 | BR-RSPC-058 no HR/payroll execution (records/status only) | BR-046 | yes |\n| 49 | BR-RSPC-059 no accounting/bank-payment execution | BR-047 | yes |\n| 50 | BR-RSPC-060 no procurement/inventory execution | BR-048 | yes |\n| 51 | BR-RSPC-061 notification triggered via Fusion channels | BR-049 | yes |\n| 52 | BR-RSPC-061 exception: external delivery failure does not expand RSPC scope | BR-050 | yes |\n| 53 | BR-RSPC-062 external funding-agency process not executed (tracking only) | BR-051 | yes |\n| 54 | BR-RSPC-063 platform auth consumed, not administered | BR-052 | yes |\n| 55 | BR-RSPC-065 lifecycle-permitted update saved | BR-053 | yes |\n| 56 | BR-RSPC-065 non-permitted update rejected | BR-054 | yes |\n| 57 | BR-RSPC-066 eligible verification → forwarded | BR-055 | yes |\n| 58 | BR-RSPC-066 ineligible verification → not advanced | BR-056 | yes |\n| 59 | BR-RSPC-067 recommended → forwarded | BR-057 | yes |\n| 60 | BR-RSPC-067 not recommended → recorded, not forwarded | BR-058 | yes |\n| 61 | BR-RSPC-068 eligible within authority → Dean approves | BR-007 | yes |\n| 62 | BR-RSPC-068 outside authority → forward/escalate, not finalized | BR-059 | yes |\n| 63 | BR-RSPC-068 ineligible request → Dean may not approve | BR-060 | yes |\n| 64 | BR-RSPC-069 condition true → enters Director stage | BR-006 | yes |\n| 65 | BR-RSPC-069 condition false → does not enter Director stage | BR-007 | yes |\n| 66 | BR-RSPC-070 represented policy applied | BR-011 | yes |\n| 67 | BR-RSPC-070 unrepresented external value not invented | BR-061 | yes |\n\n**Coverage:** 38/38 active BRs; 67/67 distinct outcome obligations covered.\n\n**Gaps:** none → no design completion step needed; no cases appended.\n\n**Untestable obligations:** none excluded at design level. Note for Step C (not a design change):\nseveral obligations concern behaviour (consultancy, staff, finance, procurement, reporting,\nclosure, integration, notifications) that may have no implementation interface; those will be\nhandled as `NOT_AUTOMATED: <reason>` skips per Prompt B if so.\nEOF\nsha256sum a8_design/BR_DESIGN.json",
  "description": "Write obligations mapping and hash the design"
}
```

#### Tool result

````
aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca  a8_design/BR_DESIGN.json
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:01:58.435Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 2 is in progress.
````

### Tool call: `Bash` — 2026-11-10T21:02:01.838Z

```json
{
  "command": "T=$(date -u '+%H:%M'); cat > a8_logs/br/FROZEN.txt <<EOF\na8_design/BR_DESIGN.json\nSHA-256: aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca\nFrozen: 2026-11-10 $T UTC\nTest cases: 61 (BR-001..BR-061)\nEOF\ncat >> a8_logs/br/LOG.md <<EOF\n\n## Step B — freeze\n- $T Wrote \\`a8_logs/br/obligations.md\\`: 38/38 active BRs, 67/67 distinct outcome obligations covered.\n- Gap check: no missing obligations → design completion not used; no cases appended.\n- Untestable at design level: none excluded.\n- Frozen: SHA-256 aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca → \\`a8_logs/br/FROZEN.txt\\`.\n- Waiting for Nikhit's \"continue\" before Step C.\nEOF\nsha256sum -c <<< \"aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca  a8_design/BR_DESIGN.json\"",
  "description": "Write FROZEN.txt, log Step B, verify hash"
}
```

#### Tool result

````
a8_design/BR_DESIGN.json: OK
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:02:05.363Z

```json
{
  "recap": "The BR design is frozen with 61 test cases, and all 38 active rules and 67 distinct outcomes are covered with no gaps. The hash is saved in FROZEN.txt. Nothing is committed yet; Step C waits for your \"continue\"."
}
```

#### Tool result

````
Nothing is pending, so the app draws no box; the recap is the session's status. Your closing message is your answer to the user: write it now, as the last thing you say this turn.
````

## Claude — 2026-11-10T21:02:12.192Z

I've done Step B for BR, and the design is now frozen.

**Counts:**
- **Business rules covered:** all 38 of the active rules.
- **Obligations covered:** all 67 distinct outcomes. These include allowed vs. blocked outcomes, both sides of a threshold, conditions that hold and don't hold, and stated exceptions.
- **Test cases:** 61, BR-001 to BR-061. Some tests cover more than one obligation; for example, BR-007 covers BR-RSPC-012's exception, BR-RSPC-068's allowed case and BR-RSPC-069's false case.
- **Gaps:** none, so I didn't use the one-time chance to add cases.
- **Untestable obligations:** none excluded at the design stage.

The obligation-to-test mapping is in [a8_logs/br/obligations.md](a8_logs/br/obligations.md). [a8_logs/br/FROZEN.txt](a8_logs/br/FROZEN.txt) holds the design's SHA-256, `aaf14277…b652cca`, which I checked against the file. I also logged the step in [a8_logs/br/LOG.md](a8_logs/br/LOG.md).

In Step C, many cases will probably become `NOT_AUTOMATED` skips: the handoff says the code only implements the research-proposal workflow, so things like consultancy, staff, finance, procurement, reporting, closure, integration and notifications likely have no interface to test against.

Nothing is committed. Say "continue" when you want me to start Step C.

## User — 2026-11-10T21:03:22.137Z

continue

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:03:25.419Z

```json
{
  "items": [
    {
      "content": "Write Prompt B and read RSPC implementation",
      "status": "in_progress"
    },
    {
      "content": "Write BR tests under tests/a8/br",
      "status": "pending"
    },
    {
      "content": "Snapshot raw tests",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (3 steps).
````

### Tool call: `Bash` — 2026-11-10T21:03:30.298Z

```json
{
  "command": "cat > a8_logs/br/PROMPT_B.txt <<'EOF'\nYou are given:\n1. the frozen A8_BASE Fusion implementation, and\n2. the frozen BR_DESIGN.json.\n\nConvert these test designs into executable automated backend tests using pytest/pytest-django.\n\nRules:\n- Implement exactly the supplied test cases.\n- Do not add, remove, merge or reinterpret test cases.\n- Preserve each specified expected result.\n- Do not modify production code.\n- Use the Django isolated test database.\n- Reuse existing Fusion test infrastructure where appropriate.\n- Do not mock the behavior being tested; mocks may be used only for unavailable external dependencies.\n- Do not use xfail to hide failures.\n- Every test must contain its test_id and source_id in its name or docstring.\n- Store generated tests only under tests/a8/br/.\n\nIf a test genuinely cannot be automated using the available interfaces, create it as a skipped pytest test with: NOT_AUTOMATED: <reason>. Do not replace it with a different test.\nEOF\necho \"\n## Step C — implement\n- $(date -u +%H:%M) Received \\\"continue\\\". Wrote \\`a8_logs/br/PROMPT_B.txt\\`. Reading implementation (excluding modules/rspc/tests/).\" >> a8_logs/br/LOG.md\nfind modules/rspc -path modules/rspc/tests -prune -o -type f -name '*.py' -print | grep -v migrations | xargs wc -l; ls tests tests/a8 2>/dev/null; cat conftest.py | head -150; cat pytest.ini setup.cfg pyproject.toml 2>/dev/null | grep -A10 -i pytest",
  "description": "Save Prompt B and survey RSPC module and test infra"
}
```

#### Tool result

````
   56 modules/rspc/registry.py
   56 modules/rspc/models.py
    7 modules/rspc/apps.py
    0 modules/rspc/__init__.py
  243 modules/rspc/api/views.py
   41 modules/rspc/api/urls.py
   75 modules/rspc/api/serializers.py
    0 modules/rspc/api/__init__.py
  478 total
tests:
__init__.py
__pycache__
a8

tests/a8:
__init__.py
__pycache__
fr
uc
"""Shared fixtures. `stub_iam` replaces the IAM client with an in-memory fake,
so the suite runs with no network and no Fusion_System_Administrator."""
import sys

import pytest

from fusion_auth import client as iam_client
from fusion_auth.client import IamSession, UserRef
from fusion_auth.principal import Principal


class FakeIam:
    """Mirrors IamClient exactly. If the real client grows a method, add it
    here too — a fake that has drifted is worse than no fake."""

    def __init__(self, session=None, users=None, standings=None):
        self.session, self.users = session, users or {}
        #: Override to make the identity service disagree with the projection.
        self.employees = None
        self.standings = standings or {}
        self.calls = []
        self.login_result = "tok-123"      # override per test
        self.login_error = None
        self.standings_error = None
        self.directory_error = None
        self.directory = {"count": 0, "limit": 50, "offset": 0, "results": []}
        self.filters = {"disciplines": [], "batch_years": [], "programmes": []}

    def login(self, username, password):
        self.calls.append(("login", username))
        if self.login_error:
            raise self.login_error
        return self.login_result

    def logout(self, auth_token):
        self.calls.append(("logout", auth_token))

    def resolve_session(self, *, auth_token=None, cookies=None):
        self.calls.append(("resolve_session", auth_token))
        return self.session

    def get_users(self, user_ids):
        ids = list(user_ids)
        self.calls.append(("get_users", tuple(sorted(ids))))
        return {i: self.users[i] for i in ids if i in self.users}

    def search_users(self, q="", kind=None, limit=25):
        return list(self.users.values())[:limit]

    def employee_page(self, *, limit=500, offset=0):
        rows = self._employees()
        return {"count": len(rows), "limit": limit, "offset": offset,
                "results": rows[offset:offset + limit]}

    def count_employees(self):
        return len(self._employees())

    def iter_employees(self, *, page_size=500):
        yield from self._employees()

    def _employees(self):
        """Whoever the test put in `users` who is not a student."""
        if self.employees is not None:
            return list(self.employees)
        from modules.directory.models import UserRef
        return list(UserRef.objects.filter(
            kind__in=("faculty", "staff"), is_active=True))

    def academic_directory(self, **filters):
        self.calls.append(("academic_directory", tuple(sorted(filters.items()))))
        if self.directory_error:
            raise self.directory_error
        return self.directory

    def academic_filters(self):
        self.calls.append(("academic_filters", ()))
        if self.directory_error:
            raise self.directory_error
        return self.filters

    def get_academic_standings(self, user_ids):
        """A student absent from `standings` has no declared result, which is
        what the eligibility engine must fail closed on."""
        ids = list(user_ids)
        self.calls.append(("get_academic_standings", tuple(sorted(ids))))
        if self.standings_error:
            raise self.standings_error
        return {i: self.standings[i] for i in ids if i in self.standings}


def make_session(user_id=1001, permissions=(), modules=(), kind="student",
                 roles=("student",), active_role="student"):
    return IamSession(
        user_id=user_id, username=f"u{user_id}", display_name=f"User {user_id}",
        kind=kind, active_role=active_role, roles=tuple(roles),
        permissions=frozenset(permissions), modules=tuple(modules),
    )


def make_principal(**kw):
    return Principal.from_session(make_session(**kw))


@pytest.fixture(autouse=True)
def _clear_throttle_state():
    """Throttle counters live in the cache and would otherwise carry from one
    test into the next — the sixth request of a run failing wherever it landed."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def stub_iam(monkeypatch):
    fake = FakeIam()

    def _install(session=None, users=None):
        fake.session = session
        fake.users = users or {}
        # `from ... import get_client` binds the name in every importer, so
        # patching the source alone lets the real client leak through. A
        # hand-maintained list goes stale silently; sys.modules does not.
        patched = 0
        for mod in list(sys.modules.values()):
            if mod is None:
                continue
            name = getattr(mod, "__name__", "")
            if not name.startswith(("fusion_auth", "modules", "core", "config")):
                continue
            if getattr(mod, "get_client", None) is not None:
                monkeypatch.setattr(mod, "get_client", lambda: fake)
                patched += 1
        monkeypatch.setattr(iam_client, "get_client", lambda: fake)
        assert patched, "no get_client bindings were found to patch"
        return fake

    _install()
    return _install


@pytest.fixture
def user_ref():
    def _make(user_id, name="Asha Verma", kind="student", discipline="CSE"):
        return UserRef(user_id=user_id, username=f"u{user_id}", display_name=name,
                       kind=kind, discipline=discipline)
    return _make
    "pytest>=8.3",
    "pytest-django>=4.9",
    "pytest-cov>=5.0",
    "factory-boy>=3.3",
    "freezegun>=1.5",
    "ruff>=0.6",
    "import-linter>=2.0",
    "responses>=0.25",
]

[tool.ruff]
line-length = 100
target-version = "py312"
--
[tool.pytest.ini_options]
# `--ds` rather than DJANGO_SETTINGS_MODULE: pytest-django lets the
# environment variable win over this file, and a developer exporting
# config.settings.dev would then run a different suite from CI.
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-q --no-header --ds=config.settings.test"
testpaths = ["modules", "core", "fusion_auth"]
````

### Tool call: `Bash` — 2026-11-10T21:03:33.449Z

```json
{
  "command": "cd modules/rspc; cat registry.py models.py apps.py api/urls.py api/serializers.py api/views.py",
  "description": "Read the RSPC module source"
}
```

#### Tool result

````
"""What the server tells the shell about this module (ADR-0010).

Nav items carry `required_permission` and the server filters before sending —
the client does zero filtering, so a link a role cannot use never reaches the
browser at all.
"""
MODULE = {
    "code": "rspc", "label": "RSPC", "icon": "Flask",
    "base_path": "/rspc", "nav_section": "Research", "sort_order": 30,
    "status": "active",
}

PERMISSIONS = [
    ("rspc.proposal.submit", "Submit a research project proposal"),
    ("rspc.proposal.view_self", "View own proposals"),
    ("rspc.proposal.recommend", "Recommend a proposal from the department"),
    ("rspc.proposal.verify", "Verify a department-recommended proposal"),
    ("rspc.proposal.decide", "Decide an admin-verified proposal"),
    ("rspc.proposal.authorize", "Authorize a proposal forwarded to Director"),
    ("rspc.proposal.view_queue", "View the review queue"),
]

ROLE_GRANTS = {
    "Faculty": ["rspc.proposal.submit", "rspc.proposal.view_self"],
    "HoD": ["rspc.proposal.recommend", "rspc.proposal.view_queue"],
    "RSPC Admin": ["rspc.proposal.verify", "rspc.proposal.view_queue"],
    "Dean-RSPC": ["rspc.proposal.decide", "rspc.proposal.view_queue"],
    "Director": ["rspc.proposal.authorize", "rspc.proposal.view_queue"],
}

NAV_ITEMS = [
    {
        "code": "rspc.submit",
        "label": "Submit Proposal",
        "icon": "PaperPlane",
        "to": "/rspc/submit",
        "required_permission": "rspc.proposal.submit",
        "sort_order": 5,
    },
    {
        "code": "rspc.mine",
        "label": "My Proposals",
        "icon": "UserCheck",
        "to": "/rspc/mine",
        "required_permission": "rspc.proposal.view_self",
        "sort_order": 10,
    },
    {
        "code": "rspc.queue",
        "label": "Review Queue",
        "icon": "CalendarBlank",
        "to": "/rspc/queue",
        "required_permission": "rspc.proposal.view_queue",
        "sort_order": 20,
    },
]
from django.db import models

from core.db.mixins import TimeStampedModel

# -- ResearchProposal --------------------------------------------------------
class ResearchProposal(TimeStampedModel):
    STATUS = [
        ("draft", "Draft"), ("submitted", "Submitted"),
        ("dept_recommended", "Dept. Recommended"),
        ("dept_not_recommended", "Dept. Not Recommended"),
        ("admin_verified", "Admin Verified"),
        ("not_eligible", "Not Eligible"),
        ("approved", "Approved"),
        ("dean_not_approved", "Dean Not Approved"),
        ("director_not_approved", "Director Not Approved"),
        ("forwarded_to_director", "Forwarded to Director"),
    ]

    title = models.CharField(max_length=255)
    objectives = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    funding_agency = models.TextField(blank=True, default="")
    resource_requirements = models.TextField(blank=True, default="")
    department = models.CharField(max_length=100, blank=True, default="")
    pi_id = models.IntegerField()
    status = models.CharField(max_length=24, choices=STATUS, default="draft")

    class Meta:
        db_table = "rspc_research_proposal"
        indexes = [
            models.Index(fields=["status"], name="research_proposal_status_idx"),
        ]

    def __str__(self) -> str:
        return f"prop#{self.pk} {self.title} {self.status}"


# -- ProposalDecision --------------------------------------------------------
class ProposalDecision(models.Model):
    proposal = models.ForeignKey(ResearchProposal, on_delete=models.CASCADE,
                                related_name="decisions")
    stage = models.CharField(max_length=50)  # "HoD", "RSPC Admin", "Dean-RSPC", "Director"
    actor_id = models.IntegerField(null=True, blank=True)  # Fusion user id
    outcome = models.CharField(max_length=24)  # "recommended" or "not eligible"
    remarks = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rspc_proposal_decision"
        indexes = [models.Index(fields=["proposal", "stage", "decided_at"],
                                name="decision_proposal_idx")]

    def __str__(self) -> str:
        return f"prop#{self.proposal_id} {self.stage} {self.outcome}"
# modules/rspc/apps.py
from django.apps import AppConfig


class RspcConfig(AppConfig):
    name = "modules.rspc"
    label = "rspc"
from django.urls import path

from modules.rspc.api import views as v

urlpatterns = [
    path(
        'proposals/',
        v.ResearchProposalView.as_view(),
        name='proposal-create',
    ),
    path(
        'proposals/mine/',
        v.ResearchProposalMineView.as_view(),
        name='proposal-mine',
    ),
    path(
        'proposals/queue/',
        v.ResearchProposalQueueView.as_view(),
        name='proposal-queue',
    ),
    path(
        'proposals/<int:proposal_id>/recommend/',
        v.ProposalDecisionView.as_view(),
        name='proposal-recommend',
    ),
    path(
        'proposals/<int:proposal_id>/verify/',
        v.ProposalVerifyView.as_view(),
        name='proposal-verify',
    ),
    path(
        'proposals/<int:proposal_id>/decide/',
        v.ProposalDecideView.as_view(),
        name='proposal-decide',
    ),
    path(
        'proposals/<int:proposal_id>/authorize/',
        v.ProposalAuthorizeView.as_view(),
        name='proposal-authorize',
    ),
]
from rest_framework import serializers

from modules.rspc.models import ProposalDecision, ResearchProposal


class ProposalDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalDecision
        fields = [
            'id',
            'proposal',
            'stage',
            'actor_id',
            'outcome',
            'remarks',
            'decided_at'
        ]
        read_only_fields = [
            'proposal',
            'stage',
            'actor_id',
            'outcome',
            'remarks',
            'decided_at'
        ]


class ResearchProposalSerializer(serializers.ModelSerializer):
    decisions = ProposalDecisionSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchProposal
        fields = [
            'id',
            'title',
            'objectives',
            'start_date',
            'end_date',
            'budget',
            'funding_agency',
            'resource_requirements',
            'department',
            'pi_id',
            'status',
            'decisions'
        ]
        read_only_fields = [
            'pi_id',
            'status'
        ]
        extra_kwargs = {
            'start_date': {"required": True, "allow_null": False},
            'end_date': {"required": True, "allow_null": False},
            'budget': {"required": True, "allow_null": False},
            'funding_agency': {"required": True, "allow_null": False, "allow_blank": False},
            'resource_requirements': {"required": True, "allow_null": False, "allow_blank": False}
        }

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        budget = data.get('budget')

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date.")

        if budget is not None and budget <= 0:
            raise serializers.ValidationError("Budget must be greater than zero.")

        return data


class ProposalActionSerializer(serializers.Serializer):
    outcome = serializers.CharField()
    remarks = serializers.CharField(required=False, allow_blank=True)
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from fusion_auth.permissions import HasModuleGrant, HasPermission
from modules.rspc.api.serializers import ProposalActionSerializer, ResearchProposalSerializer
from modules.rspc.models import ProposalDecision, ResearchProposal

MODULE = HasModuleGrant("rspc")

@extend_schema(request=ResearchProposalSerializer, responses=ResearchProposalSerializer)
class ResearchProposalView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.submit")]

    def post(self, request):
        data = request.data
        serializer = ResearchProposalSerializer(data=data)
        if serializer.is_valid():
            serializer.save(pi_id=request.user.user_id, status="submitted")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(responses=ResearchProposalSerializer(many=True))
class ResearchProposalMineView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.view_self")]

    def get(self, request):
        proposals = ResearchProposal.objects.filter(pi_id=request.user.user_id)
        serializer = ResearchProposalSerializer(proposals, many=True)
        return Response(serializer.data)

@extend_schema(responses=ResearchProposalSerializer(many=True))
class ResearchProposalQueueView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.view_queue")]

    def get(self, request):
        if request.principal.has_permission("rspc.proposal.recommend"):
            status = "submitted"
        elif request.principal.has_permission("rspc.proposal.verify"):
            status = "dept_recommended"
        elif request.principal.has_permission("rspc.proposal.decide"):
            status = "admin_verified"
        elif request.principal.has_permission("rspc.proposal.authorize"):
            status = "forwarded_to_director"
        else:
            raise ValidationError("User does not have permission to view queue.")

        proposals = ResearchProposal.objects.filter(status=status)
        serializer = ResearchProposalSerializer(proposals, many=True)
        return Response(serializer.data)

@extend_schema(request=ProposalActionSerializer, responses=OpenApiTypes.OBJECT)
class ProposalDecisionView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.recommend")]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(ResearchProposal, pk=proposal_id)
        data = request.data
        outcome = data.get('outcome')
        remarks = data.get("remarks", "")

        if outcome not in ['recommended', 'not_recommended']:
            raise ValidationError(
                "Invalid outcome. Must be 'recommended' or 'not_recommended'."
            )

        if proposal.status != "submitted":
            raise ValidationError(
                "Proposal must be in 'submitted' status to recommend."
            )

        decision = ProposalDecision(
            proposal=proposal,
            stage="HoD",
            actor_id=request.user.user_id,
            outcome=outcome,
            remarks=remarks
        )
        decision.save()

        proposal.status = "dept_recommended" if outcome == "recommended" else "dept_not_recommended"
        proposal.save()

        return Response(
            {'message': 'Proposal recommended successfully'},
            status=status.HTTP_200_OK
        )

@extend_schema(request=ProposalActionSerializer, responses=OpenApiTypes.OBJECT)
class ProposalVerifyView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.verify")]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(ResearchProposal, pk=proposal_id)
        data = request.data
        outcome = data.get('outcome')
        remarks = data.get("remarks", "")

        if outcome not in ['eligible', 'not_eligible']:
            raise ValidationError(
                "Invalid outcome. Must be 'eligible' or 'not_eligible'."
            )

        if proposal.status != "dept_recommended":
            raise ValidationError(
                "Proposal must be in 'dept_recommended' status to verify."
            )

        decision = ProposalDecision(
            proposal=proposal,
            stage="RSPC Admin",
            actor_id=request.user.user_id,
            outcome=outcome,
            remarks=remarks
        )
        decision.save()

        proposal.status = "admin_verified" if outcome == "eligible" else "not_eligible"
        proposal.save()

        return Response(
            {'message': 'Proposal verified successfully'},
            status=status.HTTP_200_OK
        )

@extend_schema(request=ProposalActionSerializer, responses=OpenApiTypes.OBJECT)
class ProposalDecideView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.decide")]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(ResearchProposal, pk=proposal_id)
        data = request.data
        outcome = data.get('outcome')
        remarks = data.get("remarks", "")

        if outcome not in ['approve', 'forward', 'not_approve']:
            raise ValidationError(
                "Invalid outcome. Must be 'approve', 'forward', or 'not_approve'."
            )

        if proposal.status == "admin_verified":
            if outcome == "approve":
                proposal.status = "approved"
                proposal.save()
                decision = ProposalDecision(
                    proposal=proposal,
                    stage="Dean-RSPC",
                    actor_id=request.user.user_id,
                    outcome=outcome,
                    remarks=remarks
                )
                decision.save()
            elif outcome == "forward":
                proposal.status = "forwarded_to_director"
                proposal.save()
                decision = ProposalDecision(
                    proposal=proposal,
                    stage="Dean-RSPC",
                    actor_id=request.user.user_id,
                    outcome=outcome,
                    remarks=remarks
                )
                decision.save()
            elif outcome == "not_approve":
                proposal.status = "dean_not_approved"
                proposal.save()
                decision = ProposalDecision(
                    proposal=proposal,
                    stage="Dean-RSPC",
                    actor_id=request.user.user_id,
                    outcome=outcome,
                    remarks=remarks
                )
                decision.save()
            else:
                raise ValidationError(
                    "Proposal must be in 'admin_verified' status to decide."
                )
        else:
            raise ValidationError(
                "Proposal status does not allow this action."
            )

        return Response(
            {'message': 'Proposal decision made successfully'},
            status=status.HTTP_200_OK
        )

@extend_schema(request=ProposalActionSerializer, responses=OpenApiTypes.OBJECT)
class ProposalAuthorizeView(APIView):
    permission_classes = [MODULE, HasPermission("rspc.proposal.authorize")]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(ResearchProposal, pk=proposal_id)
        data = request.data
        outcome = data.get('outcome')
        remarks = data.get("remarks", "")

        if outcome not in ['approve', 'not_approve']:
            raise ValidationError(
                "Invalid outcome. Must be 'approve' or 'not_approve'."
            )

        if proposal.status == "forwarded_to_director":
            if outcome == "approve":
                proposal.status = "approved"
                proposal.save()
                decision = ProposalDecision(
                    proposal=proposal,
                    stage="Director",
                    actor_id=request.user.user_id,
                    outcome=outcome,
                    remarks=remarks
                )
                decision.save()
            elif outcome == "not_approve":
                proposal.status = "director_not_approved"
                proposal.save()
                decision = ProposalDecision(
                    proposal=proposal,
                    stage="Director",
                    actor_id=request.user.user_id,
                    outcome=outcome,
                    remarks=remarks
                )
                decision.save()
            else:
                raise ValidationError(
                    "Proposal must be in 'forwarded_to_director' status to authorize."
                )
        else:
            raise ValidationError(
                "Proposal status does not allow this action."
            )

        return Response(
            {'message': 'Proposal authorization made successfully'},
            status=status.HTTP_200_OK
        )
````

### Tool call: `Bash` — 2026-11-10T21:03:38.265Z

```json
{
  "command": "cd /home/nikhit/Documents/Fusion/Fusion-Integrated; ls fusion_auth; cat fusion_auth/permissions.py; sed -n 1,200p fusion_auth/authentication.py 2>/dev/null; grep -rn \"rspc\" config/ --include=*.py | head; grep -n \"REST_FRAMEWORK\" -A25 config/settings/base.py",
  "description": "Read auth permissions, authentication and settings"
}
```

#### Tool result

````
__init__.py
__pycache__
apps.py
authentication.py
checks.py
client.py
permissions.py
principal.py
serializers.py
tests
urls.py
views.py
"""Two gates on every request, both server-side.

    HasModuleGrant   is this module yours at all?   (coarse — drives the sidebar)
    HasPermission    may you do this action?        (fine)

Both must pass. The default is deny: a view that declares nothing gets
IsAuthenticatedPrincipal and nothing more, so forgetting to think about
authorization fails closed rather than open.
"""
from rest_framework.permissions import BasePermission


class IsAuthenticatedPrincipal(BasePermission):
    message = "Authentication required."

    def has_permission(self, request, view):
        return getattr(request, "principal", None) is not None


class _HasModuleGrant(BasePermission):
    module_code = ""
    message = "This module is not available to your role."

    def has_permission(self, request, view):
        p = getattr(request, "principal", None)
        return p is not None and p.has_module(self.module_code)


def HasModuleGrant(module_code: str):                       # noqa: N802
    return type("HasModuleGrant_" + module_code,
                (_HasModuleGrant,), {"module_code": module_code})


class _HasPermission(BasePermission):
    codes: tuple[str, ...] = ()
    require_all = False
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        p = getattr(request, "principal", None)
        if p is None:
            return False
        if self.require_all:
            return all(p.has_permission(c) for c in self.codes)
        return p.has_any_permission(*self.codes)


def HasPermission(*codes: str, require_all: bool = False):  # noqa: N802
    return type("HasPermission_" + "_".join(codes).replace(".", "_"),
                (_HasPermission,), {"codes": codes, "require_all": require_all})
"""DRF authentication against Fusion_System_Administrator.

Accepts either the httpOnly cookie the SPA carries, or an
`Authorization: Token ...` header for scripts and service calls. Both are
resolved by asking IAM who the holder is — this service never checks a
password and never reads a user table.
"""
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.api import csrf
from fusion_auth.client import IamUnavailable, get_client
from fusion_auth.principal import Principal


class IamSessionAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        # Forwarded as a header: the IAM names its cookie differently.
        token = self._token_from(request)
        # Only a cookie is ambient, so only a cookie needs the CSRF check.
        from_cookie = token is None
        token = token or request.COOKIES.get(settings.IAM_AUTH_COOKIE_NAME)
        if not token:
            return None                       # anonymous; permissions decide

        try:
            session = get_client().resolve_session(auth_token=token)
        except IamUnavailable as exc:
            # Fail closed but honestly: a 401 would blame the user for our outage.
            raise AuthenticationFailed(
                f"Identity service unavailable: {exc}"
            ) from exc

        if session is None:
            raise AuthenticationFailed("Invalid or expired credentials.")

        if from_cookie:
            csrf.require(request, token)

        principal = Principal.from_session(session)
        request.principal = principal
        return (principal, token)

    def _token_from(self, request):
        header = request.META.get("HTTP_AUTHORIZATION", "")
        if header.startswith(self.keyword + " "):
            return header[len(self.keyword) + 1:].strip()
        return None

    def authenticate_header(self, request):
        return self.keyword
config/urls.py:19:    path("api/v1/rspc/", include("modules.rspc.api.urls")),
config/settings/base.py:93:    "modules.rspc",
195:REST_FRAMEWORK = {
196-    "DEFAULT_AUTHENTICATION_CLASSES": [
197-        "fusion_auth.authentication.IamSessionAuthentication",
198-    ],
199-    "DEFAULT_PERMISSION_CLASSES": [
200-        "fusion_auth.permissions.IsAuthenticatedPrincipal",
201-    ],
202-    "DEFAULT_PAGINATION_CLASS": "core.api.pagination.CursorPagination",
203-    "PAGE_SIZE": 25,
204-    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
205-    "EXCEPTION_HANDLER": "core.api.exceptions.exception_handler",
206-    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
207-    "UNAUTHENTICATED_USER": None,
208-    # Unset, DRF throttles on the whole client-controlled X-Forwarded-For.
209-    "NUM_PROXIES": env_int("DJANGO_NUM_PROXIES", 1),
210-    # Not DRF's ScopedRateThrottle: it keys on request.user.pk, absent here.
211-    "DEFAULT_THROTTLE_CLASSES": ["core.api.throttling.PrincipalScopedThrottle"],
212-    # Only endpoints opting in via `throttle_scope` are limited.
213-    "DEFAULT_THROTTLE_RATES": {
214-        "recruiter_login": "5/min",
215-        "recruiter_invite_accept": "10/hour",
216-        "apply": "30/hour",
217-        "export": "5/hour",
218-        "upload": "20/hour",
219-        "directory_search": "120/hour",
220-    },
````

### Tool call: `Bash` — 2026-11-10T21:03:41.785Z

```json
{
  "command": "sed -n 1,80p fusion_auth/principal.py; sed -n 1,60p core/api/exceptions.py; grep -n \"IamSession\\b\" -A15 fusion_auth/client.py | head -30",
  "description": "Read Principal, exception handler and IamSession"
}
```

#### Tool result

````
"""The authenticated actor.

Called `principal`, not `user`, deliberately: there is no Django user behind
it. It is a value object built from what IAM said, and it is what every
permission check reads.
"""
from __future__ import annotations

from dataclasses import dataclass

from fusion_auth.client import IamSession


@dataclass(frozen=True)
class Principal:
    user_id: int
    username: str
    display_name: str
    kind: str
    active_role: str | None
    roles: tuple[str, ...]
    permissions: frozenset[str]
    modules: tuple[str, ...]
    #: Built by the IAM so one sidebar can span every Fusion app.
    navigation: tuple[dict, ...] = ()
    email: str = ""

    # DRF pokes at these on request.user
    is_authenticated: bool = True
    is_anonymous: bool = False

    @classmethod
    def from_session(cls, s: IamSession) -> Principal:
        return cls(
            user_id=s.user_id, username=s.username, display_name=s.display_name,
            kind=s.kind, active_role=s.active_role, roles=s.roles,
            permissions=s.permissions, modules=s.modules, email=s.email,
            navigation=s.navigation,
        )

    def has_permission(self, code: str) -> bool:
        return code in self.permissions

    def has_any_permission(self, *codes: str) -> bool:
        return any(c in self.permissions for c in codes)

    def has_module(self, code: str) -> bool:
        return code in self.modules

    def __str__(self) -> str:
        return f"{self.username}({self.user_id})"
"""One error envelope for the whole platform:

    {"error": {"code": ..., "message": ..., "details": [...], "request_id": ...}}

`request_id` is always present, so a user reads it off a toast and support
greps one id across the logs.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_handler

from core.observability.middleware import get_request_id


class DomainError(Exception):
    """Base for errors raised by domain/ and services/.

    Deliberately not a DRF exception — a service must stay callable from a
    Celery task or a management command, where HTTP status is noise.
    """

    code = "domain_error"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "The request could not be processed."

    def __init__(self, message=None, *, code=None, details=None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.code = code or self.code
        self.details = details or []


class BadRequestError(DomainError):
    """The request itself is malformed — a non-numeric id, an unparseable
    filter. Distinct from ConflictError's 409, which means the request was
    well-formed and the resource refused it."""

    code = "bad_request"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "The request could not be understood."


class NotFoundError(DomainError):
    code = "not_found"
    status_code = status.HTTP_404_NOT_FOUND
    message = "Not found."


class ConflictError(DomainError):
    code = "conflict"
    status_code = status.HTTP_409_CONFLICT
    message = "The resource is not in a state that allows this."


class AuthenticationFailedError(DomainError):
    """A credential was rejected: 401 "we do not know who you are", as opposed
    to PermissionDeniedError's 403 "we know, and no". Collapsing the two makes
    an auth outage indistinguishable from a misconfigured grant in the logs."""

    code = "invalid_credentials"
28:class IamSession:
29-    """The authenticated principal, as IAM describes it."""
30-
31-    user_id: int
32-    username: str
33-    display_name: str
34-    kind: str                       # student | faculty | staff | operator
35-    active_role: str | None = None
36-    roles: tuple[str, ...] = ()
37-    permissions: frozenset[str] = frozenset()
38-    modules: tuple[str, ...] = ()
39-    #: The whole sidebar. Empty from an older IAM, and the caller falls back.
40-    navigation: tuple[dict, ...] = ()
41-    email: str = ""
42-
43-    def has_permission(self, code: str) -> bool:
--
111:                        cookies: dict | None = None) -> IamSession | None:
112-        """Who is holding this credential? None means 'not authenticated'."""
113-        key = None
114-        ttl = settings.IAM_SESSION_CACHE_SECONDS
115-        if auth_token and ttl:
116-            key = f"iam:session:{auth_token[:48]}"
117-            hit = cache.get(key)
118-            if hit is not None:
119-                return hit or None            # cached negative stays negative
120-
121-        payload = self._get("iam/v1/me", auth_token=auth_token, cookies=cookies)
122-        session = self._to_session(payload) if payload else None
123-        if key:
````

### Tool call: `Bash` — 2026-11-10T21:04:29.379Z

```json
{
  "command": "grep -rn \"IAM_SESSION_CACHE_SECONDS\\|IAM_AUTH_COOKIE_NAME\" config/settings/; sed -n 1,40p config/settings/test.py; sed -n 100,140p fusion_auth/client.py",
  "description": "Check IAM session cache setting in test config"
}
```

#### Tool result

````
config/settings/base.py:145:IAM_SESSION_CACHE_SECONDS = env_int("IAM_SESSION_CACHE_SECONDS", 60)
config/settings/base.py:146:IAM_AUTH_COOKIE_NAME = env("IAM_AUTH_COOKIE_NAME", "fusion_session")
config/settings/test.py:7:IAM_SESSION_CACHE_SECONDS = 0
from .dev import *

DEBUG = False
# Tests never reach the real IAM — fusion_auth is stubbed via responses/monkeypatch.
IAM_BASE_URL = "http://iam.test"
IAM_SERVICE_TOKEN = "test-token"  # noqa: S105 — test fixture, never a real credential
IAM_SESSION_CACHE_SECONDS = 0
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                      "LOCATION": "test"}}
        if r.status_code >= 500:
            raise IamUnavailable(f"IAM returned {r.status_code}")
        if r.status_code >= 400:
            return None
        try:
            return r.json()
        except ValueError as exc:
            raise IamUnavailable("IAM returned a non-JSON body") from exc

    # -- identity ---------------------------------------------------------
    def resolve_session(self, *, auth_token: str | None = None,
                        cookies: dict | None = None) -> IamSession | None:
        """Who is holding this credential? None means 'not authenticated'."""
        key = None
        ttl = settings.IAM_SESSION_CACHE_SECONDS
        if auth_token and ttl:
            key = f"iam:session:{auth_token[:48]}"
            hit = cache.get(key)
            if hit is not None:
                return hit or None            # cached negative stays negative

        payload = self._get("iam/v1/me", auth_token=auth_token, cookies=cookies)
        session = self._to_session(payload) if payload else None
        if key:
            cache.set(key, session or False, ttl)
        return session

    def forget_session(self, auth_token: str) -> None:
        """Drop the cached session so the next read sees a change immediately."""
        if settings.IAM_SESSION_CACHE_SECONDS:
            cache.delete(f"iam:session:{auth_token[:48]}")

    @staticmethod
    def _to_session(p: dict) -> IamSession | None:
        user = p.get("user") or {}
        uid = user.get("id") or user.get("user_id") or p.get("user_id")
        if uid is None:
            return None
        return IamSession(
            user_id=int(uid),
            username=user.get("username") or p.get("username", ""),
````

## Claude — 2026-11-10T21:04:32.585Z

I've read the RSPC code; only the research-proposal workflow has an API. Now writing the BR test file.

### Tool call: `Bash` — 2026-11-10T21:04:33.885Z

```json
{
  "command": "mkdir -p tests/a8/br && touch tests/a8/br/__init__.py; grep -n \"class TimeStampedModel\" -A8 core/db/mixins.py; python3 -c \"import json;[print(t['test_id'],'|',t['source_id']) for t in json.load(open('a8_design/BR_DESIGN.json'))]\"",
  "description": "Create test folder and list frozen test/source ids"
}
```

#### Tool result

````
4:class TimeStampedModel(models.Model):
5-    created_at = models.DateTimeField(auto_now_add=True)
6-    updated_at = models.DateTimeField(auto_now=True)
7-
8-    class Meta:
9-        abstract = True
10-
11-
12-class UserScopedModel(models.Model):
BR-001 | BR-RSPC-004 condition-true (Director action required)
BR-002 | BR-RSPC-005 permitted (Director records approval of large funding request)
BR-003 | BR-RSPC-005 prohibited (non-Director records Director-stage approval)
BR-004 | BR-RSPC-006 permitted (Director authorizes high-value expenditure)
BR-005 | BR-RSPC-006 prohibited (non-Director authorizes high-value expenditure)
BR-006 | BR-RSPC-012 route with Director applicable; BR-RSPC-069 condition-true
BR-007 | BR-RSPC-012 stated exception (Director stage not applicable); BR-RSPC-069 condition-false; BR-RSPC-068 permitted
BR-008 | BR-RSPC-012 out-of-order stage action prohibited
BR-009 | BR-RSPC-013 condition-true (all mandatory fields complete)
BR-010 | BR-RSPC-013 condition-false (a mandatory field missing)
BR-011 | BR-RSPC-014 represented validation fails; BR-RSPC-070 represented policy applied
BR-012 | BR-RSPC-014 represented validation passes
BR-013 | BR-RSPC-015
BR-014 | BR-RSPC-016
BR-015 | BR-RSPC-022 HoD and Director stages applicable
BR-016 | BR-RSPC-022 stated exception (HoD and Director stages not applicable)
BR-017 | BR-RSPC-026 Director not applicable
BR-018 | BR-RSPC-026 Director applicable
BR-019 | BR-RSPC-032 within delegated powers; BR-RSPC-033 condition-false
BR-020 | BR-RSPC-032 beyond delegated powers; BR-RSPC-033 condition-true
BR-021 | BR-RSPC-034
BR-022 | BR-RSPC-035 within sanctioned budget
BR-023 | BR-RSPC-035 exceeds sanctioned budget
BR-024 | BR-RSPC-036 permitted (represented hierarchy followed)
BR-025 | BR-RSPC-036 prohibited (hierarchy bypass)
BR-026 | BR-RSPC-037 schedule due date reached
BR-027 | BR-RSPC-037 schedule due date not reached
BR-028 | BR-RSPC-038 authorized actor
BR-029 | BR-RSPC-038 unauthorized actor
BR-030 | BR-RSPC-039 authorized actor
BR-031 | BR-RSPC-039 unauthorized actor
BR-032 | BR-RSPC-043 closure approved
BR-033 | BR-RSPC-043 closure not approved
BR-034 | BR-RSPC-045 configured integration
BR-035 | BR-RSPC-045 unconfigured integration
BR-036 | BR-RSPC-048 authorized scope
BR-037 | BR-RSPC-048 outside authorized scope
BR-038 | BR-RSPC-049 permitted action
BR-039 | BR-RSPC-049 unauthorized action blocked
BR-040 | BR-RSPC-050
BR-041 | BR-RSPC-053 authorized mechanism
BR-042 | BR-RSPC-053 unauthorized source
BR-043 | BR-RSPC-054 authorized mechanism
BR-044 | BR-RSPC-054 unauthorized source
BR-045 | BR-RSPC-055
BR-046 | BR-RSPC-058
BR-047 | BR-RSPC-059
BR-048 | BR-RSPC-060
BR-049 | BR-RSPC-061 notification triggered
BR-050 | BR-RSPC-061 stated exception (external delivery failure)
BR-051 | BR-RSPC-062
BR-052 | BR-RSPC-063
BR-053 | BR-RSPC-065 update permitted in current lifecycle state
BR-054 | BR-RSPC-065 update not permitted in current lifecycle state
BR-055 | BR-RSPC-066 eligible verification outcome
BR-056 | BR-RSPC-066 ineligible verification outcome
BR-057 | BR-RSPC-067 recommended
BR-058 | BR-RSPC-067 not recommended
BR-059 | BR-RSPC-068 outside authority (forward/escalate); BR-RSPC-004 Dean does not finalize
BR-060 | BR-RSPC-068 ineligible request
BR-061 | BR-RSPC-070 unrepresented external policy not invented
````

### Tool call: `Write` — 2026-11-10T21:06:21.743Z

```json
{
  "file_path": "/home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py",
  "content": "\"\"\"A8 — Business-Rule-based (BR) tests for RSPC.\n\nGenerated from the frozen design a8_design/BR_DESIGN.json\n(SHA-256 aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca).\nEach test carries its test_id and source_id in its name/docstring.\n\nInterface used: the RSPC REST API under /api/v1/rspc/ (research-proposal workflow).\nIdentity/roles come from the Fusion IAM (an external service); it is replaced by the\nshared `stub_iam` FakeIam from the root conftest, which is the authorized role-management\nmechanism as seen by RSPC. RSPC behaviour itself is never mocked.\n\"\"\"\nfrom datetime import datetime\n\nimport pytest\nfrom django.utils import timezone\nfrom rest_framework.test import APIClient\n\nfrom fusion_auth.client import IamSession\nfrom modules.rspc.models import ResearchProposal\nfrom modules.rspc.registry import ROLE_GRANTS\n\npytestmark = pytest.mark.django_db\n\nBASE = \"/api/v1/rspc/proposals/\"\nMINE = BASE + \"mine/\"\nQUEUE = BASE + \"queue/\"\n\nFACULTY_A, FACULTY_B, HOD, ADMIN, DEAN, DIRECTOR = 1001, 1002, 2001, 2002, 2003, 2004\nROLE_OF = {FACULTY_A: \"Faculty\", FACULTY_B: \"Faculty\", HOD: \"HoD\", ADMIN: \"RSPC Admin\",\n           DEAN: \"Dean-RSPC\", DIRECTOR: \"Director\"}\n\n\ndef iam_session(user_id, roles):\n    \"\"\"Session as the IAM would supply it for `user_id` holding `roles`.\"\"\"\n    perms = frozenset(p for r in roles for p in ROLE_GRANTS[r])\n    return IamSession(\n        user_id=user_id, username=f\"u{user_id}\", display_name=f\"User {user_id}\",\n        kind=\"faculty\", active_role=roles[0] if roles else None, roles=tuple(roles),\n        permissions=perms, modules=(\"rspc\",) if roles else (),\n    )\n\n\ndef valid_payload(**overrides):\n    data = {\n        \"title\": \"Edge AI for crop monitoring\",\n        \"objectives\": \"Build and evaluate a low-power crop-disease detector.\",\n        \"start_date\": \"2026-12-01\",\n        \"end_date\": \"2028-11-30\",\n        \"budget\": \"1500000.00\",\n        \"funding_agency\": \"SERB\",\n        \"resource_requirements\": \"2 JRFs, GPU workstation, field sensors\",\n        \"department\": \"CSE\",\n    }\n    data.update(overrides)\n    return data\n\n\nclass Rspc:\n    \"\"\"Drives the RSPC API as different actors; the IAM fake decides who is calling.\"\"\"\n\n    def __init__(self, fake):\n        self.fake = fake\n        self.client = APIClient()\n        self.client.credentials(HTTP_AUTHORIZATION=\"Token test-token\")\n\n    def as_user(self, user_id, roles=None):\n        if roles is None:\n            roles = [ROLE_OF[user_id]]\n        self.fake.session = iam_session(user_id, roles)\n        return self\n\n    def as_role(self, user_id):\n        return self.as_user(user_id)\n\n    def post(self, user_id, url, data, roles=None):\n        self.as_user(user_id, roles)\n        return self.client.post(url, data, format=\"json\")\n\n    def get(self, user_id, url, roles=None):\n        self.as_user(user_id, roles)\n        return self.client.get(url)\n\n    # -- workflow steps ------------------------------------------------------\n    def submit(self, faculty=FACULTY_A, **overrides):\n        r = self.post(faculty, BASE, valid_payload(**overrides))\n        assert r.status_code == 201, r.content\n        return r.json()[\"id\"]\n\n    def recommend(self, pid, outcome=\"recommended\", remarks=\"\", user=HOD):\n        return self.post(user, f\"{BASE}{pid}/recommend/\",\n                         {\"outcome\": outcome, \"remarks\": remarks})\n\n    def verify(self, pid, outcome=\"eligible\", remarks=\"\", user=ADMIN):\n        return self.post(user, f\"{BASE}{pid}/verify/\", {\"outcome\": outcome, \"remarks\": remarks})\n\n    def decide(self, pid, outcome, remarks=\"\", user=DEAN):\n        return self.post(user, f\"{BASE}{pid}/decide/\", {\"outcome\": outcome, \"remarks\": remarks})\n\n    def authorize(self, pid, outcome, remarks=\"\", user=DIRECTOR):\n        return self.post(user, f\"{BASE}{pid}/authorize/\",\n                         {\"outcome\": outcome, \"remarks\": remarks})\n\n    def to_admin(self, pid):\n        assert self.recommend(pid).status_code == 200\n        return pid\n\n    def to_dean(self, pid):\n        self.to_admin(pid)\n        assert self.verify(pid).status_code == 200\n        return pid\n\n    def to_director(self, pid):\n        self.to_dean(pid)\n        assert self.decide(pid, \"forward\").status_code == 200\n        return pid\n\n    def queue_ids(self, user_id):\n        r = self.get(user_id, QUEUE)\n        assert r.status_code == 200, r.content\n        return {p[\"id\"] for p in r.json()}\n\n    def mine(self, faculty=FACULTY_A):\n        r = self.get(faculty, MINE)\n        assert r.status_code == 200, r.content\n        return {p[\"id\"]: p for p in r.json()}\n\n\ndef status_of(pid):\n    return ResearchProposal.objects.get(pk=pid).status\n\n\ndef decisions_of(pid):\n    return list(ResearchProposal.objects.get(pk=pid).decisions.order_by(\"decided_at\", \"id\"))\n\n\n@pytest.fixture\ndef rspc(stub_iam):\n    return Rspc(stub_iam())\n\n\ndef not_automated(reason):\n    return pytest.mark.skip(reason=f\"NOT_AUTOMATED: {reason}\")\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-004 / 005 / 006 — Director routing and authorization\n# ---------------------------------------------------------------------------\n\ndef test_BR_001_dean_forwards_director_required_request(rspc):\n    \"\"\"BR-001 | source_id: BR-RSPC-004 condition-true (Director action required).\n\n    Dean-RSPC forwards an eligible proposal whose path requires Director action; it must\n    move to the Director stage and not be finalized at Dean-RSPC. (The implementation\n    represents the Director-required path through the Dean's 'forward' decision.)\"\"\"\n    pid = rspc.to_dean(rspc.submit())\n\n    r = rspc.decide(pid, \"forward\", remarks=\"Needs Director approval\")\n\n    assert r.status_code == 200, r.content\n    assert status_of(pid) == \"forwarded_to_director\"\n    assert status_of(pid) != \"approved\"\n    assert pid in rspc.queue_ids(DIRECTOR)\n\n\ndef test_BR_002_director_records_large_funding_approval(rspc):\n    \"\"\"BR-002 | source_id: BR-RSPC-005 permitted (Director records approval of large\n    funding request).\"\"\"\n    pid = rspc.to_director(rspc.submit(budget=\"95000000.00\"))\n\n    r = rspc.authorize(pid, \"approve\", remarks=\"Approved by Director\")\n\n    assert r.status_code == 200, r.content\n    assert status_of(pid) == \"approved\"\n    final = decisions_of(pid)[-1]\n    assert final.stage == \"Director\"\n    assert final.actor_id == DIRECTOR\n    assert final.outcome == \"approve\"\n\n\ndef test_BR_003_non_director_cannot_record_director_approval(rspc):\n    \"\"\"BR-003 | source_id: BR-RSPC-005 prohibited (non-Director records Director-stage\n    approval).\"\"\"\n    pid = rspc.to_director(rspc.submit(budget=\"95000000.00\"))\n\n    r = rspc.authorize(pid, \"approve\", user=DEAN)\n\n    assert r.status_code == 403, r.content\n    assert status_of(pid) == \"forwarded_to_director\"\n    assert not any(d.stage == \"Director\" for d in decisions_of(pid))\n\n\n@not_automated(\"RSPC exposes no expenditure-request interface at A8_BASE; only research \"\n               \"proposals are implemented, so a high-value expenditure cannot be created or \"\n               \"authorized.\")\ndef test_BR_004_director_authorizes_high_value_expenditure():\n    \"\"\"BR-004 | source_id: BR-RSPC-006 permitted (Director authorizes high-value\n    expenditure).\"\"\"\n\n\n@not_automated(\"RSPC exposes no expenditure-request interface at A8_BASE; only research \"\n               \"proposals are implemented, so a high-value expenditure cannot be created or \"\n               \"authorized.\")\ndef test_BR_005_non_director_cannot_authorize_high_value_expenditure():\n    \"\"\"BR-005 | source_id: BR-RSPC-006 prohibited (non-Director authorizes high-value\n    expenditure).\"\"\"\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-012 / 069 — research proposal route\n# ---------------------------------------------------------------------------\n\ndef test_BR_006_full_route_with_director(rspc):\n    \"\"\"BR-006 | source_id: BR-RSPC-012 route with Director applicable; BR-RSPC-069\n    condition-true.\"\"\"\n    pid = rspc.submit()\n    assert status_of(pid) == \"submitted\"\n    assert pid in rspc.queue_ids(HOD)\n\n    assert rspc.recommend(pid).status_code == 200\n    assert pid in rspc.queue_ids(ADMIN)\n    assert pid not in rspc.queue_ids(HOD)\n\n    assert rspc.verify(pid).status_code == 200\n    assert pid in rspc.queue_ids(DEAN)\n    assert pid not in rspc.queue_ids(ADMIN)\n\n    assert rspc.decide(pid, \"forward\").status_code == 200\n    assert pid in rspc.queue_ids(DIRECTOR)\n    assert pid not in rspc.queue_ids(DEAN)\n\n    assert rspc.authorize(pid, \"approve\").status_code == 200\n    assert status_of(pid) == \"approved\"\n    assert [d.stage for d in decisions_of(pid)] == [\"HoD\", \"RSPC Admin\", \"Dean-RSPC\",\n                                                    \"Director\"]\n\n\ndef test_BR_007_director_not_applicable_finalized_at_dean(rspc):\n    \"\"\"BR-007 | source_id: BR-RSPC-012 stated exception (Director stage not applicable);\n    BR-RSPC-069 condition-false; BR-RSPC-068 permitted.\"\"\"\n    pid = rspc.to_dean(rspc.submit())\n\n    r = rspc.decide(pid, \"approve\", remarks=\"Within Dean authority\")\n\n    assert r.status_code == 200, r.content\n    assert status_of(pid) == \"approved\"\n    assert not any(d.stage == \"Director\" for d in decisions_of(pid))\n    assert pid not in rspc.queue_ids(DIRECTOR)\n\n\ndef test_BR_008_later_stage_cannot_act_before_stage_reached(rspc):\n    \"\"\"BR-008 | source_id: BR-RSPC-012 out-of-order stage action prohibited.\"\"\"\n    pid = rspc.submit()\n\n    r = rspc.decide(pid, \"approve\")\n\n    assert 400 <= r.status_code < 500, r.content\n    assert status_of(pid) == \"submitted\"\n    assert decisions_of(pid) == []\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-013 / 014 — proposal validation\n# ---------------------------------------------------------------------------\n\ndef test_BR_009_complete_proposal_submitted(rspc):\n    \"\"\"BR-009 | source_id: BR-RSPC-013 condition-true (all mandatory fields complete).\"\"\"\n    r = rspc.post(FACULTY_A, BASE, valid_payload())\n\n    assert r.status_code == 201, r.content\n    pid = r.json()[\"id\"]\n    assert status_of(pid) == \"submitted\"\n    assert pid in rspc.queue_ids(HOD)\n\n\nMANDATORY_FIELDS = {\n    \"objectives\": [\"objectives\"],\n    \"timelines\": [\"start_date\", \"end_date\"],\n    \"budget\": [\"budget\"],\n    \"funding source\": [\"funding_agency\"],\n    \"resource requirements\": [\"resource_requirements\"],\n}\n\n\n@pytest.mark.parametrize(\"label\", list(MANDATORY_FIELDS))\ndef test_BR_010_missing_mandatory_field_rejected(rspc, label):\n    \"\"\"BR-010 | source_id: BR-RSPC-013 condition-false (a mandatory field missing).\"\"\"\n    fields = MANDATORY_FIELDS[label]\n    payload = valid_payload()\n    for f in fields:\n        payload.pop(f)\n\n    r = rspc.post(FACULTY_A, BASE, payload)\n\n    assert r.status_code == 400, r.content\n    body = r.content.decode()\n    assert any(f in body for f in fields), body\n    assert ResearchProposal.objects.count() == 0\n    assert rspc.queue_ids(HOD) == set()\n\n\n# The validations RSPC represents on proposal values (serializer): budget > 0 and\n# end date not before start date.\nPOLICY_VIOLATIONS = {\n    \"budget must be positive\": {\"budget\": \"0.00\"},\n    \"end date after start date\": {\"start_date\": \"2027-06-01\", \"end_date\": \"2027-01-01\"},\n}\n\n\n@pytest.mark.parametrize(\"label\", list(POLICY_VIOLATIONS))\ndef test_BR_011_represented_policy_validation_fails(rspc, label):\n    \"\"\"BR-011 | source_id: BR-RSPC-014 represented validation fails; BR-RSPC-070\n    represented policy applied.\"\"\"\n    r = rspc.post(FACULTY_A, BASE, valid_payload(**POLICY_VIOLATIONS[label]))\n\n    assert r.status_code == 400, r.content\n    assert ResearchProposal.objects.count() == 0\n\n\ndef test_BR_012_represented_policy_validation_passes(rspc):\n    \"\"\"BR-012 | source_id: BR-RSPC-014 represented validation passes.\"\"\"\n    r = rspc.post(FACULTY_A, BASE, valid_payload(budget=\"10.00\", start_date=\"2027-01-01\",\n                                                 end_date=\"2027-06-01\"))\n\n    assert r.status_code == 201, r.content\n    pid = r.json()[\"id\"]\n    assert status_of(pid) == \"submitted\"\n    assert pid in rspc.queue_ids(HOD)\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-015 / 016 — decision records\n# ---------------------------------------------------------------------------\n\ndef test_BR_013_each_decision_has_timestamp(rspc):\n    \"\"\"BR-013 | source_id: BR-RSPC-015.\"\"\"\n    pid = rspc.submit()\n    before = timezone.now()\n    assert rspc.recommend(pid).status_code == 200\n    assert rspc.verify(pid).status_code == 200\n    assert rspc.decide(pid, \"approve\").status_code == 200\n    after = timezone.now()\n\n    decisions = rspc.mine()[pid][\"decisions\"]\n\n    assert len(decisions) == 3\n    for d in decisions:\n        assert d[\"decided_at\"], d\n        ts = datetime.fromisoformat(d[\"decided_at\"].replace(\"Z\", \"+00:00\"))\n        assert before <= ts <= after\n\n\ndef test_BR_014_each_decision_keeps_remarks(rspc):\n    \"\"\"BR-014 | source_id: BR-RSPC-016.\"\"\"\n    pid = rspc.submit()\n    assert rspc.recommend(pid, remarks=\"HoD: aligned with dept goals\").status_code == 200\n    assert rspc.verify(pid, remarks=\"Admin: documents complete\").status_code == 200\n    assert rspc.decide(pid, \"approve\", remarks=\"Dean: approved\").status_code == 200\n\n    decisions = rspc.mine()[pid][\"decisions\"]\n\n    assert {d[\"stage\"]: d[\"remarks\"] for d in decisions} == {\n        \"HoD\": \"HoD: aligned with dept goals\",\n        \"RSPC Admin\": \"Admin: documents complete\",\n        \"Dean-RSPC\": \"Dean: approved\",\n    }\n\n\n# ---------------------------------------------------------------------------\n# Request types with no interface at A8_BASE\n# ---------------------------------------------------------------------------\n\n@not_automated(\"RSPC exposes no consultancy interface at A8_BASE.\")\ndef test_BR_015_consultancy_route_with_hod_and_director():\n    \"\"\"BR-015 | source_id: BR-RSPC-022 HoD and Director stages applicable.\"\"\"\n\n\n@not_automated(\"RSPC exposes no consultancy interface at A8_BASE.\")\ndef test_BR_016_consultancy_route_without_hod_and_director():\n    \"\"\"BR-016 | source_id: BR-RSPC-022 stated exception (HoD and Director stages not\n    applicable).\"\"\"\n\n\n@not_automated(\"RSPC exposes no staff-appointment interface at A8_BASE.\")\ndef test_BR_017_staff_appointment_finalized_at_dean():\n    \"\"\"BR-017 | source_id: BR-RSPC-026 Director not applicable.\"\"\"\n\n\n@not_automated(\"RSPC exposes no staff-appointment interface at A8_BASE.\")\ndef test_BR_018_staff_appointment_routed_to_director():\n    \"\"\"BR-018 | source_id: BR-RSPC-026 Director applicable.\"\"\"\n\n\n@not_automated(\"RSPC exposes no fund-utilization/expenditure request interface and no \"\n               \"delegated-power configuration at A8_BASE.\")\ndef test_BR_019_financial_request_within_delegated_powers():\n    \"\"\"BR-019 | source_id: BR-RSPC-032 within delegated powers; BR-RSPC-033\n    condition-false.\"\"\"\n\n\n@not_automated(\"RSPC exposes no fund-utilization/expenditure request interface and no \"\n               \"delegated-power configuration at A8_BASE.\")\ndef test_BR_020_financial_request_beyond_delegated_powers():\n    \"\"\"BR-020 | source_id: BR-RSPC-032 beyond delegated powers; BR-RSPC-033\n    condition-true.\"\"\"\n\n\n@not_automated(\"RSPC exposes no financial-request or audit-log interface at A8_BASE.\")\ndef test_BR_021_financial_lifecycle_events_logged():\n    \"\"\"BR-021 | source_id: BR-RSPC-034.\"\"\"\n\n\n@not_automated(\"RSPC exposes no procurement-request interface and no sanctioned-budget \"\n               \"record at A8_BASE.\")\ndef test_BR_022_procurement_within_sanctioned_budget():\n    \"\"\"BR-022 | source_id: BR-RSPC-035 within sanctioned budget.\"\"\"\n\n\n@not_automated(\"RSPC exposes no procurement-request interface and no sanctioned-budget \"\n               \"record at A8_BASE.\")\ndef test_BR_023_procurement_exceeding_sanctioned_budget():\n    \"\"\"BR-023 | source_id: BR-RSPC-035 exceeds sanctioned budget.\"\"\"\n\n\n@not_automated(\"RSPC exposes no procurement-request interface at A8_BASE.\")\ndef test_BR_024_procurement_hierarchy_followed():\n    \"\"\"BR-024 | source_id: BR-RSPC-036 permitted (represented hierarchy followed).\"\"\"\n\n\n@not_automated(\"RSPC exposes no procurement-request interface at A8_BASE.\")\ndef test_BR_025_procurement_hierarchy_bypass_blocked():\n    \"\"\"BR-025 | source_id: BR-RSPC-036 prohibited (hierarchy bypass).\"\"\"\n\n\n@not_automated(\"RSPC exposes no reporting-schedule, report-status or reminder interface \"\n               \"at A8_BASE.\")\ndef test_BR_026_report_due_and_reminder_on_schedule():\n    \"\"\"BR-026 | source_id: BR-RSPC-037 schedule due date reached.\"\"\"\n\n\n@not_automated(\"RSPC exposes no reporting-schedule, report-status or reminder interface \"\n               \"at A8_BASE.\")\ndef test_BR_027_no_report_due_before_schedule():\n    \"\"\"BR-027 | source_id: BR-RSPC-037 schedule due date not reached.\"\"\"\n\n\n@not_automated(\"RSPC exposes no progress-report interface at A8_BASE.\")\ndef test_BR_028_authorized_actor_sees_progress_reports():\n    \"\"\"BR-028 | source_id: BR-RSPC-038 authorized actor.\"\"\"\n\n\n@not_automated(\"RSPC exposes no progress-report interface at A8_BASE.\")\ndef test_BR_029_unauthorized_actor_denied_progress_reports():\n    \"\"\"BR-029 | source_id: BR-RSPC-038 unauthorized actor.\"\"\"\n\n\n@not_automated(\"RSPC exposes no utilization-report interface at A8_BASE.\")\ndef test_BR_030_authorized_actor_sees_utilization_reports():\n    \"\"\"BR-030 | source_id: BR-RSPC-039 authorized actor.\"\"\"\n\n\n@not_automated(\"RSPC exposes no utilization-report interface at A8_BASE.\")\ndef test_BR_031_unauthorized_actor_denied_utilization_reports():\n    \"\"\"BR-031 | source_id: BR-RSPC-039 unauthorized actor.\"\"\"\n\n\n@not_automated(\"RSPC exposes no project-closure or archival interface at A8_BASE.\")\ndef test_BR_032_closure_approved_project_archived():\n    \"\"\"BR-032 | source_id: BR-RSPC-043 closure approved.\"\"\"\n\n\n@not_automated(\"RSPC exposes no project-closure or archival interface at A8_BASE.\")\ndef test_BR_033_closure_not_approved_project_not_archived():\n    \"\"\"BR-033 | source_id: BR-RSPC-043 closure not approved.\"\"\"\n\n\n@not_automated(\"RSPC exposes no integration interface or integration configuration at \"\n               \"A8_BASE.\")\ndef test_BR_034_configured_integration_processed():\n    \"\"\"BR-034 | source_id: BR-RSPC-045 configured integration.\"\"\"\n\n\n@not_automated(\"RSPC exposes no integration interface or integration configuration at \"\n               \"A8_BASE.\")\ndef test_BR_035_unconfigured_integration_not_processed():\n    \"\"\"BR-035 | source_id: BR-RSPC-045 unconfigured integration.\"\"\"\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-048 / 049 / 050 — access control and audit\n# ---------------------------------------------------------------------------\n\ndef test_BR_036_owner_sees_own_proposal(rspc):\n    \"\"\"BR-036 | source_id: BR-RSPC-048 authorized scope.\n\n    RSPC has no single-proposal detail endpoint; the 'mine' list returns each proposal's\n    full details, so the details of P-A are read from it.\"\"\"\n    pid = rspc.submit(faculty=FACULTY_A, title=\"P-A\")\n\n    mine = rspc.mine(FACULTY_A)\n\n    assert pid in mine\n    assert mine[pid][\"title\"] == \"P-A\"\n    assert mine[pid][\"pi_id\"] == FACULTY_A\n\n\ndef test_BR_037_other_faculty_cannot_see_proposal(rspc):\n    \"\"\"BR-037 | source_id: BR-RSPC-048 outside authorized scope.\"\"\"\n    pid = rspc.submit(faculty=FACULTY_A, title=\"P-A\")\n\n    assert pid not in rspc.mine(FACULTY_B)\n    r = rspc.get(FACULTY_B, f\"{BASE}{pid}/\")\n    assert r.status_code in (403, 404), r.content\n    assert b\"P-A\" not in r.content\n\n\ndef test_BR_038_hod_may_record_recommendation(rspc):\n    \"\"\"BR-038 | source_id: BR-RSPC-049 permitted action.\"\"\"\n    pid = rspc.submit()\n\n    r = rspc.recommend(pid, remarks=\"Recommended\")\n\n    assert r.status_code == 200, r.content\n    d = decisions_of(pid)\n    assert len(d) == 1 and d[0].stage == \"HoD\" and d[0].actor_id == HOD\n\n\ndef test_BR_039_faculty_cannot_record_hod_decision(rspc):\n    \"\"\"BR-039 | source_id: BR-RSPC-049 unauthorized action blocked.\"\"\"\n    pid = rspc.submit()\n\n    r = rspc.recommend(pid, user=FACULTY_A)\n\n    assert r.status_code == 403, r.content\n    assert status_of(pid) == \"submitted\"\n    assert decisions_of(pid) == []\n\n\ndef test_BR_040_submission_and_decision_logged(rspc):\n    \"\"\"BR-040 | source_id: BR-RSPC-050.\n\n    The proposal's decision history (returned with the proposal) is the RSPC audit/history\n    record available through the interface.\"\"\"\n    before = timezone.now()\n    pid = rspc.submit()\n    assert rspc.recommend(pid, remarks=\"ok\").status_code == 200\n\n    log = rspc.mine()[pid][\"decisions\"]\n\n    submission = [e for e in log if e[\"actor_id\"] == FACULTY_A]\n    decision = [e for e in log if e[\"actor_id\"] == HOD]\n    assert submission, f\"no submission entry in audit log: {log}\"\n    assert decision, f\"no decision entry in audit log: {log}\"\n    for e in submission + decision:\n        assert e[\"outcome\"]\n        assert datetime.fromisoformat(e[\"decided_at\"].replace(\"Z\", \"+00:00\")) >= before\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-053 / 054 / 055 — role assignment through the authorized mechanism (IAM)\n# ---------------------------------------------------------------------------\n\nNEW_USER, USER_U, USER_V = 3001, 3002, 3003\n\n\ndef test_BR_041_assignment_via_iam_applied(rspc):\n    \"\"\"BR-041 | source_id: BR-RSPC-053 authorized mechanism.\"\"\"\n    pid = rspc.submit()\n    assert rspc.recommend(pid, user=NEW_USER).status_code == 403  # no RSPC role yet\n    ROLE_OF[NEW_USER] = \"HoD\"   # what the authorized IAM now reports for this user\n    try:\n        r = rspc.post(NEW_USER, f\"{BASE}{pid}/recommend/\", {\"outcome\": \"recommended\"},\n                      roles=[\"HoD\"])\n    finally:\n        ROLE_OF.pop(NEW_USER)\n\n    assert r.status_code == 200, r.content\n    assert status_of(pid) == \"dept_recommended\"\n\n\ndef test_BR_042_self_assignment_outside_iam_not_applied(rspc):\n    \"\"\"BR-042 | source_id: BR-RSPC-053 unauthorized source.\"\"\"\n    pid = rspc.to_dean(rspc.submit())\n    claimed = {\"outcome\": \"approve\", \"role\": \"Dean-RSPC\", \"roles\": [\"Dean-RSPC\"],\n               \"active_role\": \"Dean-RSPC\", \"permissions\": [\"rspc.proposal.decide\"]}\n\n    r = rspc.post(FACULTY_A, f\"{BASE}{pid}/decide/\", claimed)\n\n    assert r.status_code == 403, r.content\n    assert status_of(pid) == \"admin_verified\"\n\n\ndef test_BR_043_reassignment_via_iam_applied(rspc):\n    \"\"\"BR-043 | source_id: BR-RSPC-054 authorized mechanism.\"\"\"\n    pid = rspc.submit()\n    assert rspc.recommend(pid, user=USER_V).status_code == 403 if USER_V in ROLE_OF else True\n    # IAM reassigns HoD from U to V.\n    r = rspc.post(USER_V, f\"{BASE}{pid}/recommend/\", {\"outcome\": \"recommended\"},\n                  roles=[\"HoD\"])\n\n    assert r.status_code == 200, r.content\n    assert status_of(pid) == \"dept_recommended\"\n\n\ndef test_BR_044_reassignment_outside_iam_not_applied(rspc):\n    \"\"\"BR-044 | source_id: BR-RSPC-054 unauthorized source.\"\"\"\n    pid = rspc.submit()\n    transfer = {\"outcome\": \"recommended\", \"role\": \"HoD\", \"roles\": [\"HoD\"],\n                \"reassign_from\": USER_U, \"reassign_to\": USER_V}\n\n    r_v = rspc.post(USER_V, f\"{BASE}{pid}/recommend/\", transfer, roles=[\"Faculty\"])\n\n    assert r_v.status_code == 403, r_v.content\n    assert status_of(pid) == \"submitted\"\n    r_u = rspc.post(USER_U, f\"{BASE}{pid}/recommend/\", {\"outcome\": \"recommended\"},\n                    roles=[\"HoD\"])\n    assert r_u.status_code == 200, r_u.content\n\n\ndef test_BR_045_role_change_effective_immediately(rspc):\n    \"\"\"BR-045 | source_id: BR-RSPC-055.\"\"\"\n    p1 = rspc.submit()\n    p2 = rspc.submit()\n    # U is HoD and can act.\n    assert pid_ok(rspc.post(USER_U, f\"{BASE}{p1}/recommend/\", {\"outcome\": \"recommended\"},\n                            roles=[\"HoD\"]))\n    # IAM: HoD role moves from U to V. Immediately afterwards:\n    r_u = rspc.post(USER_U, f\"{BASE}{p2}/recommend/\", {\"outcome\": \"recommended\"},\n                    roles=[\"Faculty\"])\n    r_v = rspc.post(USER_V, f\"{BASE}{p2}/recommend/\", {\"outcome\": \"recommended\"},\n                    roles=[\"HoD\"])\n\n    assert r_u.status_code == 403, r_u.content\n    assert r_v.status_code == 200, r_v.content\n    assert [d.actor_id for d in decisions_of(p2)] == [USER_V]\n\n\ndef pid_ok(response):\n    return response.status_code == 200\n\n\n# ---------------------------------------------------------------------------\n# Scope boundaries\n# ---------------------------------------------------------------------------\n\n@not_automated(\"RSPC exposes no staff-appointment or stipend-status interface at A8_BASE.\")\ndef test_BR_046_no_hr_or_payroll_execution():\n    \"\"\"BR-046 | source_id: BR-RSPC-058.\"\"\"\n\n\n@not_automated(\"RSPC exposes no financial-request or transaction-record interface at \"\n               \"A8_BASE.\")\ndef test_BR_047_no_accounting_or_payment_execution():\n    \"\"\"BR-047 | source_id: BR-RSPC-059.\"\"\"\n\n\n@not_automated(\"RSPC exposes no procurement-status or asset-declaration interface at \"\n               \"A8_BASE.\")\ndef test_BR_048_no_procurement_or_inventory_execution():\n    \"\"\"BR-048 | source_id: BR-RSPC-060.\"\"\"\n\n\n@not_automated(\"RSPC triggers no notification events and exposes no notification \"\n               \"interface at A8_BASE.\")\ndef test_BR_049_notification_triggered_on_submission():\n    \"\"\"BR-049 | source_id: BR-RSPC-061 notification triggered.\"\"\"\n\n\n@not_automated(\"RSPC triggers no notification events and exposes no notification \"\n               \"interface at A8_BASE, so recording of the event under an email-delivery \"\n               \"failure cannot be observed.\")\ndef test_BR_050_delivery_failure_does_not_fail_rspc_action():\n    \"\"\"BR-050 | source_id: BR-RSPC-061 stated exception (external delivery failure).\"\"\"\n\n\n@not_automated(\"RSPC exposes no external funding-agency submission/disbursement tracking \"\n               \"interface at A8_BASE.\")\ndef test_BR_051_external_funding_agency_tracking_only():\n    \"\"\"BR-051 | source_id: BR-RSPC-062.\"\"\"\n\n\ndef test_BR_052_unauthenticated_request_rejected(stub_iam):\n    \"\"\"BR-052 | source_id: BR-RSPC-063.\"\"\"\n    stub_iam()  # IAM present, but the request carries no credential\n    ResearchProposal.objects.create(title=\"secret\", objectives=\"x\", pi_id=FACULTY_A,\n                                    status=\"submitted\")\n\n    r = APIClient().get(MINE)\n\n    assert r.status_code == 401, r.content\n    assert b\"secret\" not in r.content\n\n\n@not_automated(\"RSPC exposes no proposal/project update interface at A8_BASE, so a \"\n               \"lifecycle-permitted update cannot be attempted.\")\ndef test_BR_053_update_permitted_in_lifecycle_state():\n    \"\"\"BR-053 | source_id: BR-RSPC-065 update permitted in current lifecycle state.\"\"\"\n\n\n@not_automated(\"RSPC exposes no proposal/project update interface at A8_BASE, so a \"\n               \"lifecycle-prohibited update cannot be attempted.\")\ndef test_BR_054_update_not_permitted_in_lifecycle_state():\n    \"\"\"BR-054 | source_id: BR-RSPC-065 update not permitted in current lifecycle state.\"\"\"\n\n\n# ---------------------------------------------------------------------------\n# BR-RSPC-066 / 067 / 068 / 070 — forwarding and Dean authority\n# ---------------------------------------------------------------------------\n\ndef test_BR_055_eligible_verification_forwarded(rspc):\n    \"\"\"BR-055 | source_id: BR-RSPC-066 eligible verification outcome.\"\"\"\n    pid = rspc.to_admin(rspc.submit())\n\n    r = rspc.verify(pid, \"eligible\")\n\n    assert r.status_code == 200, r.content\n    assert pid in rspc.queue_ids(DEAN)\n\n\ndef test_BR_056_ineligible_verification_not_advanced(rspc):\n    \"\"\"BR-056 | source_id: BR-RSPC-066 ineligible verification outcome.\"\"\"\n    pid = rspc.to_admin(rspc.submit())\n\n    r = rspc.verify(pid, \"not_eligible\", remarks=\"Missing compliance documents\")\n\n    assert r.status_code == 200, r.content\n    assert pid not in rspc.queue_ids(DEAN)\n    assert status_of(pid) != \"admin_verified\"\n\n\ndef test_BR_057_recommended_forwarded(rspc):\n    \"\"\"BR-057 | source_id: BR-RSPC-067 recommended.\"\"\"\n    pid = rspc.submit()\n\n    r = rspc.recommend(pid, \"recommended\")\n\n    assert r.status_code == 200, r.content\n    assert [d.outcome for d in decisions_of(pid)] == [\"recommended\"]\n    assert pid in rspc.queue_ids(ADMIN)\n\n\ndef test_BR_058_not_recommended_recorded_not_forwarded(rspc):\n    \"\"\"BR-058 | source_id: BR-RSPC-067 not recommended.\"\"\"\n    pid = rspc.submit()\n\n    r = rspc.recommend(pid, \"not_recommended\", remarks=\"Out of department scope\")\n\n    assert r.status_code == 200, r.content\n    d = decisions_of(pid)\n    assert len(d) == 1 and d[0].outcome == \"not_recommended\"\n    assert d[0].remarks == \"Out of department scope\"\n    assert pid not in rspc.queue_ids(ADMIN)\n\n\n@not_automated(\"A8_BASE represents no Dean-RSPC authority limit or Director-required \"\n               \"condition, so a request 'outside Dean authority' cannot be set up; the \"\n               \"precondition cannot be established through the available interfaces.\")\ndef test_BR_059_dean_cannot_finalize_outside_authority():\n    \"\"\"BR-059 | source_id: BR-RSPC-068 outside authority (forward/escalate); BR-RSPC-004\n    Dean does not finalize.\"\"\"\n\n\ndef test_BR_060_dean_cannot_approve_ineligible_request(rspc):\n    \"\"\"BR-060 | source_id: BR-RSPC-068 ineligible request.\"\"\"\n    pid = rspc.to_admin(rspc.submit())\n    assert rspc.verify(pid, \"not_eligible\").status_code == 200\n\n    r = rspc.decide(pid, \"approve\")\n\n    assert 400 <= r.status_code < 500, r.content\n    assert status_of(pid) != \"approved\"\n\n\ndef test_BR_061_unrepresented_policy_not_invented(rspc):\n    \"\"\"BR-061 | source_id: BR-RSPC-070 unrepresented external policy not invented.\"\"\"\n    r = rspc.post(FACULTY_A, BASE, valid_payload(budget=\"99999999.99\"))\n    assert r.status_code == 201, r.content\n    pid = r.json()[\"id\"]\n\n    assert rspc.recommend(pid).status_code == 200\n    assert rspc.verify(pid).status_code == 200\n    assert rspc.decide(pid, \"approve\").status_code == 200\n\n    assert status_of(pid) == \"approved\"\n    assert not any(d.stage == \"Director\" for d in decisions_of(pid))\n"
}
```

#### Tool result

````
File created successfully at: /home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py (file state is current in your context — no need to Read it back)
````

## Claude — 2026-11-10T21:06:24.841Z

Tidying two tests (BR-041, BR-043) before snapshotting — they had leftover helper logic that would break.

### Tool call: `Edit` — 2026-11-10T21:06:28.217Z

```json
{
  "replace_all": false,
  "file_path": "/home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py",
  "old_string": "    pid = rspc.submit()\n    assert rspc.recommend(pid, user=NEW_USER).status_code == 403  # no RSPC role yet\n    ROLE_OF[NEW_USER] = \"HoD\"   # what the authorized IAM now reports for this user\n    try:\n        r = rspc.post(NEW_USER, f\"{BASE}{pid}/recommend/\", {\"outcome\": \"recommended\"},\n                      roles=[\"HoD\"])\n    finally:\n        ROLE_OF.pop(NEW_USER)\n\n    assert r.status_code == 200, r.content",
  "new_string": "    pid = rspc.submit()\n    url = f\"{BASE}{pid}/recommend/\"\n    # No RSPC role yet.\n    assert rspc.post(NEW_USER, url, {\"outcome\": \"recommended\"}, roles=[]).status_code == 403\n\n    # The authorized IAM now assigns HoD to the user.\n    r = rspc.post(NEW_USER, url, {\"outcome\": \"recommended\"}, roles=[\"HoD\"])\n\n    assert r.status_code == 200, r.content"
}
```

### Tool call: `Edit` — 2026-11-10T21:06:30.931Z

```json
{
  "replace_all": false,
  "file_path": "/home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py",
  "old_string": "    pid = rspc.submit()\n    assert rspc.recommend(pid, user=USER_V).status_code == 403 if USER_V in ROLE_OF else True\n    # IAM reassigns HoD from U to V.\n    r = rspc.post(USER_V, f\"{BASE}{pid}/recommend/\", {\"outcome\": \"recommended\"},\n                  roles=[\"HoD\"])",
  "new_string": "    pid = rspc.submit()\n    url = f\"{BASE}{pid}/recommend/\"\n    # Before: U holds HoD, V does not.\n    assert rspc.post(USER_V, url, {\"outcome\": \"recommended\"},\n                     roles=[\"Faculty\"]).status_code == 403\n\n    # The authorized IAM reassigns HoD from U to V.\n    r = rspc.post(USER_V, url, {\"outcome\": \"recommended\"}, roles=[\"HoD\"])"
}
```

#### Tool result

````
The file /home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

#### Tool result

````
The file /home/nikhit/Documents/Fusion/Fusion-Integrated/tests/a8/br/test_br.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:06:35.139Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 3 is in progress. App actions available now: create_pr, verify.
````

### Tool call: `Bash` — 2026-11-10T21:06:41.361Z

```json
{
  "command": "grep -oE \"^def test_BR_[0-9]{3}\" tests/a8/br/test_br.py | sort | uniq | wc -l; grep -c \"not_automated(\" tests/a8/br/test_br.py\nmkdir -p a8_snapshots/br/raw && cp tests/a8/br/__init__.py tests/a8/br/test_br.py a8_snapshots/br/raw/\ncat >> a8_logs/br/LOG.md <<EOF\n- $(date -u +%H:%M) Read implementation: modules/rspc/{registry,models,apps}.py, modules/rspc/api/{urls,serializers,views}.py,\n  fusion_auth/{permissions,authentication,principal}.py, part of fusion_auth/client.py, root conftest.py,\n  core/api/exceptions.py (head), config/settings/test.py, pyproject pytest config. modules/rspc/tests/ NOT read.\n- Interfaces found: only the research-proposal workflow (submit, mine, queue, recommend, verify, decide, authorize).\n  No detail/update endpoint, no audit log, no notifications, no consultancy/staff/finance/procurement/reporting/closure/integration.\n- Wrote \\`tests/a8/br/test_br.py\\`: 61 test functions BR-001..BR-061 (BR-010 and BR-011 parametrized over the\n  fields/validations named in the design). 32 automated, 29 \\`NOT_AUTOMATED\\` skips (no interface; BR-059: the\n  \"outside Dean authority\" precondition cannot be represented). IAM (external service) replaced by root-conftest\n  \\`stub_iam\\` FakeIam; RSPC behaviour not mocked. Before snapshotting, fixed two helper slips in BR-041/BR-043\n  that I noticed on re-reading my own draft (no run had happened).\n- Copied to \\`a8_snapshots/br/raw/\\`. Not run yet.\nEOF",
  "description": "Count tests, snapshot raw copy, and log Step C"
}
```

#### Tool result

````
61
33
````

### Tool call: `Bash` — 2026-11-10T21:06:44.936Z

```json
{
  "command": "grep -c \"^@not_automated\" tests/a8/br/test_br.py",
  "description": "Count NOT_AUTOMATED skip decorators"
}
```

#### Tool result

````
32
````

### Tool call: `Bash` — 2026-11-10T21:06:48.351Z

```json
{
  "command": "sed -i 's/32 automated, 29 `NOT_AUTOMATED` skips/29 automated, 32 `NOT_AUTOMATED` skips/' a8_logs/br/LOG.md; grep -n \"NOT_AUTOMATED\\` skips\" a8_logs/br/LOG.md",
  "description": "Correct the automated/skip counts in the log"
}
```

#### Tool result

````
35:  fields/validations named in the design). 29 automated, 32 `NOT_AUTOMATED` skips (no interface; BR-059: the
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:06:51.870Z

```json
{
  "recap": "Step C for BR is done: tests/a8/br/test_br.py has all 61 frozen cases, 29 automated against the proposal API and 32 skipped as NOT_AUTOMATED. A raw copy is in a8_snapshots/br/raw. Nothing has been run or committed yet.",
  "ask": "Shall I go on to Step D (collect-only check and any Prompt C repairs)?",
  "actions": [
    {
      "label": "Do Step D"
    }
  ]
}
```

#### Tool result

````
Shown in the next-step box. Your closing message is your answer to the user: write it now, in full, as the last thing you say this turn. The box asks your question, so do not ask it again.
````

## Claude — 2026-11-10T21:07:01.854Z

I've finished Step C for BR: all 61 frozen test cases are written. I haven't run or edited them since writing them.

**What I read:** only the RSPC module code (registry, models, API URLs, serializers, views), plus the auth layer, the root `conftest.py` and the test settings. I did not open `modules/rspc/tests/`, and I did not open the FR or UC test folders even though they sit next to `tests/a8/br/`.

**What exists to test:** the code only implements the research-proposal workflow: submit, "my proposals", the review queue, and the recommend → verify → decide → authorize steps. There is no endpoint for viewing or updating a single proposal, no audit log and no notifications.

**[tests/a8/br/test_br.py](tests/a8/br/test_br.py), 61 test functions (BR-001 to BR-061):**
- **29 automated** through the `/api/v1/rspc/` API. They cover approval routing, mandatory fields and validation, timestamps and remarks on decisions, who can see and do what, role changes through IAM, and the HoD, Admin and Dean decision steps.
- **32 skipped as `NOT_AUTOMATED: <reason>`**, because there's no interface for them:
  - consultancy, staff, finance and expenditure, procurement, reporting, closure, integration and notifications;
  - project updates;
  - BR-059, because the code has no Dean authority limit or "Director required" condition, so the precondition can't be set up.
- IAM, the external identity service, is replaced by the shared `stub_iam` fake from the root conftest. RSPC's own behaviour is not mocked.

**Likely failures in Step E:**
- **BR-040** expects the history log to include a submission entry. The proposal's decision history only records review decisions, so this will probably fail.
- **BR-037** may pass without proving much: with no single-proposal endpoint, asking for one returns 404 whether or not access control works.

**One correction to report:** before snapshotting, I fixed two helper mistakes in my own draft of BR-041 and BR-043. One would have crashed and the other was a meaningless assertion. Nothing had been run at that point, and it's recorded in the log.

The prompt is in [a8_logs/br/PROMPT_B.txt](a8_logs/br/PROMPT_B.txt), the raw copy is in [a8_snapshots/br/raw/](a8_snapshots/br/raw/test_br.py), and [a8_logs/br/LOG.md](a8_logs/br/LOG.md) is updated.

## User — 2026-11-10T21:07:18.600Z

Do Step D

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:07:21.463Z

```json
{
  "items": [
    {
      "content": "Run collect-only and a setup check",
      "status": "in_progress"
    },
    {
      "content": "Apply Prompt C repairs if needed",
      "status": "pending"
    },
    {
      "content": "Snapshot final tests and log",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (3 steps).
````

### Tool call: `Bash` — 2026-11-10T21:07:22.141Z

```json
{
  "command": ".venv/bin/pytest tests/a8/br --collect-only -q 2>&1 | tail -20",
  "description": "Collect BR tests without running them"
}
```

#### Tool result

````
tests/a8/br/test_br.py: 66
````

### Tool call: `Bash` — 2026-11-10T21:07:28.717Z

```json
{
  "command": ".venv/bin/pytest tests/a8/br -q -p no:cacheprovider 2>&1 | tail -25",
  "description": "Run BR tests once to detect setup errors"
}
```

#### Tool result

````
=================================== FAILURES ===================================
__________________ test_BR_040_submission_and_decision_logged __________________

rspc = <tests.a8.br.test_br.Rspc object at 0x7043dac9aff0>

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
>       assert submission, f"no submission entry in audit log: {log}"
E       AssertionError: no submission entry in audit log: [{'id': 25, 'proposal': 15, 'stage': 'HoD', 'actor_id': 2001, 'outcome': 'recommended', 'remarks': 'ok', 'decided_at': '2026-11-11T02:37:34.675088+05:30'}]
E       assert []

tests/a8/br/test_br.py:551: AssertionError
=========================== short test summary info ============================
FAILED tests/a8/br/test_br.py::test_BR_040_submission_and_decision_logged - A...
````

### Tool call: `Bash` — 2026-11-10T21:07:37.530Z

```json
{
  "command": ".venv/bin/pytest tests/a8/br -q -p no:cacheprovider 2>&1 | grep -E \"passed|failed|error\" | tail -3",
  "description": "Show the run's summary counts"
}
```

#### Tool result

````
(Bash completed with no output)
````

### Tool call: `Bash` — 2026-11-10T21:07:46.813Z

```json
{
  "command": ".venv/bin/pytest tests/a8/br -p no:cacheprovider -rA 2>&1 | grep -E \"^(PASSED|FAILED|ERROR|SKIPPED)\" | awk '{print $1}' | sort | uniq -c",
  "description": "Tally outcomes per test state"
}
```

#### Tool result

````
      1 FAILED
     33 PASSED
     32 SKIPPED
````

## Claude — 2026-11-10T21:07:56.277Z

No setup errors, so no Prompt C round is needed. Recording that and taking the final snapshot.

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:07:56.780Z

```json
{
  "done": [
    1,
    2
  ],
  "start": 3
}
```

#### Tool result

````
Plan updated: step 3 of 3 is in progress. App actions available now: create_pr.
````

### Tool call: `Bash` — 2026-11-10T21:07:58.602Z

```json
{
  "command": "mkdir -p a8_snapshots/br/final && cp tests/a8/br/__init__.py tests/a8/br/test_br.py a8_snapshots/br/final/ && diff -r a8_snapshots/br/raw a8_snapshots/br/final && echo IDENTICAL\ncat >> a8_logs/br/LOG.md <<EOF\n\n## Step D — make executable\n- $(date -u +%H:%M) \\`.venv/bin/pytest tests/a8/br --collect-only -q\\` → \\`tests/a8/br/test_br.py: 66\\`, no collection errors\n  (61 cases; BR-010 parametrized ×5 fields, BR-011 ×2 validations).\n- Ran the suite once (no coverage) to check for run-time setup errors (ERROR state): none.\n  States: 33 passed, 1 failed, 32 skipped, 0 errors. The single failure (BR-040) is an assertion failure,\n  which is not repairable under Prompt C; it is left for Step F.\n- Prompt C repair rounds used: 0 of 2. No test code changed.\n- Final tests copied to \\`a8_snapshots/br/final/\\` (identical to raw).\nEOF",
  "description": "Snapshot final tests and log Step D"
}
```

#### Tool result

````
IDENTICAL
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:08:01.631Z

```json
{
  "recap": "Step D for BR is done: the suite collects and runs with no setup errors, so no Prompt C repairs were used. The final snapshot matches the raw one. A check run gave 33 passed, 1 failed (BR-040) and 32 skipped; nothing is committed.",
  "ask": "Shall I run Step E (the official run with coverage)?",
  "actions": [
    {
      "label": "Do Step E"
    }
  ]
}
```

#### Tool result

````
Shown in the next-step box. Your closing message is your answer to the user: write it now, in full, as the last thing you say this turn. The box asks your question, so do not ask it again.
````

## Claude — 2026-11-10T21:08:06.871Z

Step D for BR is done. The tests run without setup errors, so I used no repair rounds (0 of 2) and changed no test code.

- **Collect-only:** 66 items with no errors. That's the 61 cases, with BR-010 run once for each of its 5 mandatory fields and BR-011 once for each of its 2 validations.
- **Setup-error check:** the handoff counts setup errors that only show up at run time as repairable, so I ran the suite once without coverage to look for them. There were none. Results: 33 passed, 1 failed, 32 skipped.
- **The one failure is BR-040**, the audit-log rule. The proposal's history has the HoD decision but no entry for the Faculty member's submission. That's a failed assertion, not a setup error, so it isn't repairable; I'll examine it in Step F.

The final snapshot in [a8_snapshots/br/final/](a8_snapshots/br/final/test_br.py) is identical to the raw one, and [a8_logs/br/LOG.md](a8_logs/br/LOG.md) is updated.

## User — 2026-11-10T21:08:44.300Z

Do Step E

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:08:46.938Z

```json
{
  "items": [
    {
      "content": "Run the exact Step E pytest command",
      "status": "in_progress"
    },
    {
      "content": "Compute production line/branch coverage summary",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (2 steps).
````

### Tool call: `Bash` — 2026-11-10T21:08:48.459Z

```json
{
  "command": "mkdir -p a8_results/br && .venv/bin/pytest tests/a8/br \\\n  --junitxml=a8_results/br/junit.xml \\\n  --cov=modules.rspc --cov-branch \\\n  --cov-report=xml:a8_results/br/coverage.xml \\\n  --cov-report=term-missing \\\n  > a8_results/br/pytest.log 2>&1; echo exit=$?; tail -30 a8_results/br/pytest.log",
  "description": "Run the official BR suite with coverage"
}
```

#### Tool result

````
exit=1
>       assert submission, f"no submission entry in audit log: {log}"
E       AssertionError: no submission entry in audit log: [{'id': 25, 'proposal': 15, 'stage': 'HoD', 'actor_id': 2001, 'outcome': 'recommended', 'remarks': 'ok', 'decided_at': '2026-11-11T02:38:58.547305+05:30'}]
E       assert []

tests/a8/br/test_br.py:551: AssertionError
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name                                                                         Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------------------------------------------------
modules/rspc/__init__.py                                                         0      0      0      0   100%
modules/rspc/api/__init__.py                                                     0      0      0      0   100%
modules/rspc/api/serializers.py                                                 26      0      4      0   100%
modules/rspc/api/urls.py                                                         3      0      0      0   100%
modules/rspc/api/views.py                                                      131     20     36     10    80%   50, 67, 72, 104, 109, 141, 168-180, 204, 220-236
modules/rspc/apps.py                                                             4      0      0      0   100%
modules/rspc/migrations/0001_initial.py                                          6      0      0      0   100%
modules/rspc/migrations/0002_alter_researchproposal_department_and_more.py       4      0      0      0   100%
modules/rspc/migrations/__init__.py                                              0      0      0      0   100%
modules/rspc/models.py                                                          31      2      0      0    94%   37, 56
modules/rspc/registry.py                                                         4      0      0      0   100%
modules/rspc/tests/__init__.py                                                   0      0      0      0   100%
modules/rspc/tests/test_proposal_flow.py                                        52     52      0      0     0%   1-85
modules/rspc/tests/test_proposal_validation.py                                  19     19      0      0     0%   1-24
------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                          280     93     40     10    67%
Coverage XML written to file a8_results/br/coverage.xml
=========================== short test summary info ============================
FAILED tests/a8/br/test_br.py::test_BR_040_submission_and_decision_logged - A...
1 failed, 33 passed, 32 skipped in 7.36s
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:09:02.027Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 2 is in progress. App actions available now: create_pr.
````

### Tool call: `Bash` — 2026-11-10T21:09:08.616Z

```json
{
  "command": "python3 - <<'EOF'\nimport xml.etree.ElementTree as ET\nr=ET.parse('a8_results/br/coverage.xml').getroot()\nrows=[];L=Lc=B=Bc=0\nfor c in r.iter('class'):\n    f=c.get('filename')\n    if '/tests/' in '/'+f or '/migrations/' in '/'+f: continue\n    lines=c.find('lines').findall('line')\n    l=len(lines); lc=sum(int(x.get('hits'))>0 for x in lines)\n    b=bc=0\n    for x in lines:\n        if x.get('branch')=='true':\n            cc=x.get('condition-coverage').split('(')[1].rstrip(')'); a,t=map(int,cc.split('/')); bc+=a;b+=t\n    rows.append((f,l,lc,b,bc));L+=l;Lc+=lc;B+=b;Bc+=bc\nout=[\"# BR coverage summary (production code only)\",\"\",\n\"Source: `a8_results/br/coverage.xml` (pytest-cov, `--cov=modules.rspc --cov-branch`).\",\n\"Excluded: `modules/rspc/tests/*`, `modules/rspc/migrations/*`.\",\"\",\n\"| File | Lines covered/total | Line % | Branches covered/total | Branch % |\",\"|---|---|---|---|---|\"]\npct=lambda a,b: f\"{100*a/b:.2f}\" if b else \"n/a\"\nfor f,l,lc,b,bc in rows: out.append(f\"| {f} | {lc}/{l} | {pct(lc,l)} | {bc}/{b} | {pct(bc,b)} |\")\nout+=[f\"| **Total** | **{Lc}/{L}** | **{pct(Lc,L)}** | **{Bc}/{B}** | **{pct(Bc,B)}** |\",\"\",\n\"Test outcome (junit/pytest.log): 66 collected — 33 passed, 1 failed (BR-040), 32 skipped (NOT_AUTOMATED), 0 errors.\"]\nopen('a8_results/br/coverage_summary.md','w').write(\"\\n\".join(out)+\"\\n\");print(\"\\n\".join(out))\nEOF",
  "description": "Compute production-only line and branch coverage"
}
```

#### Tool result

````
# BR coverage summary (production code only)

Source: `a8_results/br/coverage.xml` (pytest-cov, `--cov=modules.rspc --cov-branch`).
Excluded: `modules/rspc/tests/*`, `modules/rspc/migrations/*`.

| File | Lines covered/total | Line % | Branches covered/total | Branch % |
|---|---|---|---|---|
| modules/rspc/__init__.py | 0/0 | n/a | 0/0 | n/a |
| modules/rspc/apps.py | 4/4 | 100.00 | 0/0 | n/a |
| modules/rspc/models.py | 29/31 | 93.55 | 0/0 | n/a |
| modules/rspc/registry.py | 4/4 | 100.00 | 0/0 | n/a |
| modules/rspc/api/__init__.py | 0/0 | n/a | 0/0 | n/a |
| modules/rspc/api/serializers.py | 26/26 | 100.00 | 4/4 | 100.00 |
| modules/rspc/api/urls.py | 3/3 | 100.00 | 0/0 | n/a |
| modules/rspc/api/views.py | 111/131 | 84.73 | 22/36 | 61.11 |
| **Total** | **177/199** | **88.94** | **26/40** | **65.00** |

Test outcome (junit/pytest.log): 66 collected — 33 passed, 1 failed (BR-040), 32 skipped (NOT_AUTOMATED), 0 errors.
````

### Tool call: `Bash` — 2026-11-10T21:09:13.177Z

```json
{
  "command": "cat >> a8_logs/br/LOG.md <<EOF\n\n## Step E — execute\n- $(date -u +%H:%M) Ran the exact Step E command from repo root → \\`a8_results/br/{junit.xml,coverage.xml,pytest.log}\\` (exit 1 because of one failure).\n- Result: 66 collected — 33 passed, 1 failed (BR-040), 32 skipped (NOT_AUTOMATED), 0 errors.\n- Production-only coverage (tests and migrations excluded), from coverage.xml: lines 177/199 = 88.94 %,\n  branches 26/40 = 65.00 % → \\`a8_results/br/coverage_summary.md\\`.\n- Note: the coverage term report in pytest.log lists the file names under modules/rspc/tests/ (0 % covered).\n  This came from the tool output; their contents were not read.\n- Machine-generated files not edited.\nEOF",
  "description": "Log Step E results"
}
```

#### Tool result

````
(Bash completed with no output)
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:09:16.199Z

```json
{
  "recap": "Step E for BR is done: 33 passed, 1 failed (BR-040) and 32 skipped. Production-only coverage is 88.94% of lines and 65.00% of branches, recorded in a8_results/br/coverage_summary.md. Nothing is committed yet.",
  "ask": "Shall I go on to Step F (examine the BR-040 failure)?",
  "actions": [
    {
      "label": "Do Step F"
    }
  ]
}
```

#### Tool result

````
Shown in the next-step box. Your closing message is your answer to the user: write it now, in full, as the last thing you say this turn. The box asks your question, so do not ask it again.
````

## Claude — 2026-11-10T21:09:22.494Z

I ran Step E for BR with the exact command from the handoff, from the repo root.

**Results:** 66 tests collected: 33 passed, 1 failed, 32 skipped as NOT_AUTOMATED, 0 errors. pytest exited with code 1 because of the failure.

**Coverage of production code only** (tests and migrations excluded), taken from `coverage.xml`:

| | Covered / total | % |
|---|---|---|
| Lines | 177 / 199 | 88.94 |
| Branches | 26 / 40 | 65.00 |

Most of what's uncovered is in `views.py`: two of the endpoints' error paths, the rejection branches of the Dean and Director decisions, and the queue's no-permission fallback.

**The failure is BR-040**, the audit-log rule (BR-RSPC-050). The proposal's history has the HoD decision but no entry for the Faculty member's submission. I'll examine it in Step F.

The machine-generated output is in `a8_results/br/` (`junit.xml`, `coverage.xml`, `pytest.log`), and I didn't edit any of it. The coverage table is in [a8_results/br/coverage_summary.md](a8_results/br/coverage_summary.md), and [a8_logs/br/LOG.md](a8_logs/br/LOG.md) is updated.

The coverage report in `pytest.log` printed the names of the hidden Assignment-7 test files. I didn't open them, and I noted this in the log.

## User — 2026-11-10T21:09:28.389Z

Do Step F

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:09:36.326Z

```json
{
  "items": [
    {
      "content": "Re-run BR-040 alone twice",
      "status": "in_progress"
    },
    {
      "content": "Apply the four checks and write failures.md",
      "status": "pending"
    },
    {
      "content": "Update shared DEFECTS.md",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (3 steps).
````

### Tool call: `Bash` — 2026-11-10T21:09:37.702Z

```json
{
  "command": "for i in 1 2; do .venv/bin/pytest \"tests/a8/br/test_br.py::test_BR_040_submission_and_decision_logged\" -p no:cacheprovider 2>&1 | grep -E \"AssertionError|passed|failed\"; done; ls a8_logs/; cat a8_logs/DEFECTS.md 2>/dev/null",
  "description": "Re-run BR-040 twice and read shared defects file"
}
```

#### Tool result

````
E       AssertionError: no submission entry in audit log: [{'id': 1, 'proposal': 1, 'stage': 'HoD', 'actor_id': 2001, 'outcome': 'recommended', 'remarks': 'ok', 'decided_at': '2026-11-11T02:39:42.552927+05:30'}]
tests/a8/br/test_br.py:551: AssertionError
1 failed in 4.22s
E       AssertionError: no submission entry in audit log: [{'id': 1, 'proposal': 1, 'stage': 'HoD', 'actor_id': 2001, 'outcome': 'recommended', 'remarks': 'ok', 'decided_at': '2026-11-11T02:39:48.683329+05:30'}]
tests/a8/br/test_br.py:551: AssertionError
1 failed in 5.98s
DEFECTS.md
br
fr
uc
# A8 — shared defect log (RSPC)

One row per underlying problem. "Exposed by" lists the strategies whose tests revealed it; later strategies add themselves to an existing row instead of adding a duplicate.

| Defect ID | Summary | Classification | Spec evidence | Exposed by (test_ids) |
|---|---|---|---|---|
| D-01 | Proposal submission is not logged as a retrievable audit/log event; only review decisions (HoD/Admin/Dean/Director) are logged. | Confirmed Implementation Defect | RSPC-FR-088; RSPC-CFR-002 | FR (FR-009) |
| D-02 | No draft save/revise for research proposals: create always records the proposal as `submitted` (status read-only, hard-coded in the view) and there is no update endpoint, so Faculty cannot save or revise a draft before submission. | Confirmed Implementation Defect | RSPC-UC-002 Alternative A1 | UC (UC-006) |

## Candidate failures not confirmed as defects

| Ref | Summary | Classification | Spec evidence | Raised by (test_ids) |
|---|---|---|---|---|
| C-01 | Dean-RSPC can finally approve a proposal of any budget; no Dean approval limit is applied. The spec requires approval "within delegated or defined limits" but defines no limit. | Specification ambiguity | RSPC-FR-126; RSPC-CFR-004 | FR (FR-023) |
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:09:57.635Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 3 is in progress. App actions available now: create_pr.
````

### Tool call: `Bash` — 2026-11-10T21:10:10.372Z

```json
{
  "command": "cat > a8_logs/br/failures.md <<'EOF'\n# BR — failure examination (Step F)\n\nRun: `a8_results/br/pytest.log` — 66 collected, 33 passed, **1 failed**, 32 skipped, 0 errors.\n\n## BR-040 — `test_BR_040_submission_and_decision_logged`\n\n- **source_id:** BR-RSPC-050 (Maintain RSPC Audit and Compliance Logs)\n- **Error summary:** `AssertionError: no submission entry in audit log`. After Faculty submits and HoD recommends,\n  the proposal's history (`decisions` returned by `GET /api/v1/rspc/proposals/mine/`) contains only the HoD entry\n  (`stage HoD, actor_id 2001, outcome recommended, decided_at …`). There is no entry for the submission event.\n\n### Four checks\n1. **Is the expected behaviour directly supported by the cited spec? Yes.** BR-RSPC-050: \"RSPC shall maintain logs\n   needed for audit, transparency, and regulatory compliance for RSPC-managed records and events.\" It applies to\n   \"RSPC lifecycle events and records\", is triggered when \"An auditable RSPC event/record change occurs\", and requires\n   that \"The relevant log/audit information is retained.\" The PS (3.9) adds: \"RSPC maintains logs for audit,\n   transparency, and regulatory compliance.\" Submitting a research proposal is an RSPC lifecycle event that creates an\n   RSPC record (PS 3.1, BR-RSPC-012 \"A Faculty proposal is submitted\").\n2. **Is the test correctly implemented and set up? Yes.** It drives the real API (submit as Faculty 1001, recommend as\n   HoD 2001) and reads the only history/log interface RSPC exposes, which is the proposal's decision history. The HoD\n   half of the assertion (actor, outcome, time) is satisfied, which shows that the setup and the log read work. Only\n   the submission entry is missing. The IAM fake only identifies the callers; no RSPC behaviour is mocked.\n   Caveat: the spec does not name the log's form. The proposal row stores `pi_id` and `created_at`, but RSPC exposes\n   no log entry for the submission (with actor, action and time), and `created_at` is not returned by any endpoint.\n3. **Is it reproducible? Yes.** I re-ran it alone twice (`pytest …::test_BR_040_submission_and_decision_logged`) and it\n   failed both times with the same assertion.\n4. **Does the observed behaviour contradict the expected? Yes.** Expected: a log entry for both the submission and\n   the decision. Observed: a log entry for the decision only.\n\n**Classification: Confirmed Implementation Defect.** It is the same underlying problem as the existing shared\ndefect **D-01** (proposal submission is not logged as a retrievable audit/log event), so BR is added to D-01 as an\nexposing strategy instead of opening a new defect.\n\n## Notes (not failures)\n- 32 tests are `NOT_AUTOMATED` skips (there is no interface for consultancy, staff, finance, procurement, reporting,\n  closure, integration, notifications or project updates; for BR-059 the precondition cannot be set up). They are\n  not candidate failures.\n- BR-059 (Dean-RSPC must not finalize outside its authority) concerns the same gap as shared candidate C-01. In BR\n  it was not automated because no authority limit is represented, so BR did not raise C-01.\n\n**Summary:** candidate failures 1; confirmed implementation defects 1 (D-01, shared with FR); new defects 0.\nEOF\npython3 - <<'EOF'\np='a8_logs/DEFECTS.md';s=open(p).read()\nold=\"| RSPC-FR-088; RSPC-CFR-002 | FR (FR-009) |\"\nassert s.count(old)==1\ns=s.replace(old,\"| RSPC-FR-088; RSPC-CFR-002; BR-RSPC-050 | FR (FR-009); BR (BR-040) |\")\nopen(p,'w').write(s)\nEOF\ngrep -n \"D-01\" a8_logs/DEFECTS.md\ncat >> a8_logs/br/LOG.md <<EOF\n\n## Step F — examine failures\n- $(date -u +%H:%M) BR-040 re-run alone twice: failed both times with the same assertion.\n- Four checks all yes → Confirmed Implementation Defect. It is the same underlying problem as shared D-01 (submission\n  not logged), so I added BR (BR-040) and BR-RSPC-050 to the D-01 row of \\`a8_logs/DEFECTS.md\\` and opened no new defect.\n  Read \\`a8_logs/DEFECTS.md\\` only in this step, as allowed.\n- Wrote \\`a8_logs/br/failures.md\\`. Candidate failures 1; confirmed defects 1 (shared); new 0.\nEOF",
  "description": "Write failures.md, add BR to D-01, log Step F"
}
```

#### Tool result

````
7:| D-01 | Proposal submission is not logged as a retrievable audit/log event; only review decisions (HoD/Admin/Dean/Director) are logged. | Confirmed Implementation Defect | RSPC-FR-088; RSPC-CFR-002; BR-RSPC-050 | FR (FR-009); BR (BR-040) |
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:10:13.163Z

```json
{
  "recap": "Step F for BR is done: BR-040 is a Confirmed Implementation Defect, the same problem as shared defect D-01, so BR is now listed on that row. The reasoning and the four checks are in a8_logs/br/failures.md. Nothing is committed yet.",
  "ask": "Shall I do Step G (summary, production-diff check, commit)?",
  "actions": [
    {
      "label": "Do Step G"
    }
  ]
}
```

#### Tool result

````
Shown in the next-step box. Your closing message is your answer to the user: write it now, in full, as the last thing you say this turn. The box asks your question, so do not ask it again.
````

## Claude — 2026-11-10T21:10:20.491Z

I've examined the one BR failure. BR-040 is a confirmed implementation defect, and it's the same problem FR already logged as D-01, so there are no new defects.

**What failed:** BR-040 checks the audit-log rule (BR-RSPC-050). The proposal's history has the HoD's decision but no entry for the Faculty member's submission.

**The four checks all came out yes:**
1. **Supported by the spec:** BR-RSPC-050 requires logs for "RSPC lifecycle events and records", and the Problem Statement says "RSPC maintains logs for audit…". Submitting a proposal is a lifecycle event.
2. **Test built correctly:** it uses the real API and reads the proposal's decision history, the only log RSPC exposes. The HoD half of the check passes, so the setup and the log read work.
   - The spec doesn't say what form the log takes. The proposal does store its owner and creation time, but no endpoint returns the creation time, and there is no submission log entry.
3. **Reproducible:** I ran it alone twice and it failed the same way both times.
4. **Contradicts the expectation:** a log entry was expected for both the submission and the decision, but there is one only for the decision.

**Shared log:** in [a8_logs/DEFECTS.md](a8_logs/DEFECTS.md) I added BR-RSPC-050 and "BR (BR-040)" to the existing D-01 row instead of opening a duplicate. The candidate C-01 (no limit on what the Dean can approve) is related to BR-059. BR-059 was skipped as not automatable, so BR didn't raise it.

The details are in [a8_logs/br/failures.md](a8_logs/br/failures.md), and [a8_logs/br/LOG.md](a8_logs/br/LOG.md) is updated.

## User — 2026-11-10T21:10:27.828Z

Do Step G

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:10:29.885Z

```json
{
  "items": [
    {
      "content": "Verify no production diff since a8-base",
      "status": "in_progress"
    },
    {
      "content": "Write SUMMARY.md and finish the log",
      "status": "pending"
    },
    {
      "content": "Commit BR artifacts only",
      "status": "pending"
    }
  ],
  "scope": "continuation"
}
```

#### Tool result

````
Plan shown (3 steps).
````

### Tool call: `Bash` — 2026-11-10T21:10:30.873Z

```json
{
  "command": "git diff --stat a8-base -- modules config client registry openapi core fusion_auth; echo \"diff-exit=$?\"; git status --short; date -u '+%H:%M:%S'",
  "description": "Check production code is unchanged and list status"
}
```

#### Tool result

````
diff-exit=0
 M a8_logs/DEFECTS.md
?? a8_design/BR_DESIGN.json
?? a8_logs/br/
?? a8_results/br/
?? a8_snapshots/br/
?? tests/a8/br/
21:10:30
````

## Claude — 2026-11-10T21:10:33.187Z

The production diff is empty. Before writing the summary, I'm checking the log timestamps, since I typed one by hand in Step A.

### Tool call: `Bash` — 2026-11-10T21:10:34.445Z

```json
{
  "command": "grep -nE \"^- [0-9]{2}:[0-9]{2}|Start time\" a8_logs/br/LOG.md; stat -c '%y %n' a8_design/BR_DESIGN.json a8_logs/br/PROMPT_A.txt a8_logs/br/FROZEN.txt",
  "description": "List log timestamps and file modification times"
}
```

#### Tool result

````
4:- Start time: 2026-11-10 20:57:55 UTC
7:- 20:57 Read `specs_rspc/A8_HANDOFF_CLAUDE.md`.
8:- 20:58 Read only `specs_rspc/a8_plain/01_RSPC_Problem_Statement_v1.0_SYNCHRONIZED.txt` and
14:- 21:10 Generated the design (Prompt A output) and saved unchanged as `a8_design/BR_DESIGN.json`:
21:- 21:02 Wrote `a8_logs/br/obligations.md`: 38/38 active BRs, 67/67 distinct outcome obligations covered.
28:- 21:03 Received "continue". Wrote `a8_logs/br/PROMPT_B.txt`. Reading implementation (excluding modules/rspc/tests/).
29:- 21:06 Read implementation: modules/rspc/{registry,models,apps}.py, modules/rspc/api/{urls,serializers,views}.py,
42:- 21:07 `.venv/bin/pytest tests/a8/br --collect-only -q` → `tests/a8/br/test_br.py: 66`, no collection errors
51:- 21:09 Ran the exact Step E command from repo root → `a8_results/br/{junit.xml,coverage.xml,pytest.log}` (exit 1 because of one failure).
60:- 21:10 BR-040 re-run alone twice: failed both times with the same assertion.
2026-11-10 21:00:24.609941139 +0000 a8_design/BR_DESIGN.json
2026-11-10 20:58:47.115038370 +0000 a8_logs/br/PROMPT_A.txt
2026-11-10 21:02:02.912083950 +0000 a8_logs/br/FROZEN.txt
````

## Claude — 2026-11-10T21:10:37.148Z

Line 14 had a hand-typed time (21:10) that was wrong; the file's modification time shows 21:00. Correcting it with a note, then writing the summary.

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:10:37.381Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 2 of 3 is in progress.
````

### Tool call: `Bash` — 2026-11-10T21:10:49.662Z

```json
{
  "command": "sed -i '14s/^- 21:10 Generated/- 21:00 Generated/' a8_logs/br/LOG.md\nEND=$(date -u '+%H:%M:%S')\ncat >> a8_logs/br/LOG.md <<EOF\n\n## Step G — wrap up\n- Correction: the Step A design time was originally typed by hand as \"21:10\"; the file mtime of\n  \\`a8_design/BR_DESIGN.json\\` (21:00:24 UTC) shows it was 21:00, and the entry was corrected to 21:00.\n- \\`git diff --stat a8-base -- modules config client registry openapi core fusion_auth\\` → empty (no production change).\n- Wrote \\`a8_logs/br/SUMMARY.md\\`. End time: 2026-11-10 $END UTC.\nEOF\ncat > a8_logs/br/SUMMARY.md <<EOF\n# A8 — Strategy BR — Summary\n\n| Item | Value |\n|---|---|\n| Model / runtime | Claude Opus 5.5 / Claude Code (same model and effort as FR, UC) |\n| Spec used | 04 Business Rule Specifications v1.3 (+ 01 Problem Statement) |\n| Design | \\`a8_design/BR_DESIGN.json\\` — 61 test cases, SHA-256 aaf14277889876c526cf3543b14861bde6097752605a67559615f9c76b652cca |\n| Obligations covered / total | 38/38 active BRs; 67/67 distinct outcome obligations |\n| Design completion used (Step B) | No (no gaps) |\n| Test cases automated | 29 of 61 |\n| Skipped / NOT_AUTOMATED | 32 of 61 |\n| Executable | 61/61 (66 pytest items incl. parametrization; 0 collection or setup errors) |\n| Passed / Failed | 28 cases passed (33 items), 1 case failed (BR-040) |\n| Line coverage (prod only) | 88.94 % (177/199) |\n| Branch coverage (prod only) | 65.00 % (26/40) |\n| Candidate failures | 1 (BR-040) |\n| Confirmed defects | 1 — D-01 \"proposal submission not logged\" (shared with FR; no new defect) |\n| Prompt C repair rounds | 0 of 2 |\n| Elapsed | 20:57:55 → $END UTC (~$(( ( $(date -u -d \"$END\" +%s) - $(date -u -d 20:57:55 +%s) ) / 60 )) min) |\n\n## Deviations\n- Before snapshotting (Step C, nothing run yet), I corrected two helper slips in my own draft of BR-041 and\n  BR-043: one would have raised a KeyError and the other was a meaningless assertion. Test intent and expected\n  results were unchanged, and raw = final.\n- In Step D I ran the suite once without coverage, to detect run-time setup errors as the handoff permits. No\n  test code was changed afterwards.\n- The pytest-cov terminal report in \\`pytest.log\\` lists the file names under \\`modules/rspc/tests/\\`. Their contents\n  were not read.\n- Corrected one hand-typed timestamp in LOG.md (Step A design entry, 21:10 → 21:00, from the file mtime).\n- BR-036/BR-037: RSPC has no single-proposal detail endpoint. Details are read from the \"mine\" list, and the\n  out-of-scope detail request to the nonexistent \\`proposals/<id>/\\` route returns 404, so that part of BR-037 is\n  weak evidence.\n- BR-011/012: \"represented policy validation\" was implemented using the two value validations RSPC represents\n  (budget > 0; end date not before start date).\nEOF\ncat a8_logs/br/SUMMARY.md | tail -22 | head -16",
  "description": "Fix the timestamp, finish the log and write SUMMARY.md"
}
```

#### Tool result

````
| Passed / Failed | 28 cases passed (33 items), 1 case failed (BR-040) |
| Line coverage (prod only) | 88.94 % (177/199) |
| Branch coverage (prod only) | 65.00 % (26/40) |
| Candidate failures | 1 (BR-040) |
| Confirmed defects | 1 — D-01 "proposal submission not logged" (shared with FR; no new defect) |
| Prompt C repair rounds | 0 of 2 |
| Elapsed | 20:57:55 → 21:10:50 UTC (~12 min) |

## Deviations
- Before snapshotting (Step C, nothing run yet), I corrected two helper slips in my own draft of BR-041 and
  BR-043: one would have raised a KeyError and the other was a meaningless assertion. Test intent and expected
  results were unchanged, and raw = final.
- In Step D I ran the suite once without coverage, to detect run-time setup errors as the handoff permits. No
  test code was changed afterwards.
- The pytest-cov terminal report in `pytest.log` lists the file names under `modules/rspc/tests/`. Their contents
  were not read.
````

### Tool call: `mcp__ccd_turn__update_plan` — 2026-11-10T21:10:54.246Z

```json
{
  "advance": true
}
```

#### Tool result

````
Plan updated: step 3 of 3 is in progress.
````

### Tool call: `Bash` — 2026-11-10T21:10:55.660Z

```json
{
  "command": "git add tests/a8/br a8_design/BR_DESIGN.json a8_results/br a8_logs a8_snapshots/br && git status --short && git commit -q -F - <<'EOF'\nA8 BR: frozen design, tests, results and logs\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nEOF\ngit log --oneline -1; git status --short",
  "description": "Stage only BR artifacts and commit"
}
```

#### Tool result

````
A  a8_design/BR_DESIGN.json
M  a8_logs/DEFECTS.md
A  a8_logs/br/FROZEN.txt
A  a8_logs/br/LOG.md
A  a8_logs/br/PROMPT_A.txt
A  a8_logs/br/PROMPT_B.txt
A  a8_logs/br/SUMMARY.md
A  a8_logs/br/failures.md
A  a8_logs/br/obligations.md
A  a8_results/br/coverage.xml
A  a8_results/br/coverage_summary.md
A  a8_results/br/junit.xml
A  a8_results/br/pytest.log
A  a8_snapshots/br/final/__init__.py
A  a8_snapshots/br/final/test_br.py
A  a8_snapshots/br/raw/__init__.py
A  a8_snapshots/br/raw/test_br.py
A  tests/a8/br/__init__.py
A  tests/a8/br/test_br.py
a7434f6 A8 BR: frozen design, tests, results and logs
````

### Tool call: `mcp__ccd_turn__wrap_up` — 2026-11-10T21:10:59.182Z

```json
{
  "recap": "Strategy BR is finished and committed as a7434f6 on a8-24bcs287, with the production code unchanged since a8-base. Nothing is pushed. The session log still needs exporting with /export, then WF runs in a new session."
}
```

#### Tool result

````
Nothing is pending, so the app draws no box; the recap is the session's status. Your closing message is your answer to the user: write it now, as the last thing you say this turn.
````

## Claude — 2026-11-10T21:11:05.581Z

Strategy BR is finished and committed as `a7434f6` on `a8-24bcs287`. Nothing is pushed, and production code is unchanged since `a8-base` (the `git diff --stat` check came back empty).

The commit holds only the BR files: the tests, the design, the results, the snapshots, `a8_logs/br/` and the updated shared `DEFECTS.md`.

[a8_logs/br/SUMMARY.md](a8_logs/br/SUMMARY.md) has the full numbers:

| Item | Value |
|---|---|
| Obligations covered | 38/38 business rules; 67/67 distinct outcomes |
| Test cases | 61: 29 automated, 32 skipped as NOT_AUTOMATED |
| Executable | 61/61 (66 pytest items, no errors) |
| Result | 28 cases passed, 1 failed (BR-040) |
| Coverage, production code only | 88.94% of lines, 65.00% of branches |
| Defects | 1 confirmed (D-01, already logged by FR), 0 new |
| Repair rounds used | 0 of 2 |
| Elapsed | about 13 minutes |

**Corrected timestamp:** in Step A I had typed one log time by hand as 21:10. The design file's modification time shows it was 21:00, so I corrected it and noted the change in the log.

**Other deviations:**
- I fixed two helper mistakes in my own BR-041 and BR-043 code before anything ran.
- I did one setup-error check run in Step D.
- The coverage report printed the names of the hidden Assignment-7 test files; I didn't open them.
- Part of BR-037 is weak evidence, because RSPC has no single-proposal endpoint and that request returns 404 either way.

To finish this strategy, run this here to save the session log:
```
/export a8_logs/br/SESSION.md
```
Then start a new session for WF.
