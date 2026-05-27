# WBS-057 Blockers

Status: `BLOCKED_WBS057_MOD_TRANSCRIPTION`

WBS-057 source/mapping review is complete, but `model/samba_classic/samba_classic.mod` must not be created until exact executable Dynare equations are transcribed from approved sources.

Blocker classification: missing_formula_text.

Not a mechanical test-contract blocker.

Not a subjective macro-judgment blocker.

WP239 local reference: available at `docs/references/bcb_wp239_samba.pdf`.

Dynare-ready rows: 24.

Resolved to Dynare-ready in this pass: 15.

Remaining true WBS-057 source blockers: 0.

Remaining WBS-057b implementation blocker: exact executable Dynare equation text is not present in the project docs. The sourcing table records WP239 locations and registry mappings, but not the final equation text needed to create `.mod` without interpretation. Remaining executable formula-text blockers: 1 WBS-level blocker.

Deferred to WBS-058 `shocks.inc`: 11 rows (`EQ-SHOCK-003`, `EQ-SHOCK-005`..`EQ-SHOCK-009`, `EQ-SHOCK-011`..`EQ-SHOCK-012`, `EQ-SHOCK-014`..`EQ-SHOCK-016`).

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items. Existing observable rows (`EQ-PRICE-003`, `EQ-MEAS-001..EQ-MEAS-015`) remain outside WBS-057.

Resolved final blocker:

- `EQ-AGG-004`: not required as a separate WBS-057 `.mod` equation. `y_gap` enters the `.mod` through `EQ-MON-001` Taylor-rule mapping; `y_pot` and output-gap measurement/reporting treatment remain outside WBS-057.

Needs human formula review: none.

Still missing in sources: none after the WP239 Appendix C and Tables 2/3 pass.

Duplicate or not-required rows must not be implemented twice: `EQ-SHOCK-001`, `EQ-SHOCK-002`, `EQ-SHOCK-004`, `EQ-SHOCK-010`, `EQ-SHOCK-013`, `EQ-SHOCK-017`, `EQ-PRICE-003`, and `EQ-MEAS-001..EQ-MEAS-015`.

WBS-057b cannot proceed to file creation until exact formulas are transcribed/reviewed. This file does not create or authorize `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign work.

Next task: transcribe exact WP239 Appendix C formulas and Tables 2/3 parameter mappings into approved WBS-057b implementation inputs, then create `samba_classic.mod` only from that exact material.

Do not create `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.
