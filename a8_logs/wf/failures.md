# WF — failure examination (Step F)

Execution (a8_results/wf/junit.xml, pytest.log): 34 tests — 6 passed, 0 failed, 0 errors, 28 skipped (NOT_AUTOMATED).

**No failed or errored tests → no candidate failures to examine. Confirmed implementation defects exposed by WF: 0.**

Notes (not failures):
- WF-001..006 (CW-RSPC-01) passed: every specified research-proposal transition and decision outcome (recommend / not recommend,
  eligible / not eligible, Dean approve / forward / not approve, Director approve / not approve) produced the specified resulting state.
- The WF tests start each proposal with the Faculty submit call; the spec's "Proposal Draft" from-state is a precondition and is not separately
  observed. As a result WF does not expose the existing draft defect D-02, and nothing was added to that row.
- WF-002/006 represent "Director action is required" by the Dean choosing to forward a high-value proposal. WF has no obligation that the Dean be
  *prevented* from approving a high-value proposal, so the existing C-01 is not touched.
- 28 NOT_AUTOMATED skips (WF-007..034: consultancy, staff appointment, financial, procurement, closure) are missing interfaces, not failures.
  They are reported as not automated rather than as defects.
