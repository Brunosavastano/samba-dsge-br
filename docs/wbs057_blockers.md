# WBS-057 Blockers

Status: `BLOCKED_WBS057_HUMAN_FORMULA_REVIEW`

WBS-057 remains blocked before `model/samba_classic/samba_classic.mod`.

WP239 local reference: available at `docs/references/bcb_wp239_samba.pdf`.

Dynare-ready rows: 24.

Resolved to Dynare-ready in this pass: 15.

Remaining true WBS-057 blockers: 1.

Deferred to WBS-058 `shocks.inc`: 11 rows (`EQ-SHOCK-003`, `EQ-SHOCK-005`..`EQ-SHOCK-009`, `EQ-SHOCK-011`..`EQ-SHOCK-012`, `EQ-SHOCK-014`..`EQ-SHOCK-016`).

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items. Existing observable rows (`EQ-PRICE-003`, `EQ-MEAS-001..EQ-MEAS-015`) remain outside WBS-057.

Needs human formula review:

- `EQ-AGG-004`: exact output-gap/potential-output formula was not confidently located in WP239 Section 2.6, Section 2.7, or Appendix C.4-C.5. Do not infer it from generic accounting.

Still missing in sources: none after the WP239 Appendix C and Tables 2/3 pass.

Duplicate or not-required rows must not be implemented twice: `EQ-SHOCK-001`, `EQ-SHOCK-002`, `EQ-SHOCK-004`, `EQ-SHOCK-010`, `EQ-SHOCK-013`, `EQ-SHOCK-017`, `EQ-PRICE-003`, and `EQ-MEAS-001..EQ-MEAS-015`.

WBS-057b cannot proceed while `EQ-AGG-004` needs human formula review.

Next source to check: human/assistant visual review of WP239 Section 2.6, Section 2.7, Appendix C.4-C.5, and approved project decisions for the exact output-gap/potential-output formula.

Do not create `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.
