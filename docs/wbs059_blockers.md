# WBS-059 Blockers

Status: `BLOCKED_WBS059_MEASUREMENT_MAPPING`

`model/samba_classic/observables.inc` was not created.

Current blockers:

- Core WBS-052 data columns are not yet mapped to log-linear model deviations or compatible measurement equations.
- `pi`, `x`, and `m` are currently `varexo` in `samba_classic.mod`, so direct `varobs` is not safe.
- EQ-MEAS-001 through EQ-MEAS-015 remain `measurement_draft` with `measurement_transform_pending_gate1b`.
- Auxiliary/non-core observables are missing generated data and, for several rows, still have TBD sources.

Next action: finalize WBS-059 measurement equations and scaling/deviation transforms before creating `observables.inc`.
