# WBS-057 to Gate 3 Recovery Plan

## 1. Current State

- Branch: `codex/modeling-decisions-baseline`.
- PR: GitHub draft PR `#1`, `[codex] Propose Gate 0 modeling decisions`.
- Current WBS/status before this recovery plan: `WBS-057 / PR11`, `BLOCKED_WBS057_EQUATION_SOURCES`.
- Last completed WBS: WBS-056, sourced `model/samba_classic/steady_state.m`.
- Completed artifacts: `model/samba_classic/calibration.m`, `model/samba_classic/steady_state.m`, `docs/wbs057_equation_sourcing.md`, `docs/wbs057_blockers.md`.
- Missing artifacts: `model/samba_classic/samba_classic.mod`, `model/samba_classic/shocks.inc`, `model/samba_classic/observables.inc`, Dynare wrapper, Dynare output tests, Gate 3 report.
- Actual blocker: 34 MVP-required rows still have `missing_formula` in `docs/wbs057_equation_sourcing.md`.
- Current status discrepancy to clean up: `docs/PROJECT_STATUS.md` still said `Commit hash: pending until commit` even though the latest pushed blocker commit is `7ae6cf6`.

Do not create `.mod`, `.inc`, outputs, data, estimation, Redux, or sovereign files until the relevant WBS explicitly allows them.

## 2. Remaining Tasks to Gate 3

| WBS | Objective | Inputs needed | Files to create/edit | Validation command | Stop condition | Commit message |
|---|---|---|---|---|---|---|
| WBS-057 | Implement `samba_classic.mod` by translating the approved registry into Dynare. | Exact formulas from WP239 Appendix C or approved project decisions; `calibration.m`; `steady_state.m`; registry mappings. | `docs/wbs057_equation_sourcing.md`, `model/samba_classic/samba_classic.mod`, phase-aware tests. | `python -m pytest`; `dynare model/samba_classic/samba_classic.mod noclearall` only if parse-ready. | Any MVP equation has `missing_formula`, unmapped variable, unmapped parameter, or unresolved test-contract block. | `Implement sourced SAMBA classic model shell` |
| WBS-058 | Add shock declarations and variances only after WBS-057 parses. | WBS-057 `.mod`; sourced shock names and standard deviations; registry shock rows. | `model/samba_classic/shocks.inc`, tests only. | `python -m pytest`; Dynare parse with shocks include. | Any shock std or equation is unsourced, deferred, or ambiguous. | `Add sourced shock declarations for SAMBA MVP` |
| WBS-059 | Add observables include only after data/registry mappings are consistent. | WBS-043 measurement drafts, WBS-052 dataset, approved observable variable names. | `model/samba_classic/observables.inc`, tests only. | `python -m pytest`; Dynare parse with observables include. | Measurement transform, `varobs`, or source mapping is unresolved. | `Add MVP observables include` |
| WBS-060 | Add reproducible Dynare wrapper. | Working WBS-057 model path, runtime verification, Makefile conventions. | Wrapper location from plan, likely diagnostics/test harness only; no outputs committed. | `python -m pytest`; wrapper dry run where non-destructive. | Wrapper writes committed outputs or depends on unavailable runtime. | `Add reproducible Dynare wrapper` |
| WBS-061 | Test steady-state residuals. | WBS-057 model, WBS-056 steady state, WBS-060 wrapper if needed. | Tests only; no committed Dynare outputs. | `python -m pytest`; Dynare steady/residual check. | Residuals exceed tolerance or require invented steady-state values. | `Add steady-state residual checks` |
| WBS-062 | Test Blanchard-Kahn conditions. | Solved WBS-057 model and runtime. | Tests only; no committed outputs. | `python -m pytest`; Dynare `check`. | BK fails or requires equation/parameter invention. | `Add BK condition checks` |
| WBS-063 | Test core IRF restrictions. | Solved model, sourced shock setup, approved IRF sign/timing criteria. | Tests only; no committed outputs unless later WBS permits. | `python -m pytest`; Dynare IRF run if runtime-safe. | IRF signs/timing fail or targets are not sourced. | `Add MVP IRF restriction checks` |
| WBS-064 | Write MVP calibrated report for Gate 3. | Passing WBS-061, WBS-062, WBS-063 results and validation notes. | Gate 3 report docs only unless outputs are explicitly allowed. | `python -m pytest`; report consistency checks. | Any Gate 3 validation test fails or outputs are unavailable. | `Document Gate 3 calibrated MVP results` |

