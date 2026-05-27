# WBS-057 Blockers

Status: `WBS-057_READY_FOR_MOD`

WBS-057 source/mapping review and WBS-057b formula transcription are complete. `model/samba_classic/samba_classic.mod` may be created in the next WBS-057b implementation step using only the transcribed formulas in `docs/wbs057_equation_sourcing.md`.

Previous blocker classification: missing_formula_text.

Not a mechanical test-contract blocker.

Not a subjective macro-judgment blocker.

WP239 local reference: available at `docs/references/bcb_wp239_samba.pdf`.

Dynare-ready rows: 24.

Resolved to Dynare-ready in this pass: 15.

Remaining true WBS-057 source blockers: 0.

Remaining WBS-057b implementation blocker: none after formula transcription. Remaining executable formula-text blockers: 0.

Deferred to WBS-058 `shocks.inc`: 11 rows (`EQ-SHOCK-003`, `EQ-SHOCK-005`..`EQ-SHOCK-009`, `EQ-SHOCK-011`..`EQ-SHOCK-012`, `EQ-SHOCK-014`..`EQ-SHOCK-016`).

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items. Existing observable rows (`EQ-PRICE-003`, `EQ-MEAS-001..EQ-MEAS-015`) remain outside WBS-057.

Resolved final blocker:

- `EQ-AGG-004`: not required as a separate WBS-057 `.mod` equation. `y_gap` enters the `.mod` through `EQ-MON-001` Taylor-rule mapping; `y_pot` and output-gap measurement/reporting treatment remain outside WBS-057.

Needs human formula review: none.

Still missing in sources: none after the WP239 Appendix C and Tables 2/3 pass.

Duplicate or not-required rows must not be implemented twice: `EQ-SHOCK-001`, `EQ-SHOCK-002`, `EQ-SHOCK-004`, `EQ-SHOCK-010`, `EQ-SHOCK-013`, `EQ-SHOCK-017`, `EQ-PRICE-003`, and `EQ-MEAS-001..EQ-MEAS-015`.

WBS-057b can proceed to `samba_classic.mod` creation in the next step. This file does not create or authorize `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign work.

Next task: create `samba_classic.mod` using only rows marked Dynare-ready and formulas transcribed in `docs/wbs057_equation_sourcing.md`.

Do not create `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.
