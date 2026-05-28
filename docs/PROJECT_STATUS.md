# Project Status

Updated: 2026-05-27

Current gate: Gate 3 started; Gate 1b approved for core source IDs; Gate 2b approved for minimum viable equation registry.
Execution status: WBS-057_COMPLETED; WBS-058_COMPLETED; WBS-059_COMPLETED.
Current PR/WBS: WBS-059 / PR11 `observables.inc` created.
Blocked WBS: none for WBS-059.
Previous blocking status: BLOCKED_WBS059_MEASUREMENT_MAPPING.
Last completed task: WBS-058 `shocks.inc` created from WP239 Table 3 posterior-mean standard deviations.
Last runtime task: Installed and verified Octave 11.1.0 plus Dynare 7.0.
Next safe task: WBS-060 Dynare wrapper.
Blocker classification: none for WBS-059 include creation.
Blockers: remaining WBS-059 blockers for `observables.inc`: 0. Several WP239 observables remain deferred because their model variables are `varexo`, their data dictionary source is missing, or no WBS-052 data file exists.
Required user action: continue to WBS-060 only; do not create priors, outputs, estimation, Redux, or sovereign files.
Files changed: `model/samba_classic/observables.inc`, `model/samba_classic/samba_classic.mod`, `docs/wbs059_observable_sourcing.md`, `docs/wbs059_blockers.md`, `docs/PROJECT_STATUS.md`, and WBS-059 test-contract updates.
Tests run: `python -m pytest` - 82 passed; `git diff --check` - passed.
Dynare parse: passed in temp directory with `dynare samba_classic.mod noclearall nolog`; no generated Dynare files kept in repo.
Commit hash: pending for WBS-059 implementation.
Safe to continue: true for WBS-060 Dynare wrapper only. Do not create priors, fake outputs, data, estimation, Redux, or sovereign extension.

Visual status:

Progress metric: 62/86 WBS complete, approximately 72% by WBS item count. This is not effort-weighted; the remaining Dynare, estimation, and validation work is heavier than early documentation WBS.

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
| PR 11 Dynare calibrated model | 054..064 | 6/11 | WBS-059 complete | next WBS-060 Dynare wrapper |
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
| Gate 3 | in progress | WBS-054 structure, WBS-055 `calibration.m`, WBS-056 `steady_state.m`, WBS-057 `samba_classic.mod`, WBS-058 `shocks.inc`, and WBS-059 `observables.inc` complete; WBS-060 wrapper next |
| Gate 4 | not started | no identification outputs |
| Gate 5a/5b | not started | no estimation outputs |
| Gate 6 | not started | no validation/backtesting outputs |
