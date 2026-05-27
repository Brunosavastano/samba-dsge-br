# WBS-057 Blockers

Status: `BLOCKED_WBS057_EQUATION_SOURCES`

WBS-057 remains blocked before `model/samba_classic/samba_classic.mod`.

WP239 local reference: available at `docs/references/bcb_wp239_samba.pdf`.

Dynare-ready rows: 9.

Remaining true WBS-057 blockers: 16.

Deferred to WBS-058 `shocks.inc`: 11 rows (`EQ-SHOCK-003`, `EQ-SHOCK-005`..`EQ-SHOCK-009`, `EQ-SHOCK-011`..`EQ-SHOCK-012`, `EQ-SHOCK-014`..`EQ-SHOCK-016`).

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items. Existing observable rows (`EQ-PRICE-003`, `EQ-MEAS-001..EQ-MEAS-015`) remain outside WBS-057.

Exact formula still unavailable: `EQ-AGG-004` output-gap/potential-output accounting.

Formula available but mapping/calibration incomplete for WBS-057:
`EQ-EXT-003`; `EQ-FISC-002`..`EQ-FISC-004`; `EQ-HH-001`..`EQ-HH-004`; `EQ-FIRM-001`..`EQ-FIRM-004`; `EQ-AGG-001`..`EQ-AGG-003`.

Duplicate or not-required rows must not be implemented twice: `EQ-SHOCK-001`, `EQ-SHOCK-002`, `EQ-SHOCK-004`, `EQ-SHOCK-010`, `EQ-SHOCK-013`, `EQ-SHOCK-017`, `EQ-PRICE-003`, and `EQ-MEAS-001..EQ-MEAS-015`.

WBS-057b cannot proceed while the 16 true WBS-057 blockers remain.

Next source to check: WP239 Appendix C plus Table 2/Table 3 for every unresolved parameter, weight, or mapping needed by those formulas.

Do not create `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.
