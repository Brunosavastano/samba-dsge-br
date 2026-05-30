# WBS-072 Blockers

Status: `BLOCKED_WBS072_ACCEPTANCE_BAND`

WBS-072 requires an MH pilot before WBS-073 full MH. Bruno approved the pilot
configuration on 2026-05-30 with R-hat unavailable/above 1.1 treated as a
diagnostic warning, not a blocker.

Approved configuration:
- `mh_replic`: 2000 per chain;
- chains: 2;
- blocks: 2 if compatible with wrapper/runtime;
- burn-in: 50 percent;
- target acceptance band: 0.20 to 0.35;
- pilot artifacts only.

Checked sources:
- `docs/PROJECT_STATUS.md`
- `docs/08_implementation_plan.md`
- `docs/04_estimation_strategy.md`
- WBS-071/WBS-071a result docs

Proposal created and approved: `docs/wbs072_mh_pilot_config.md`.

Pilot attempt result after fixing acceptance parser:
- command: `python src/diagnostics/run_dynare.py --mode mh-pilot --timeout-seconds 1800`;
- Dynare return code: 3221225477;
- elapsed seconds: 931.484;
- finite likelihood reported: true;
- last finite log posterior/likelihood: -467.15353;
- acceptance ratios: chain 1 = 0.169, chain 2 = 0.096;
- average acceptance ratio: 0.1325;
- target acceptance band: 0.20 to 0.35;
- R-hat: unavailable warning, per approved amendment;
- stdout included `pstdev Inf` values in posterior summary rows for
  inverse-gamma priors; these are prior/posterior table standard-deviation
  entries and no likelihood NaN/Inf was reported.

WBS-072 remains blocked because average pilot acceptance is below the approved
0.20 to 0.35 band, and the Dynare/Octave process still returned nonzero after
the pilot diagnostics. WBS-073 full MH, backtesting, Redux, and sovereign
outputs remain forbidden.
