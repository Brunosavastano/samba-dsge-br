# WBS-072 Blockers

Status: `WBS-072_CONFIG_PROPOSED`

WBS-072 requires an MH pilot before WBS-073 full MH, but the approved project
docs currently specify only "short chains" and preliminary acceptance/R-hat.

Missing approved configuration:
- `mh_replic` for the pilot chain run;
- number of chains or blocks to run/evaluate;
- acceptance-rate pass band;
- preliminary R-hat parameters and threshold scope;
- minimal allowed files under `outputs/posterior/pilot/`.

Checked sources:
- `docs/PROJECT_STATUS.md`
- `docs/08_implementation_plan.md`
- `docs/04_estimation_strategy.md`
- WBS-071/WBS-071a result docs

Proposal created: `docs/wbs072_mh_pilot_config.md`.

The proposal remains unapproved. This is not a mechanical blocker and must not
be resolved by running MH until Bruno approves the proposed settings.

WBS-072 remains blocked for execution until Bruno approves the pilot
configuration. WBS-073 full MH, backtesting, Redux, and sovereign outputs remain
forbidden.
