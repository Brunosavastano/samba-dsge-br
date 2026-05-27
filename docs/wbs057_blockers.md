# WBS-057 Blockers

Status: `BLOCKED_WBS057_EQUATION_SOURCES`

WBS-057 remains blocked before `model/samba_classic/samba_classic.mod`.

WP239 local reference: available at `docs/references/bcb_wp239_samba.pdf`.

Dynare-ready rows: 9.

Resolved to Dynare-ready in this pass: 0.

Remaining true WBS-057 blockers: 16.

Deferred to WBS-058 `shocks.inc`: 11 rows (`EQ-SHOCK-003`, `EQ-SHOCK-005`..`EQ-SHOCK-009`, `EQ-SHOCK-011`..`EQ-SHOCK-012`, `EQ-SHOCK-014`..`EQ-SHOCK-016`).

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items. Existing observable rows (`EQ-PRICE-003`, `EQ-MEAS-001..EQ-MEAS-015`) remain outside WBS-057.

Remaining true WBS-057 blockers:

- `EQ-EXT-003`: still missing project-approved accounting weights/debt-anchor mapping for C.37-C.39.
- `EQ-FISC-002`: still missing project-approved fiscal coefficients and government-spending share mapping for C.30/C.33.
- `EQ-FISC-003`: still missing project-approved lambda_B inputs and debt-law parameter mapping for C.34.
- `EQ-FISC-004`: still missing project-approved `rho_T`/tax-process mapping for C.32.
- `EQ-HH-001`: still missing project-approved preference, habit, discounting and investment parameter mappings for C.1-C.10.
- `EQ-HH-002`: still missing project-approved habit-state and parameter mappings for C.1-C.10.
- `EQ-HH-003`: still missing project-approved wage/labor and markup parameter mappings for C.10-C.13.
- `EQ-HH-004`: still missing project-approved rule-of-thumb share/tax mappings.
- `EQ-FIRM-001`: still missing project-approved production-share and sectoral cost-share mappings for C.11-C.17.
- `EQ-FIRM-002`: still missing project-approved price-rigidity, indexation and markup mappings for C.14-C.21/C.24-C.27.
- `EQ-FIRM-003`: still missing project-approved investment-adjustment, capital and discounting mappings for C.4-C.9/C.11.
- `EQ-FIRM-004`: still missing project-approved imported-input and relative-price mappings for C.16-C.17/C.38.
- `EQ-AGG-001`: still missing project-approved sector weights for C.35-C.36.
- `EQ-AGG-002`: still missing project-approved absorption/NX weights and NFA-link mappings for C.37-C.39.
- `EQ-AGG-003`: still missing project-approved GDP and deflator weights for C.40-C.42.
- `EQ-AGG-004`: still missing exact output-gap/potential-output formula from WP239 or approved project docs.

Duplicate or not-required rows must not be implemented twice: `EQ-SHOCK-001`, `EQ-SHOCK-002`, `EQ-SHOCK-004`, `EQ-SHOCK-010`, `EQ-SHOCK-013`, `EQ-SHOCK-017`, `EQ-PRICE-003`, and `EQ-MEAS-001..EQ-MEAS-015`.

WBS-057b cannot proceed while the 16 true WBS-057 blockers remain.

Next source to check: manually transcribe the exact WP239 Appendix C formulas and convert Tables 2/3 entries into approved project calibration names before creating `.mod`.

Do not create `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.
