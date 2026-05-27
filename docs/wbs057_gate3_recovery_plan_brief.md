# WBS-057 Gate 3 Recovery Plan Brief

Current blocker: `BLOCKED_WBS057_EQUATION_SOURCES`.

Current WBS: WBS-057 / PR11.

Completed: WBS-055 `calibration.m`; WBS-056 `steady_state.m`.

Missing now: `model/samba_classic/samba_classic.mod`.

Do not create now: `.mod`, `.inc`, outputs, data, estimation, Redux, sovereign.

Missing formula count: 34.

Formula groups:
- MON: 1.
- EXT: 1.
- FISC: 4.
- ADMIN: 2.
- HH: 4.
- FIRM: 4.
- AGG: 4.
- SHOCK: 14.

`.mod` can be created next? No.

Reason: exact WP239 Appendix C formulas are not yet recorded for all MVP-required rows.

Recommended sequence:
1. Extract exact WP239 Appendix C formulas into WBS-057 sourcing.
2. Mark rows usable only when formula, source, and registry mapping are exact.
3. Fix phase-aware tests before `.mod` implementation if they block allowed WBS-057 artifacts.
4. Create `samba_classic.mod` only after missing formula count is zero.
5. Then proceed WBS-058 `shocks.inc`.
6. Then WBS-059 `observables.inc`.
7. Then WBS-060 wrapper.
8. Then WBS-061 residuals, WBS-062 BK, WBS-063 IRFs.
9. Then WBS-064 Gate 3 calibrated report.

True blockers:
- Missing exact formula.
- Missing source.
- Missing registry mapping.
- Runtime unavailable.
- Test contract too rigid.

Runtime status: Octave 11.1.0 and Dynare 7.0 available.

Exact next command:
`Implement the first step in docs/wbs057_gate3_recovery_plan_brief.md: extract exact WP239 Appendix C formulas for WBS-057 only.`
