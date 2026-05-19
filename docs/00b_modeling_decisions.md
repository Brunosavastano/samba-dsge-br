# Modeling Decisions - samba-dsge-br

**Documento:** `docs/00b_modeling_decisions.md`
**Status geral:** Gate 0 approved
**Fonte canonica:** `samba_dsge_br_spec_standalone_consolidado.md`
**Plano operacional:** `docs/08_implementation_plan.md`
**Criado por:** Codex
**Aprovado por:** Bruno
**Data de aprovacao:** 2026-05-19

---

## 0. Regra de governanca

Bruno autorizou a aprovacao do Gate 0 em 2026-05-19, limitada ao MVP, desde que as correcoes tecnicas objetivas fossem aplicadas neste documento.

```text
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
```

Esta aprovacao nao aprova `source_id`, dados, priors, Dynare/MATLAB/Octave, Redux ou extensao soberana.

---

## 1. Checklist Gate 0

| Decisao | ID | Status |
|---|---|---|
| Amostra, COVID e revisao de dados | SAMPLE-001 | approved |
| Tratamento de tendencia | TREND-001 | approved |
| Regra de politica monetaria | MON-001 | approved |
| Inflacao-meta | TARGET-001 | approved |
| UIP e premio de risco | EXT-001 | approved |
| Regra fiscal | FISC-001 | approved |
| Precos administrados | ADMIN-001 | approved |
| Observaveis iniciais | OBS-001 | approved |
| Variaveis estruturais minimas | STRUCT-001 | approved |
| Escopo do MVP | SCOPE-001 | approved |

Gate 0 esta aprovado para o MVP.

---

## 2. Decisoes aprovadas

### SAMPLE-001 - Amostra, COVID e revisao de dados

```yaml
decision_id: SAMPLE-001
decision_title: Amostra, COVID e politica de revisao de dados
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Incluir COVID no baseline linear-Gaussiano inicial."
  - "Usar real-time vintages no MVP academico."
  - "Misturar dados final-revised e real-time no mesmo experimento."
  - "Usar a amostra Redux 2001Q4-2019Q4 como baseline do SAMBA classico MVP."
rationale: >
  O MVP classico usa amostra pos-crise de 2002, sob regime de metas,
  sem choque pandemico e com dados final-revised.
downstream_files:
  - config/sample.yaml
  - docs/02_data_dictionary.md
  - docs/04_estimation_strategy.md
  - model/samba_classic/observables.inc
```

Decisao aprovada:

```yaml
sample:
  classic_mvp:
    start: "2003Q1"
    end: "2019Q4"
    frequency: "quarterly"
    covid_treatment: "excluded"
    data_revision: "final_revised"
  redux_replication:
    start: "2001Q4"
    end: "2019Q4"
    status: "deferred"
    scope: "out_of_mvp"
  future_operational:
    period: "current/future"
    data_revision: "real_time_vintage"
    scope: "out_of_mvp"
```

### TREND-001 - Tratamento de tendencia

```yaml
decision_id: TREND-001
decision_title: Tratamento de tendencia para SAMBA classico
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Usar HP filter bilateral na estimacao."
  - "Escolher transformacoes dos observaveis depois do .mod."
  - "Tratar produto potencial/hiato apenas como texto sem variavel ou medida."
rationale: >
  O MVP classico e log-linear em torno de steady state deterministico.
  Transformacoes por serie serao detalhadas depois no data dictionary e nas
  measurement equations.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - docs/03_calibration_notes.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/observables.inc
```

Decisao aprovada:

```text
SAMBA classico:
- modelo log-linear em torno de steady state deterministico;
- observaveis reais em crescimento ou log-desvio conforme equation registry/data dictionary;
- inflacao e juros em desvios de steady state/meta quando aplicavel;
- nenhum HP filter bilateral na estimacao;
- `y_gap` e variavel estrutural do MVP.
```

### MON-001 - Regra de politica monetaria

```yaml
decision_id: MON-001
decision_title: Regra de Taylor forward-looking com meta explicita
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Regra de Taylor ambigua entre inflacao corrente e esperada."
  - "Absorver mudancas de meta no choque monetario."
  - "Omitir `y_gap_t` da regra ou deixa-lo sem definicao operacional."
rationale: >
  A regra monetaria usa inflacao esperada, hiato estrutural e meta explicita.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Decisao aprovada:

```text
r_t = rho_r * r_{t-1}
      + (1 - rho_r) * [r_ss + phi_pi * (E_t pi_{t+1} - pi_target_t) + phi_y * y_gap_t]
      + eps_monetary_t
