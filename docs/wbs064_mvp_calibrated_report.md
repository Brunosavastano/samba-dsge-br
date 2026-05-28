# WBS-064 MVP Calibrated Report

Status: Gate 3 completed for the calibrated SAMBA classic MVP.

## Scope

Model scope: SAMBA classic calibrated MVP, log-linear, first order, no Redux and
no sovereign extension.

Model files included:
- `model/samba_classic/samba_classic.mod`
- `model/samba_classic/calibration.m`
- `model/samba_classic/steady_state.m`
- `model/samba_classic/shocks.inc`
- `model/samba_classic/observables.inc`
- `src/diagnostics/run_dynare.py`

## Sample And Config Status

- Sample config remains documented in `config/sample.yaml`.
- Classic MVP sample: 2003Q1-2019Q4, quarterly, final revised, COVID excluded.
- No new data, source IDs, posterior outputs, backtesting outputs, Redux files,
  or sovereign-extension files are created by WBS-064.

## Calibration Source Status

- Calibration values used by `calibration.m` are documented in
  `docs/03_calibration_notes.md`.
- Shock standard deviations used by `shocks.inc` are sourced from WP239 Table 3
  and documented in `docs/wbs058_shock_sourcing.md`.
- IRF restrictions are sourced from WP239 Figure 3 and documented in
  `docs/wbs063_irf_targets.md`.

## Validated Results

Commands were run through the existing Dynare wrapper in a temporary working
directory, without committing generated Dynare clutter.

- Parse/smoke: `python src/diagnostics/run_dynare.py --mode smoke` passed.
- Residuals: `python src/diagnostics/run_dynare.py --mode residuals` passed;
  36 equations, 0 nonfinite residuals, max absolute residual 0.0.
- BK: `python src/diagnostics/run_dynare.py --mode bk` passed; 26 eigenvalues
  larger than one for 26 forward-looking variables; order and rank conditions
  verified.
- IRFs: `python src/diagnostics/run_dynare.py --mode irf` passed; 5 targets
  evaluated, 5 passed, 0 failed; no persistent outputs created.

## Limitations

- No Bayesian estimation yet.
- No local identification yet.
- No priors or `priors.inc` yet.
- No posterior outputs.
- No backtesting outputs.
- No Redux model.
- No sovereign extension.
- No Gate 6 full validation.

## Gate 3 Decision

Gate 3 is closed for the calibrated SAMBA classic MVP. The next safe task is
WBS-065, the identification protocol.
