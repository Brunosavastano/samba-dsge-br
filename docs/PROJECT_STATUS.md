# Project Status

Updated: 2026-05-28

Current gate: Gate 3 started; Gate 1b approved for core source IDs; Gate 2b approved for minimum viable equation registry.
Execution status: WBS-057_COMPLETED; WBS-058_COMPLETED; WBS-059_COMPLETED; WBS-060_COMPLETED; WBS-061_COMPLETED; BLOCKED_WBS062_BK_ORDER_CONDITION.
Current PR/WBS: WBS-062 / PR11 BK tests blocked.
Blocked WBS: WBS-062.
Previous blocking status: none for WBS-061.
Last completed task: WBS-061 residual-blocking parameters sourced from WP239 and residual wrapper mode added.
Last runtime task: Installed and verified Octave 11.1.0 plus Dynare 7.0.
Next safe task: resolve BK order-condition failure through equation/registry/state classification review.
Blocker classification: Dynare BK order condition failed.
Blockers: temporary `steady; check;` run reports 26 eigenvalues larger than 1 in modulus for 28 forward-looking variables; order condition is not verified.
Required user action: review WBS-057 model equations/state timing/classification before WBS-063 IRFs; do not alter model economics automatically.
Files changed: `src/diagnostics/run_dynare.py`, `tests/test_model_outputs.py`, `docs/PROJECT_STATUS.md`.
Tests run: `python -m pytest` - 87 passed; `git diff --check` - passed.
Dynare BK check: `python src/diagnostics/run_dynare.py --mode bk` - failed by BK order condition; no generated Dynare files kept in repo.
Commit hash: pending for WBS-062 blocker record.
Safe to continue: false for WBS-063 IRFs and later Gate 3 tasks until BK passes.

Visual status:

Progress metric: 64/86 WBS complete, approximately 74% by WBS item count. This is not effort-weighted; the remaining Dynare, estimation, and validation work is heavier than early documentation WBS.

| Area / PR | WBS scope | Done | Status | Next / blocker |
|---|---:|---:|---|---|
| Preflight + baseline | PRE-000, 000 | 2/2 | complete | none |
| Gate 0 decisions/configs | 001..009.5 | 11/11 | complete | none |
| PR 03 repo bootstrap | 010..020 | 11/11 | complete | none |
| PR 04 data dictionary skeleton | 021..023 | 3/3 | complete | none |
| PR 05 literature map | 033A | 1/1 | complete | none |
| PR 06 source verification | 024..027, 045..051 | 11/11 | complete | auxiliary TBDs remain documented |
| PR 07 data contracts | 028..032 | 5/5 | complete | none |
| PR 08 equation registry | 034..044 | 11/11 | complete | none |
| PR 09 dataset generation | 052 | 1/1 | complete | none |
| PR 10 calibration notes | 053 | 1/1 | complete | none |
| PR 11 Dynare calibrated model | 054..064 | 8/11 | WBS-062 blocked | resolve BK order condition |
| PR 12 identification | 065..067 | 0/3 | blocked | requires solved Gate 3 model |
| PR 13 estimation smoke/priors | 068..071a | 0/5 | blocked | requires Gate 4 |
| PR 14 Bayesian estimation | 072..073 | 0/2 | blocked | requires smoke/pilot gates |
| PR 15 validation/backtesting | 074..079 | 0/6 | blocked | requires estimation outputs |
| Post-MVP Redux/sovereign | 080..081 | 0/2 | out of MVP | only after Gate 6 and separate decision |

Gate view:

| Gate | Status | Evidence |
|---|---|---|
| Gate 0 | approved | `docs/gate0_approval_record.md` |
| Gate 1a | complete | `docs/02_data_dictionary.md` |
| Gate 1b | approved | `docs/gate1b_approval_record.md` |
| Gate 2a | complete | `docs/00a_literature_map.md` |
| Gate 2b | approved | `docs/gate2b_approval_record.md` |
| Gate 3 | blocked | WBS-054 structure, WBS-055 `calibration.m`, WBS-056 `steady_state.m`, WBS-057 `samba_classic.mod`, WBS-058 `shocks.inc`, WBS-059 `observables.inc`, WBS-060 wrapper, and WBS-061 residual tests complete; WBS-062 blocked by BK order condition |
| Gate 4 | not started | no identification outputs |
| Gate 5a/5b | not started | no estimation outputs |
| Gate 6 | not started | no validation/backtesting outputs |