```

Requisitos aprovados:

```text
- `pi_target_t` entra explicitamente.
- `y_gap_t` e variavel estrutural do MVP.
- A measurement equation de `y_gap_t` sera definida depois no data dictionary/equation registry.
- A IRF de choque monetario deve exigir sinal, timing, magnitude e benchmark.
```

### TARGET-001 - Inflacao-meta

```yaml
decision_id: TARGET-001
decision_title: Tratamento de `pi_target_t` no MVP classico
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Omitir inflacao-meta do modelo classico."
  - "Tratar mudancas de meta como choque monetario puro."
  - "Implementar processo Redux de meta antes do MVP."
rationale: >
  `pi_target_t` precisa existir explicitamente para nao absorver meta no choque monetario.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/observables.inc
```

Decisao aprovada:

```text
- `pi_target_t` entra explicitamente.
- No MVP calibrado, `pi_target_t` entra como serie exogena/deterministica.
- `eps_pi_target` fica desligado no MVP calibrado.
- `eps_pi_target` so pode entrar em fase posterior com aprovacao propria.
- O processo persistente de meta do Redux fica fora do MVP.
```

### EXT-001 - UIP e premio de risco

```yaml
decision_id: EXT-001
decision_title: UIP com fechamento NFA/debt-elastic e premio de risco
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Deixar UIP como 'modificada' sem equacao."
  - "Usar premio de risco AR(1) puro como unica forma sem registrar alternativa."
  - "Adiar o fechamento externo para depois do .mod."
rationale: >
  A economia aberta exige fechamento explicito antes do Dynare. O baseline usa
  risk premium nfa/debt-elastic e processo AR(1) para `risk_t`.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Convencao e baseline aprovados:

```text
- Convencao de sinal: q_t ↑ = depreciacao real do BRL.
- `risk_t` segue AR(1).
- O fechamento externo baseline usa nfa/debt-elastic risk premium.
- A alternativa de premio AR(1) puro pode ser documentada no equation registry como alternativa, nao como ambiguidade do baseline.
```

Equacao aprovada:

```text
r_t - E_t pi_{t+1}
=
r_star_t - E_t pi_star_{t+1}
+ E_t Δq_{t+1}
+ psi_nfa * (nfa_t - nfa_ss)
+ risk_t

risk_t = rho_risk * risk_t(-1) + eps_risk_t
```

Variaveis necessarias:

```text
q
nfa
risk
r_star
pi_star
```

### FISC-001 - Regra fiscal

```yaml
decision_id: FISC-001
decision_title: Regra fiscal com `sp_target` e feedback sobre divida/PIB
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Usar bloco fiscal sem regra explicita."
  - "Tratar resultado primario realizado e meta fiscal como a mesma variavel."
  - "Incluir regimes fiscais 2016/2023 no MVP."
rationale: >
  A regra fiscal separa `sp_target` de `sp`, usa `b` como divida/PIB e mantem
  regimes fiscais fora do MVP.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
```

Decisao aprovada:

```text
sp_target_t =
rho_sp_target * sp_target_{t-1}
+ (1 - rho_sp_target) * [sp_ss + phi_b * (b_t - b_ss) + phi_y_sp * y_gap_t]
+ eps_sp_target_t

b_{t+1} = funcao de b_t, r_t, crescimento nominal do PIB e resultado primario.
```

Requisitos aprovados:

```text
- `sp_target` e separado de `sp` realizado.
- `b` representa divida publica/PIB.
- `phi_b > 0` e condicao de estabilizacao fiscal local.
- A identidade completa de divida entra no equation registry antes do `.mod`.
- Regimes fiscais 2016/2023 ficam fora do MVP.
```

### ADMIN-001 - Precos administrados

```yaml
decision_id: ADMIN-001
decision_title: Processo para inflacao de precos administrados
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Tratar precos administrados como choque generico sem processo proprio."
  - "Omitir pass-through cambial/importado do processo testavel."
  - "Resolver composicao de administrados apenas na estimacao."
rationale: >
  `pi_a` tem processo proprio, persistencia AR(1), relacao com meta, cambio e
  inflacao de importados quando disponivel, alem de choque proprio.
downstream_files:
  - docs/01_equation_registry.md
  - docs/02_data_dictionary.md
  - model/samba_classic/samba_classic.mod
  - model/samba_classic/shocks.inc
  - tests/test_irf_restrictions.py
```

Decisao aprovada:

```text
- `pi_a` tem processo proprio.
- O processo inclui AR(1).
- O processo inclui relacao com meta, cambio e inflacao de importados quando disponivel.
- O processo inclui choque proprio `eps_admin`.
- Administrados NAO sao apenas choque generico.
```

Equacao aprovada:

