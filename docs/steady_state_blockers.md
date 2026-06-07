# Steady-State Blockers

Status: `BLOCKED_TEST_CONTRACT_WBS056`

Missing steady-state source count: 0.

Steady-state naming conflict count: 0.

Current blocker: WBS-056 cannot create `model/samba_classic/steady_state.m` in this run because legacy `.m` guardrail tests outside the allowed file list still allow only `model/samba_classic/calibration.m`.

Files needing later narrow update: `tests/test_dataset_outputs.py` and `tests/test_validation_templates.py`.

Guardrail to preserve: allow exactly `model/samba_classic/calibration.m` and `model/samba_classic/steady_state.m`; keep `.mod`, `.inc`, data, outputs, estimation, Redux, and sovereign extension blocked.

Exact next action: authorize narrow legacy test update for WBS-056.
