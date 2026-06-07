# Steady-State Sourcing Plan

Status: `WBS-056_READY_FOR_STEADY_STATE_M_BLOCKED_BY_TEST_CONTRACT`

Variables reviewed: registry structural, identity, auxiliary, and shock-process variables needed before `steady_state.m`.

Zero-by-loglinear convention variables: all rows in `docs/03_calibration_notes.md` marked `zero_by_loglinear_convention`.

Derived/sourced level anchors: `b_ss = 2.00` from BCB WP239 Table 2; `r_ss` and `nfa_ss` remain sourced WBS-055 calibration parameters.

Unresolved source variables: none currently identified for WBS-056.

Not required as standalone steady-state variables: registry lag aliases, expectation aliases, measurement series IDs, and deferred/non-MVP shock candidates.

Important rule: zero steady state is valid only for deviation variables and zero-mean shock states, not for economic levels.

Implementation blocker: creating `model/samba_classic/steady_state.m` would require updating legacy `.m` guardrails in tests outside this task's allowed file list.
