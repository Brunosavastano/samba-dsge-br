# Modeling Decisions — samba-dsge-br

**Documento:** `docs/00b_modeling_decisions.md`  
**Status geral:** proposed-only; aguardando aprovação humana para Gate 0  
**Fonte canônica:** `samba_dsge_br_spec_standalone_consolidado.md`  
**Plano operacional:** `docs/08_implementation_plan.md`  
**Criado por:** Codex  
**Data:** 2026-05-16

---

## 0. Regra de governança

Este documento contém propostas para o Gate 0. Codex não aprova decisões macroeconométricas.

Regra operacional:

```text
Codex pode criar ou revisar decisões com decision_status: proposed.
Codex não pode preencher approved_by nem approval_date.
Gate 0 só passa quando um revisor humano alterar explicitamente as decisões bloqueantes para approved.
```

Campos obrigatórios por decisão:

```yaml
decision_id:
decision_title:
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
rationale:
downstream_files:
```

---

## 1. Checklist Gate 0

| Decisão | ID | Status |
|---|---|---|
| Amostra, COVID e revisão de dados | SAMPLE-001 | proposed |
| Tratamento de tendência | TREND-001 | proposed |
| Regra de política monetária | MON-001 | proposed |
| Inflação-meta | TARGET-001 | proposed |
| UIP e prêmio de risco | EXT-001 | proposed |
| Regra fiscal | FISC-001 | proposed |
| Preços administrados | ADMIN-001 | proposed |
| Observáveis iniciais | OBS-001 | proposed |

Gate 0 ainda não está aprovado.

---

## 2. Decisões propostas

### SAMPLE-001 — Amostra, COVID e revisão de dados

```yaml
decision_id: SAMPLE-001
decision_title: Amostra, COVID e política de revisão de dados
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Incluir COVID no baseline linear-Gaussiano inicial."
  - "Usar real-time vintages no MVP acadêmico."
  - "Misturar dados final-revised e real-time no mesmo experimento."
  - "Usar a amostra Redux 2001Q4-2019Q4 como baseline do SAMBA clássico MVP."
rationale: >
  O SPEC consolidado define o MVP clássico como amostra pós-crise de 2002,
  sob regime de metas e sem choque pandêmico. O baseline acadêmico deve usar
  dados final-revised para reduzir complexidade operacional e evitar contaminar
  o filtro/estimação inicial com real-time vintages ou COVID.
downstream_files:
  - config/sample.yaml
  - docs/02_data_dictionary.md
  - docs/04_estimation_strategy.md
  - model/samba_classic/observables.inc
```

Proposta:

```yaml
sample:
  classic_mvp:
    start: "2003Q1"
    end: "2019Q4"
    covid_treatment: "exclude"
    data_revision: "final_revised"
    rationale: "Amostra pós-crise de 2002, sob regime de metas, sem choque pandêmico."
  redux_replication:
    start: "2001Q4"
    end: "2019Q4"
    kalman_initialization_observations: 8
    covid_treatment: "exclude"
    data_revision: "final_revised"
    status: "out_of_mvp"
  future_operational:
    start: "2003Q1"
    end: "current"
    covid_treatment: "to_be_defined"
    data_revision: "real_time_vintage"
    status: "out_of_mvp"
```

Critério para aprovação humana:

- Confirmar que `classic_mvp` deve ser 2003Q1-2019Q4.
- Confirmar que COVID fica excluído do baseline.
- Confirmar que real-time vintages ficam fora do MVP.
- Confirmar que Redux não altera a amostra do MVP clássico.

### TREND-001 — Tratamento de tendência

```yaml
decision_id: TREND-001
decision_title: Tratamento de tendência para SAMBA clássico
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Usar HP filter bilateral na estimação."
  - "Escolher transformações dos observáveis depois do .mod."
  - "Tratar produto potencial/hiato apenas como texto sem variável ou medida."
rationale: >
  O SPEC propõe SAMBA clássico log-linear em torno de steady state determinístico.
  A transformação dos observáveis precisa ser compatível com as equações de medida
  e não pode introduzir look-ahead bias via filtro bilateral.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - docs/03_calibration_notes.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/observables.inc
```

Proposta:

```text
SAMBA clássico:
- modelo log-linear em torno de steady state determinístico;
- observáveis reais em crescimento ou log-desvio conforme equação de medida;
- inflação e juros em desvios de steady state/meta quando aplicável;
- nenhum HP filter bilateral na estimação;
- `y_gap` deve ser variável/model measure explícita, não rótulo informal.
```

Critério para aprovação humana:

