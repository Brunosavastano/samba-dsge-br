# samba_classic Model Structure

Status: WBS-054 structure only.

This directory reserves the executable model location for the calibrated SAMBA classic MVP. WBS-054 creates structure and planning metadata only.

No Dynare model, MATLAB/Octave implementation file, include file, equation, calibration value, steady-state value, result, estimation output, Redux extension, or sovereign extension is approved here.

Future planned files, subject to later WBS gates:

- `calibration.m` in WBS-055.
- `steady_state.m` in WBS-056.
- `samba_classic.mod` in WBS-057.
- `shocks.inc` in WBS-058.
- `observables.inc` in WBS-059.

Equations remain governed by `docs/01_equation_registry.md`. Calibration rationale remains governed by `docs/03_calibration_notes.md`.