## 3. WBS-057 Equation Sourcing Plan

For the 34 missing formulas, use the official local WP239 PDF and existing registry locators. Do not infer equations from memory and do not use generic New Keynesian substitutes.

Missing formula groups:

- MON: 1 row, monetary shock process; check WP239 C.60.
- EXT: 1 row, NFA/external accounting; check WP239 equations 78-80 and C.37-C.39.
- FISC: 4 rows, primary surplus target, realized surplus, debt law, fiscal auxiliaries; check WP239 C.30-C.34.
- ADMIN: 2 rows, administered-price equation and shock process; check WP239 C.58 and Table 3 mappings.
- HH: 4 rows, optimizing household, habit, labor/real wage, rule-of-thumb household; check WP239 C.1-C.10.
- FIRM: 4 rows, production/marginal cost, Phillips/markup, investment/Q, imported input; check WP239 C.11-C.27.
- AGG: 4 rows, market clearing, absorption/NX, GDP/GDP deflator, output gap/potential output; check WP239 C.35-C.42.
- SHOCK: 14 rows, shock processes excluding target and commodity; check WP239 C.43-C.61.

Distinctions:

- True missing formula: source locator exists, but exact formula is not recorded in project docs.
- Registry issue: row is a measurement draft, deferred shock, alias, or duplicate concept and should not enter WBS-057.
- Test-contract issue: the file is allowed by current WBS but a legacy test still blocks it.

An equation is ready for `.mod` only when:

- formula is transcribed from WP239 Appendix C or approved project decision;
- source location is exact;
- Dynare variable, parameter, and shock names are mapped to `docs/01_equation_registry.md`;
- unsupported measurement/deferred rows are marked `not_required_for_mvp`;
- `usable_in_samba_classic_mod: true` is set in WBS-057 sourcing.

## 4. Test Contract Fix Plan

Phase-aware artifact rules should read `docs/PROJECT_STATUS.md` or an equivalent project status marker:

- after WBS-055, allow exactly `model/samba_classic/calibration.m`;
- after WBS-056, allow exactly `model/samba_classic/steady_state.m`;
- during or after WBS-057 completion, allow `model/samba_classic/samba_classic.mod`;
- during or after WBS-058 completion, allow `model/samba_classic/shocks.inc`;
- during or after WBS-059 completion, allow `model/samba_classic/observables.inc`;
- still forbid unapproved `.m`, `.mod`, `.inc`, data, outputs, estimation, Redux, and sovereign files until their WBS allows them.

Tests currently involved in this contract include `tests/test_model_structure.py`, `tests/test_validation_templates.py`, `tests/test_dataset_outputs.py`, `tests/test_calibration_notes.py`, and `tests/test_model_outputs.py`.

## 5. Recommended Execution Sequence

1. Extract exact WP239 Appendix C formulas into `docs/wbs057_equation_sourcing.md`; do not create `.mod`.
2. Reclassify each WBS-057 row as `sourced_exact_formula`, `sourced_project_decision`, `loglinear_convention`, `not_required_for_mvp`, or `missing_formula`.
3. Update tests to allow `samba_classic.mod` only when WBS-057 is complete or explicitly in the implementation state.
4. Create `samba_classic.mod` only if missing formula count is zero for MVP-required rows.
5. Run Python tests and Dynare parse for WBS-057.
6. Implement WBS-058 `shocks.inc` only after WBS-057 parses.
7. Implement WBS-059 `observables.inc` only after WBS-058 and measurement mappings are ready.
8. Add WBS-060 wrapper without committing generated outputs.
9. Add WBS-061 through WBS-063 tests for residuals, BK, and IRFs.
10. Create WBS-064 report only after Gate 3 tests pass.

## 6. True Blockers

- Missing exact formula.
- Missing source.
- Missing registry mapping.
- Runtime unavailable.
- Test contract too rigid.

Current active blockers are missing exact formulas and potential phase-aware test-contract updates. Runtime is currently available via Octave 11.1.0 and Dynare 7.0.

## 7. Next Command

`Implement the first step in docs/wbs057_gate3_recovery_plan_brief.md: extract exact WP239 Appendix C formulas for WBS-057 only.`