- Confirmar que o MVP clássico permanece log-linear e de primeira ordem.
- Confirmar política de transformação antes do data dictionary final.
- Confirmar que HP bilateral está proibido na estimação.

### MON-001 — Regra de política monetária

```yaml
decision_id: MON-001
decision_title: Regra de Taylor forward-looking com meta explícita
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Regra de Taylor ambígua entre inflação corrente e esperada."
  - "Absorver mudanças de meta no choque monetário."
  - "Omitir `y_gap_t` da regra ou deixá-lo sem definição operacional."
rationale: >
  A regra monetária precisa estar definida antes do equation registry e do .mod.
  A formulação forward-looking com meta explícita reduz ambiguidade entre inflação
  corrente, esperada e desvios em relação à meta.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Proposta:

```text
r_t = rho_r * r_{t-1}
      + (1 - rho_r) * [r_ss + phi_pi * (E_t pi_{t+1} - pi_target_t) + phi_y * y_gap_t]
      + eps_monetary_t
```

Requisitos associados:

- `pi_target_t` entra explicitamente.
- `y_gap_t` deve existir como variável ou proxy observável documentada.
- A IRF de choque monetário deve exigir sinal, timing, magnitude e benchmark.

Critério para aprovação humana:

- Confirmar uso de inflação esperada.
- Confirmar definição operacional de `y_gap_t`.
- Confirmar que o choque monetário não absorve meta de inflação.

### TARGET-001 — Inflação-meta

```yaml
decision_id: TARGET-001
decision_title: Tratamento de `pi_target_t` no MVP clássico
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Omitir inflação-meta do modelo clássico."
  - "Tratar mudanças de meta como choque monetário puro."
  - "Implementar processo Redux de meta antes do MVP."
rationale: >
  O SPEC exige `pi_target_t` e `eps_pi_target` como objetos explícitos.
  Para o MVP clássico, a meta pode entrar de forma exógena/determinística, enquanto
  choques persistentes de meta ficam opcionais ou adiados.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/observables.inc
```

Proposta:

```text
Fase clássica:
- `pi_target_t` entra como série exógena ou deterministic exogenous variable;
- `eps_pi_target` permanece opcional e desligável no MVP calibrado se necessário;
- a decisão final entre série exógena e `varexo_det` deve ser confirmada antes do `.mod`.

Fase Redux:
- processo persistente de meta de inflação fica fora do MVP.
```

Critério para aprovação humana:

- Escolher `pi_target_t` como série exógena ou `varexo_det` antes da Fase 3.
- Confirmar se `eps_pi_target` fica desligado no MVP calibrado.

### EXT-001 — UIP e prêmio de risco

```yaml
decision_id: EXT-001
decision_title: UIP com fechamento NFA/debt-elastic e prêmio de risco
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Deixar UIP como 'modificada' sem equação."
  - "Usar prêmio de risco AR(1) puro como única forma sem registrar alternativa."
  - "Adiar o fechamento externo para depois do .mod."
rationale: >
  A economia aberta exige fechamento explícito antes do Dynare. O SPEC define
  como baseline provisório a UIP com termo elástico em NFA/dívida e processo AR(1)
  para risco, mantendo alternativa documentada para prêmio AR(1) puro se a réplica
  clássica exigir.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Proposta:

```text
r_t - E_t pi_{t+1}
=
r_star_t - E_t pi_star_{t+1}
+ E_t Δq_{t+1}
+ psi_nfa * (nfa_t - nfa_ss)
+ risk_t

risk_t = rho_risk * risk_{t-1} + eps_risk_t
```

Variáveis necessárias:

```text
q
nfa
risk
r_star
pi_star
```

Critério para aprovação humana:

- Confirmar baseline NFA/debt-elastic para MVP.
- Confirmar que alternativa de prêmio AR(1) puro será registrada no equation registry.
- Confirmar qual proxy/fonte futura será considerada para prêmio de risco na estimação, sem ainda pinar `source_id`.

### FISC-001 — Regra fiscal

```yaml
decision_id: FISC-001
decision_title: Regra fiscal com `sp_target` e feedback sobre dívida/PIB
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Usar bloco fiscal sem regra explícita."
  - "Tratar resultado primário realizado e meta fiscal como a mesma variável."
  - "Incluir regimes fiscais 2016/2023 no MVP."
rationale: >
  A regra fiscal evita bloco fiscal subidentificado. O SPEC propõe separar `sp_target`
  de `sp` realizado, usar `b` como dívida/PIB e manter regimes fiscais posteriores
  fora do MVP.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
```

