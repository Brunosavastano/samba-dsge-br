# Project Status

Updated: 2026-06-05

Current gate: Gate 5a completed; Gate 5b MH pilot completed; WBS-073 external-drive scratch strategy prepared for review; Gate 4 completed; Gate 3 completed; Gate 1b approved for core source IDs; Gate 2b approved for minimum viable equation registry.
Execution status: WBS-057_COMPLETED; WBS-058_COMPLETED; WBS-059_COMPLETED; WBS-060_COMPLETED; WBS-061_COMPLETED; WBS-062_COMPLETED; WBS-063_COMPLETED; WBS-064_COMPLETED; GATE3_COMPLETED; WBS-065_COMPLETED; WBS-066_COMPLETED; WBS-067_COMPLETED; GATE4_COMPLETED; WBS-068_COMPLETED; WBS-069_COMPLETED; WBS-070_COMPLETED; WBS-071_COMPLETED; WBS-071a_COMPLETED; WBS-072_CONFIG_APPROVED; WBS-072_COMPLETED; WBS-073_APPROVED_FOR_FULL_MH; WBS073_EXTERNAL_DRIVE_PREPARED; BLOCKED_WBS073_EXTERNAL_DRIVE_REVIEW.
Current PR/WBS: WBS-073 / PR14 external-drive scratch preparation.
Blocked WBS: WBS-073 full MH rerun.
Previous blocking status: BLOCKED_WBS066_IDENTIFICATION_SOLVE resolved mechanically by using Dynare's documented diffuse-filter identification path.
Last completed task: WBS-072 approved MH pilot completed with tuned proposal scale.
Last attempted task: WBS-073 full-MH rerun caused operational disk exhaustion on `C:\`.
Last runtime task: Installed and verified Octave 11.1.0 plus Dynare 7.0.
Next safe task: Bruno reviews external-drive strategy before WBS-073 rerun.
Blocker classification: operational storage/runtime blocker; no model equations, priors, data, calibration, observables, or shocks changed.
Blockers: `docs/wbs073_blockers.md` records `BLOCKED_WBS073_EXTERNAL_DRIVE_REVIEW`.
Required user action: confirm/review the external-drive full-MH command before retrying WBS-073.
Files changed: `src/diagnostics/run_dynare.py`, `docs/wbs073_external_drive_strategy.md`, `docs/wbs073_blockers.md`, `docs/PROJECT_STATUS.md`, `tests/test_run_dynare_storage.py`.
Tests run: `python -m pytest` with Dynare/Octave removed from `PATH` to respect the no-Dynare preparation constraint - 116 passed; `git diff --check` - passed.
Dynare results: not run for this preparation task.
Runtime diagnosis: `D:\` exists with approximately 923 GB free and is prepared for WBS-073 scratch; `C:\` remains protected by a 30 GB preflight margin because Windows pagefile/cache may still use it.
Commit hash: pending for WBS-073 external-drive preparation commit.
Safe to continue: false for full MH; forbidden next without prompt: WBS-073 rerun/WBS-074/backtesting/Redux/sovereign.

Visual status:

Progress metric: 75/86 WBS complete, approximately 87% by WBS item count. This is not effort-weighted; the remaining estimation and validation work is heavier than early documentation WBS.

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
| PR 11 Dynare calibrated model | 054..064 | 11/11 | complete | Gate 3 closed |
| PR 12 identification | 065..067 | 3/3 | complete | Gate 4 closed |
| PR 13 estimation smoke/priors | 068..071a | 5/5 | complete | none |
| PR 14 Bayesian estimation | 072..073 | 1/2 | blocked | WBS-073 external-drive scratch strategy prepared; rerun awaits review |
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
| Gate 3 | completed | WBS-054 structure, WBS-055 `calibration.m`, WBS-056 `steady_state.m`, WBS-057 `samba_classic.mod`, WBS-058 `shocks.inc`, WBS-059 `observables.inc`, WBS-060 wrapper, WBS-061 residual tests, WBS-062 BK tests, WBS-063 IRF tests, and WBS-064 MVP report complete |
| Gate 4 | completed | WBS-065 protocol complete; WBS-066 reduced-form identification diagnostics complete; WBS-067 treatment decisions recorded |
| Gate 5a/5b | Gate 5a complete; Gate 5b pilot complete; WBS-073 blocked | WBS-071a estimation smoke complete; WBS-072 accepted with tuned `mh_jscale=0.337313`; WBS-073 external-drive scratch strategy prepared for review |
| Gate 6 | not started | no validation/backtesting outputs |
