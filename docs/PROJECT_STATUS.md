# Project Status

Updated: 2026-06-06

Current gate: Gate 5a completed; Gate 5b MH pilot completed; WBS-073 guarded full-MH blocked by disk guard and MH diagnostics; Gate 4 completed; Gate 3 completed; Gate 1b approved for core source IDs; Gate 2b approved for minimum viable equation registry.
Execution status: WBS-057_COMPLETED; WBS-058_COMPLETED; WBS-059_COMPLETED; WBS-060_COMPLETED; WBS-061_COMPLETED; WBS-062_COMPLETED; WBS-063_COMPLETED; WBS-064_COMPLETED; GATE3_COMPLETED; WBS-065_COMPLETED; WBS-066_COMPLETED; WBS-067_COMPLETED; GATE4_COMPLETED; WBS-068_COMPLETED; WBS-069_COMPLETED; WBS-070_COMPLETED; WBS-071_COMPLETED; WBS-071a_COMPLETED; WBS-072_CONFIG_APPROVED; WBS-072_COMPLETED; WBS-073_APPROVED_FOR_FULL_MH; WBS073_EXTERNAL_DRIVE_PREPARED; WBS073_DISK_GUARD_IMPLEMENTED_PENDING_REVIEW; BLOCKED_WBS073_FULL_MH_DISK_ABORT_AND_DIAGNOSTICS.
Current PR/WBS: WBS-073 / PR14 guarded full-MH diagnostics.
Blocked WBS: WBS-073 full MH blocked by disk guard abort plus acceptance and R-hat diagnostics outside approved criteria.
Previous blocking status: BLOCKED_WBS066_IDENTIFICATION_SOLVE resolved mechanically by using Dynare's documented diffuse-filter identification path.
Last completed task: WBS-072 approved MH pilot completed with tuned proposal scale.
Last attempted task: guarded WBS-073 full-MH rerun after archiving stale external workdir and applying a mechanical wrapper pipe-drain fix.
Last runtime task: Installed and verified Octave 11.1.0 plus Dynare 7.0.
Next safe task: Bruno/assistant review WBS-073 full-MH runtime/post-processing and MH diagnostics before approving any rerun or tuning change.
Blocker classification: operational storage/runtime plus MH diagnostic blocker; no model equations, priors, data, calibration, observables, shocks, sample, or MH configuration changed.
Blockers: `docs/wbs073_blockers.md` records `BLOCKED_WBS073_FULL_MH_DISK_ABORT_AND_DIAGNOSTICS`.
Required user action: review WBS-073 disk abort, acceptance ratio 0.187, and max R-hat 4.054739157907651 before any new full-MH attempt.
Files changed: `src/diagnostics/run_dynare.py`, `tests/test_run_dynare_storage.py`, `docs/wbs073_runtime_diagnostics.md`, `docs/wbs073_blockers.md`, `docs/PROJECT_STATUS.md`, and lightweight `outputs/posterior/full/wbs073_full_mh_*` artifacts.
Tests run: `python -m pytest` with Dynare/Octave removed from PATH - 116 passed, 5 skipped; `git diff --check` - passed.
Dynare results: WBS-073 full-MH guarded run failed; chains completed, finite likelihood reported, no NaN/Inf likelihood observed, average acceptance 0.187 outside 0.20-0.35, max R-hat 4.054739157907651 above 1.1, disk guard abort at `D:\` free space 49.937 GB.
Runtime diagnosis: stale workdir archived, wrapper pipe-drain issue fixed, raw chain artifacts kept external/untracked, `C:\` remained protected and `D:\` returned to approximately 923.37 GB free after cleanup.
Commit hash: see latest git commit for WBS-073 guarded full-MH diagnostic update.
Safe to continue: false for WBS-073 rerun and WBS-074; forbidden next without prompt: rerun/full-MH tuning/WBS-074/backtesting/Redux/sovereign.

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
| PR 14 Bayesian estimation | 072..073 | 1/2 | blocked | WBS-073 disk guard abort; acceptance/R-hat criteria failed |
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
| Gate 5a/5b | Gate 5a complete; Gate 5b pilot complete; WBS-073 blocked | WBS-071a estimation smoke complete; WBS-072 accepted with tuned `mh_jscale=0.337313`; WBS-073 guarded full-MH blocked by disk guard abort, acceptance 0.187, and max R-hat 4.0547 |
| Gate 6 | not started | no validation/backtesting outputs |
