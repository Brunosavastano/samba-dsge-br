# Equation Registry - samba-dsge-br

**Documento:** `docs/01_equation_registry.md`
**Status:** Gate 2b template
**Fonte canonica:** `docs/00a_literature_map.md`
**Criado em:** 2026-05-26

---

## 0. Gate status

```yaml
gate: Gate 2b
wbs: WBS-034
gate_status: template_created
gate2b_passed: false
dynare_allowed: false
model_file_allowed: false
source_memory_allowed: false
core_blocks_registered: false
registry_version: 0.1.0-template
created_at: 2026-05-26
updated_at: 2026-05-26
```

Gate 2b is not passed. This file is a template only.

---

## 1. Registry policy

```text
- Do not register equations from memory.
- Every future equation entry must point to `docs/00a_literature_map.md`.
- Equation numbers may be used as locators, but formulas are entered only in the relevant WBS.
- Measurement equations remain draft until Gate 1b source IDs are verified.
- Dynare and `model/` files remain blocked until Gate 2b passes.
```

---

## 2. Entry schema

```csv
field,required,description
equation_id,yes,Stable unique ID using EQ-<BLOCK>-###.
block,yes,MON EXT FISC ADMIN HH FIRM AGG SHOCK MEAS or AUX.
title,yes,Short human-readable label; not a formula.
equation_type,yes,structural identity shock_process measurement_draft or auxiliary.
source_map_id,yes,Map row from docs/00a_literature_map.md.
source_reference_id,yes,Primary reference ID such as BCB_WP239.
source_locator,yes,Exact section equation table or figure locator.
variables,yes,Variables used by the equation or none.
parameters,yes,Parameters used by the equation or none.
shocks,yes,Shocks used by the equation or none.
tests,yes,Expected validation tests or none.
status,yes,draft sourced reviewed approved deferred or rejected.
gate,yes,WBS or gate that owns the entry.
notes,no,Short implementation notes.
```

---

## 3. Planned namespaces

```csv
namespace,block,source_map_id,next_wbs,status
EQ-MON,MON,LM-MON-001,WBS-035,ready_for_registry_entry
EQ-EXT,EXT,LM-EXT-001,WBS-036,ready_for_registry_entry
EQ-FISC,FISC,LM-FISC-001,WBS-037,ready_for_registry_entry
EQ-PRICE,ADMIN,LM-PRICE-ADMIN-001,WBS-038,ready_for_registry_entry
EQ-HH,HH,LM-HH-001,WBS-039,ready_for_registry_entry
EQ-FIRM,FIRM,LM-FIRM-001,WBS-040,ready_for_registry_entry
EQ-AGG,AGG,LM-AGG-001,WBS-041,ready_for_registry_entry
EQ-SHOCK,SHOCK,LM-SHOCK-001,WBS-042,ready_for_registry_entry
EQ-MEAS,MEAS,LM-MEAS-001,WBS-043,draft_until_gate1b
```

---

## 4. Registry entries

No equation entries are registered in WBS-034.

```csv
equation_id,block,title,equation_type,source_map_id,source_reference_id,source_locator,variables,parameters,shocks,tests,status,gate,notes
```

