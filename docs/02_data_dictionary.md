# Data Dictionary - samba-dsge-br

**Documento:** `docs/02_data_dictionary.md`
**Status:** Gate 1a skeleton
**Fonte canonica:** `samba_dsge_br_spec_standalone_consolidado.md`
**Gate anterior:** Gate 0 approved
**Criado em:** 2026-05-25

---

## 0. Gate status

```yaml
gate: Gate 1a
gate_status: skeleton_created
data_extraction_allowed: false
core_source_ids_verified: false
source_id_invention_allowed: false
final_revised_and_realtime_must_not_mix: true
```

Gate 1b is not passed.

---

## 1. Source policy

```text
- Nenhum source_id pode ser inventado por memoria interna.
- Fonte generica isolada, como "BCB" ou "IBGE", nao basta.
- Se a fonte nao estiver verificada, usar TBD-verify-in-task-<WBS-ID>.
- Gate 1a permite placeholders.
- Gate 1b exige source_id verificado para os core sources.
- Nenhum dado real deve ser extraido, transformado ou salvo antes de Gate 1b.
- Dados final-revised e real-time vintage nao podem ser misturados no mesmo experimento.
```

---

## 2. DataSeries schema

Required metadata fields for every planned series:

```text
series_id
variable
description
source
source_id
source_status
revision_policy
vintage_date
base_year
frequency_raw
frequency_model
seasonal_adjustment
transform
quarterly_conversion
sample_scope
wbs
gate_status
notes
```

Allowed placeholder format before Gate 1b:

```text
TBD-verify-in-task-<WBS-ID>
```

---

## 3. Core sources required for Gate 1b

The following core sources must have verified `source_id` values before extraction, transformation, or dataset generation.

```csv
series_id,variable,description,source,source_id,source_status,revision_policy,frequency_model,wbs,gate_status
br_gdp_real,y,PIB real,TBD,TBD-verify-in-task-WBS-024,tbd,final_revised,quarterly,WBS-024,Gate 1a skeleton
br_ipca_headline,pi,Inflacao IPCA cheia,TBD,TBD-verify-in-task-WBS-025,tbd,final_revised,quarterly,WBS-025,Gate 1a skeleton
br_selic,r,Taxa Selic,TBD,TBD-verify-in-task-WBS-026,tbd,final_revised,quarterly,WBS-026,Gate 1a skeleton
br_real_exchange_rate,q,Cambio real with q_t up as BRL real depreciation,TBD,TBD-verify-in-task-WBS-027,tbd,final_revised,quarterly,WBS-027,Gate 1a skeleton
br_private_consumption,c,Consumo privado real,TBD,TBD-verify-in-task-WBS-045,tbd,final_revised,quarterly,WBS-045,Gate 1a skeleton
br_investment,i,Investimento real,TBD,TBD-verify-in-task-WBS-046,tbd,final_revised,quarterly,WBS-046,Gate 1a skeleton
br_government_consumption,g,Gasto do governo real,TBD,TBD-verify-in-task-WBS-047,tbd,final_revised,quarterly,WBS-047,Gate 1a skeleton
br_exports,x,Exportacoes reais,TBD,TBD-verify-in-task-WBS-048,tbd,final_revised,quarterly,WBS-048,Gate 1a skeleton
br_imports,m,Importacoes reais,TBD,TBD-verify-in-task-WBS-049,tbd,final_revised,quarterly,WBS-049,Gate 1a skeleton
```

---

## 4. Additional planned MVP observables

These planned observables do not unblock Gate 1b while any core source remains `TBD`.

```csv
series_id,variable,description,source,source_id,source_status,revision_policy,frequency_model,wbs,gate_status
br_ipca_free,pi_f,Inflacao de precos livres,TBD,TBD-verify-in-task-WBS-050,tbd,final_revised,quarterly,WBS-050,Gate 1a skeleton
br_ipca_administered,pi_a,Inflacao de precos administrados,TBD,TBD-verify-in-task-WBS-051,tbd,final_revised,quarterly,WBS-051,Gate 1a skeleton
br_import_price_inflation,pi_m,Inflacao de importados,TBD,TBD-verify-in-task-WBS-051,tbd,final_revised,quarterly,WBS-051,Gate 1a skeleton
br_inflation_target,pi_target,Meta de inflacao,TBD,TBD-verify-in-task-WBS-051,tbd,final_revised,quarterly,WBS-051,Gate 1a skeleton
br_risk_premium,risk,Premio de risco domestico if needed for estimation,TBD,TBD-verify-in-task-WBS-051,tbd,final_revised,quarterly,WBS-051,Gate 1a skeleton
br_output_gap,y_gap,Hiato do produto measurement candidate,TBD,TBD-verify-in-task-WBS-051,tbd,final_revised,quarterly,WBS-051,Gate 1a skeleton
```

---

## 5. Transformation rules to finalize later

```text
- Inflation: compound monthly inflation or use index log-difference; never simple average of monthly inflation.
- Interest rates: quarterly average or effective quarterly rate, chosen by measurement equation.
- Exchange rate: quarterly average baseline; end-of-period only for robustness.
- Expectations: average or end-of-quarter rule must be defined before estimation.
- Real activity: seasonally adjusted real series when appropriate.
- `y_gap_t` is structural in the MVP; measurement equation is future Gate 1/2 work.
```

---

## 6. Gate 1a acceptance

Gate 1a is satisfied by this skeleton if:

```text
- required metadata fields are listed;
- every planned observable has a source_id field;
- unverified sources use TBD-verify-in-task-*;
- generic sources are not treated as verified;
- no data file is created;
- Gate 1b remains blocked until core source IDs are verified.
```