```text
pi_a_t =
rho_a * pi_a_{t-1}
+ (1 - rho_a) * [alpha_a_target * pi_target_t + alpha_a_fx * Δq_t + alpha_a_m * pi_m_t]
+ eps_admin_t
```

### OBS-001 - Observaveis iniciais

```yaml
decision_id: OBS-001
decision_title: Conjunto inicial de observaveis do MVP e primeira estimacao
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Comecar a baixar dados antes do data dictionary."
  - "Comecar a estimacao com o dataset total."
  - "Usar `source_id` por memoria interna sem verificacao."
rationale: >
  O MVP calibrado pode rodar sem `varobs`, mas o pipeline futuro deve gerar
  base minima. Fontes e measurement equations ficam para gates posteriores.
downstream_files:
  - docs/02_data_dictionary.md
  - docs/01_equation_registry.md
  - model/samba_classic/observables.inc
  - data/observables/
  - data/model_input/
```

Base minima futura do pipeline para MVP:

```text
1. crescimento do PIB real;
2. inflacao IPCA cheia;
3. Selic;
4. cambio real;
5. consumo privado;
6. investimento;
7. gasto do governo;
8. exportacoes;
9. importacoes;
10. inflacao de livres/administrados, se disponivel.
```

Regras aprovadas:

```text
- `y_gap_t` e variavel estrutural do MVP.
- A measurement equation de `y_gap_t` sera definida depois no data dictionary/equation registry.
- Nenhum `source_id` sera criado por memoria interna.
- Fonte nao verificada fica `TBD-verify-in-task-<WBS-ID>` ate Gate 1b.
- Antes de gerar dataset, PIB, IPCA, Selic, cambio, consumo, investimento, governo, exportacoes e importacoes devem estar sem TBD.
```

### STRUCT-001 - Variaveis estruturais minimas

```yaml
decision_id: STRUCT-001
decision_title: Variaveis estruturais minimas para o equation registry
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Permitir que variaveis estruturais sejam descobertas apenas durante a escrita do .mod."
  - "Omitir variaveis incorporadas pelo SPEC, como mc, q_k, wn, lambda, y_gap, y_pot, nfa, m_int e pi_target."
rationale: >
  O SPEC consolidado incorporou variaveis estruturais ausentes como correcao tecnica.
  O equation registry deve carrega-las explicitamente antes de qualquer implementacao Dynare.
downstream_files:
  - docs/01_equation_registry.md
  - docs/03_calibration_notes.md
  - model/samba_classic/samba_classic.mod
```

Variaveis estruturais minimas aprovadas:

```text
mc
q_k
wn
lambda
y_gap
y_pot
nfa
m_int
pi_target
sp_target
risk
```

### SCOPE-001 - Escopo do MVP e exclusoes explicitas

```yaml
decision_id: SCOPE-001
decision_title: Escopo do MVP e exclusoes explicitas
decision_status: approved
proposed_by: Codex
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Incluir Redux no MVP."
  - "Incluir extensao soberana no MVP."
  - "Iniciar estimacao Bayesiana completa no MVP."
rationale: >
  O MVP deve permanecer pequeno, auditavel e limitado ao SAMBA classico calibrado.
downstream_files:
  - docs/08_implementation_plan.md
  - docs/01_equation_registry.md
  - model/samba_classic/samba_classic.mod
```

Escopo aprovado:

```text
- Redux esta fora do MVP.
- Extensao soberana esta fora do MVP.
- Estimacao Bayesiana completa esta fora do MVP.
- O MVP e SAMBA classico calibrado, log-linear, primeira ordem.
```

---

## 3. Implicacoes para os proximos gates

Gate 0 aprovado desbloqueia apenas os proximos artefatos permitidos pelo plano:

```text
- configs iniciais;
- runtime verification;
- skeletons e contratos de fases posteriores, conforme gate aplicavel.
```

Continuam proibidos ate seus gates proprios:

```text
- inventar source IDs;
- gerar dados;
- criar pipeline;
- criar equation registry final;
- criar data dictionary final;
- criar .mod;
- iniciar estimacao;
- iniciar Redux;
- iniciar extensao soberana.
```

---

## 4. Status final deste documento

```yaml
gate: Gate 0
gate_status: approved
approved_by: Bruno
approval_date: 2026-05-19
approval_basis: "Approved by Bruno via objective technical corrections specified in prompt."
approved_decision_ids:
  - SAMPLE-001
  - TREND-001
  - MON-001
  - TARGET-001
  - EXT-001
  - FISC-001
  - ADMIN-001
  - OBS-001
  - STRUCT-001
  - SCOPE-001
limitations:
  - "Approval limited to MVP."
  - "Does not approve source IDs, data, priors, Dynare, Redux or sovereign extension."
```