Proposta:

```text
sp_target_t =
rho_sp_target * sp_target_{t-1}
+ (1 - rho_sp_target) * [sp_ss + phi_b * (b_t - b_ss) + phi_y_sp * y_gap_t]
+ eps_sp_target_t

b_{t+1} = função de b_t, r_t, crescimento nominal do PIB e resultado primário.
```

Decisões associadas:

- `sp_target` é separado de `sp` realizado.
- `b` representa dívida pública/PIB.
- `phi_b > 0` é condição de estabilização fiscal local.
- Regimes fiscais 2016/2023 ficam fora do MVP.

Critério para aprovação humana:

- Confirmar separação `sp_target` vs `sp`.
- Confirmar regra de feedback em dívida/PIB.
- Confirmar exclusão de regimes fiscais do MVP.

### ADMIN-001 — Preços administrados

```yaml
decision_id: ADMIN-001
decision_title: Processo para inflação de preços administrados
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Tratar preços administrados como choque genérico sem processo próprio."
  - "Omitir pass-through cambial/importado do processo testável."
  - "Resolver composição de administrados apenas na estimação."
rationale: >
  O SPEC exige que `pi_a` seja processo testável, com persistência e relação com
  meta, câmbio e/ou preços importados. Isso evita empurrar má especificação para
  erros de mensuração ou choques genéricos.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Proposta:

```text
pi_a_t =
rho_a * pi_a_{t-1}
+ (1 - rho_a) * [alpha_a_target * pi_target_t + alpha_a_fx * Δq_t + alpha_a_m * pi_m_t]
+ eps_admin_t
```

Critério para aprovação humana:

- Confirmar que `pi_a` entra como processo próprio.
- Confirmar quais canais entram no MVP: meta, câmbio e/ou preço de importados.
- Confirmar que composição e quebras da série serão documentadas no data dictionary.

### OBS-001 — Observáveis iniciais

```yaml
decision_id: OBS-001
decision_title: Conjunto inicial de observáveis do MVP e primeira estimação
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
  - "Começar a baixar dados antes do data dictionary."
  - "Começar a estimação com o dataset total."
  - "Usar `source_id` por memória interna sem verificação."
rationale: >
  O SPEC permite que o MVP calibrado rode sem `varobs`, mas exige que o pipeline
  produza base mínima. A primeira estimação deve começar com subconjunto menor
  do que o dataset total e só após Gate 1b, Gate 2b, modelo calibrado, likelihood
  finito e identificação local.
downstream_files:
  - docs/02_data_dictionary.md
  - docs/01_equation_registry.md
  - model/samba_classic/observables.inc
  - data/observables/
  - data/model_input/
```

Base mínima que o pipeline deve gerar para MVP:

```text
1. crescimento do PIB real;
2. inflação IPCA cheia;
3. Selic;
4. câmbio real;
5. consumo privado;
6. investimento;
7. gasto do governo;
8. exportações;
9. importações;
10. inflação de livres/administrados, se disponível.
```

Primeira estimação Bayesiana deve começar com subconjunto menor:

```text
1. crescimento do PIB real;
2. inflação cheia;
3. inflação de livres;
4. Selic;
5. câmbio real;
6. consumo privado;
7. investimento;
8. exportações;
9. importações;
10. prêmio de risco, se a equação UIP exigir.
```

Política de fonte:

```text
Nenhum `source_id` será criado por memória interna.
Fonte não verificada fica `TBD-verify-in-task-<WBS-ID>` até Gate 1b.
Antes de gerar dataset, PIB, IPCA, Selic, câmbio, consumo, investimento, governo, exportações e importações devem estar sem TBD.
```

Critério para aprovação humana:

- Confirmar lista mínima do MVP.
- Confirmar subconjunto inicial de estimação.
- Confirmar que Gate 1b bloqueia extração e transformação real de dados.

---

## 3. Implicações para os próximos gates

Enquanto todas as decisões bloqueantes estiverem em `decision_status: proposed`:

```text
- Não criar config/sample.yaml.
- Não criar dataset.
- Não criar equation registry core final.
- Não criar .mod.
- Não iniciar estimação.
```

Próxima ação humana:

```text
Revisar cada decisão, ajustar texto se necessário e preencher `decision_status: approved`, `approved_by` e `approval_date` apenas quando houver concordância explícita.
```

---

## 4. Status final deste documento

```yaml
gate: Gate 0
gate_status: not_passed
reason: "Todas as decisões estão em proposed e aguardam aprovação humana."
created_by: Codex
approved_by:
approval_date:
```

