# Implementation Plan — samba-dsge-br

**Documento:** `docs/08_implementation_plan.md`  
**Versão:** v2.0-consolidated  
**Data:** 2026-05-16  
**Fonte canônica:** `samba_dsge_br_spec_standalone_consolidado.md`  
**Status:** plano-mestre revisado após parecer técnico adversarial.

---

## 0. Resumo das incorporações desta revisão

Este plano consolida o SPEC standalone, o primeiro `08_implementation_plan` e o parecer técnico adversarial recebido. A revisão foi útil principalmente por identificar que o plano anterior estava tecnicamente coerente, mas ainda frágil em **governança operacional**: o Codex poderia propor decisões macro, aprová-las implicitamente, criar pipeline com fontes em `TBD` e começar a alterar o repo sem versionamento.

### 0.1 Incorporado integralmente

| Item | Decisão incorporada | Racional |
|---|---|---|
| Aprovação humana no Gate 0 | `docs/00b_modeling_decisions.md` agora usa `decision_status: proposed / approved / rejected / deferred`, `approved_by`, `approval_date`, `alternatives_rejected`, `rationale` | Codex pode propor decisões macro, mas não pode aprová-las. |
| `WBS-000 — Initialize git repository` | Primeira tarefa real no repositório | Projeto auditável precisa de Git antes de qualquer mudança substantiva. |
| Gate 1 dividido em 1a/1b | `Gate 1a = skeleton`; `Gate 1b = core source IDs verified` | `TBD` é aceitável no skeleton, não para gerar dataset. |
| Validar SPEC consolidado antes da Thread 01 | Preflight obrigatório | Evita herdar divergência silenciosa entre SPEC v3 e matriz incorporada. |
| Schema mínimo de `models/registry.json` | Campos mínimos definidos neste plano | Registry não pode ser improvisado pelo Codex. |
| Verificação de runtime Dynare/MATLAB/Octave | `WBS-009.5` | Incompatibilidade não deve aparecer só na Fase 3. |
| Literature map antes do equation registry | `docs/00a_literature_map.md` | Evita registry baseado em memória. |
| `docs/06_model_validation.md` como template | Front matter obrigatório | Evita parecer que validação ocorreu antes do modelo. |
| Reforço contra alucinação de `source_id` | Fontes só com repo/contexto/documentação oficial acessível | Não usar memória interna para cravar SGS/SIDRA. |
| Estimation smoke test | `WBS-071a` antes de MH piloto | Fail-fast para likelihood, dados, priors e filtro. |
| Agrupamento de WBS em PRs | Seção própria | Facilita execução real por threads/branches. |

### 0.2 Incorporado parcialmente

| Item | Decisão |
|---|---|
| Renomear `models/` para `registry/` | Não renomear. O SPEC usa `models/registry.json`. O plano agora exige documentar claramente: `models/ = metadata registry`; `model/ = Dynare/MATLAB files`. |
| `pyproject.toml` vs `requirements.txt` | `pyproject.toml` será fonte de verdade para o pacote/testes; `requirements.txt` é compatibilidade de ambiente, derivado ou mantido de forma coerente. |
| Gate 1a bloqueando equation registry | Parcial. Gate 1a permite registry estrutural; measurement equations finais só avançam após Gate 1b. |
| Fixar versão de Dynare já no plano | Não. O plano exige verificar runtime local antes de fixar versão. |

### 0.3 Não incorporado

| Sugestão | Motivo |
|---|---|
| Permitir que Codex aprove decisões macro | Rejeitado. Codex propõe; humano aprova. |
| Renomear `models/` contrariando o SPEC | Rejeitado para preservar fonte canônica. |
| Cravar `source_id` via memória paramétrica | Rejeitado. Fonte não verificada permanece `TBD-verify-in-task-<WBS-ID>`. |
| Gerar dados antes do Gate 1b | Rejeitado. Extração/transformação só após core sources pinados. |

---

## 1. Diagnóstico do estado atual do repositório

Repositório alvo planejado:

```text
C:\Users\bruno\Desktop\Codex\SAMBA
```

Estado esperado neste momento: **bootstrap**.

O diagnóstico anterior indicou:

| Item | Status observado | Consequência |
|---|---|---|
| `.git/` | Ausente | Agora vira bloqueio operacional via `WBS-000`. |
| `samba_dsge_br_spec_standalone_consolidado.md` | Presente | Fonte canônica superior. |
| `docs/08_implementation_plan.md` | Presente após primeira entrega | Será substituído por esta versão consolidada. |
| `docs/00b_modeling_decisions.md` | Ausente | Bloqueia `.mod`, dados finais e estimação. |
| `docs/01_equation_registry.md` | Ausente | Bloqueia Dynare disciplinado. |
| `docs/02_data_dictionary.md` | Ausente | Bloqueia pipeline de dados real. |
| `config/sample.yaml` | Ausente | Bloqueia amostra reproduzível. |
| `config/environment.yaml` | Ausente | Bloqueia runtime/seeds reproduzíveis. |
| `models/registry.json` | Ausente | Bloqueia versionamento de modelos. |
| `README.md` / `Makefile` / Python setup | Ausentes | Bloqueiam execução padronizada. |

### 1.1 Fonte canônica

Usar como fonte superior:

```text
samba_dsge_br_spec_standalone_consolidado.md
```

A ordem de precedência do projeto passa a ser:

```text
1. samba_dsge_br_spec_standalone_consolidado.md
2. docs/00b_modeling_decisions.md, depois de aprovado por humano
3. docs/00a_literature_map.md
4. docs/01_equation_registry.md
5. docs/02_data_dictionary.md
6. models/registry.json
7. arquivos model/samba_classic/*.mod, *.m, *.inc
8. outputs e relatórios
```

### 1.2 Primeira ação não-negociável

Antes de qualquer thread com conteúdo macro ou código:

```text
WBS-PRE-000 — Validar SPEC consolidado contra as decisões incorporadas.
WBS-000     — Inicializar Git e criar baseline commit.
```

---

## 2. Princípios de implementação

1. O projeto não começa com Dynare; começa com decisões macroeconométricas documentadas e aprovadas.
2. Codex pode propor decisões macro, mas não pode aprová-las.
3. Nenhum `.mod` antes de Gate 0 aprovado por humano, Gate 1b e Gate 2.
4. Nenhuma estimação Bayesiana antes de steady state, BK, IRFs calibradas, likelihood finito e identificação local.
5. Nenhum dataset real antes de `Gate 1b — Core source IDs verified`.
6. `source_id` nunca é inventado; se não confirmado, usar `TBD-verify-in-task-<WBS-ID>`.
7. Dados final-revised e real-time não podem ser misturados no mesmo experimento.
8. HP filter bilateral não será usado na estimação.
9. Measurement errors precisam de justificativa, limite e teste.
10. O MVP cobre SAMBA clássico calibrado, log-linear, primeira ordem, sem Redux e sem extensão soberana.
11. Redux entra apenas depois de MVP validado e decisão própria sobre amostra 2001Q4–2019Q4/2002.
12. Extensão soberana entra apenas depois de `docs/07_sovereign_extension_spec.md`.
13. IRFs devem ser avaliadas por sinal, timing, magnitude e benchmark documentado.
14. `models/` é metadata registry; `model/` contém arquivos Dynare/MATLAB.
15. `pyproject.toml` é a fonte de verdade do ambiente Python; `requirements.txt` é compatibilidade derivada ou espelhada.
16. Uma thread Codex deve corresponder a uma branch e a um PR lógico.

---

## 3. Arquitetura-alvo do repositório

```text
samba-dsge-br/
├── .git/
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt
├── Makefile
├── .gitignore
├── config/
│   ├── sample.yaml
│   ├── environment.yaml
│   ├── classic_mvp.yaml
│   ├── classic_estimation.yaml
│   ├── redux_smc.yaml
│   └── sovereign_scenarios.yaml
├── models/
│   └── registry.json
├── docs/
│   ├── 00a_literature_map.md
│   ├── 00b_modeling_decisions.md
│   ├── 01_equation_registry.md
│   ├── 02_data_dictionary.md
│   ├── 03_calibration_notes.md
│   ├── 04_estimation_strategy.md
│   ├── 05_replication_targets.md
│   ├── 06_model_validation.md
│   ├── 07_sovereign_extension_spec.md
│   └── 08_implementation_plan.md
├── data/
│   ├── raw/
│   ├── interim/
│   ├── clean/
│   ├── observables/
│   ├── model_input/
│   └── vintages/
├── src/
│   ├── data_pipeline/
│   ├── diagnostics/
│   ├── plotting/
│   ├── orchestration/
│   └── utils/
├── model/
│   ├── samba_classic/
│   ├── samba_redux/
│   └── sovereign_extension/
├── outputs/
│   ├── schema/
│   ├── irfs/
│   ├── identification/
│   ├── posterior/
│   ├── moments/
│   ├── variance_decomposition/
│   ├── historical_decomposition/
│   ├── forecasts/
│   ├── backtesting/
│   └── reports/
└── tests/
    ├── test_project_structure.py
    ├── test_config.py
    ├── test_registry.py
    ├── test_equation_registry.py
    ├── test_data_transformations.py
    ├── test_observables.py
    ├── test_calibration.py
    ├── test_model_outputs.py
    ├── test_irf_restrictions.py
    ├── test_econometric.py
    └── test_backtesting.py
```

### 3.1 Convenção `models/` vs `model/`

```text
models/ = metadata registry, versionamento e mapeamento entre modelo, dados, priors e outputs.
model/  = arquivos executáveis do modelo: Dynare, MATLAB/Octave, includes e rotinas auxiliares.
```

Esta distinção deve constar no `README.md`.

### 3.2 Fonte de verdade Python

```text
pyproject.toml    = fonte de verdade para package, pytest, tooling e dependências diretas.
requirements.txt = compatibilidade de ambiente, derivado ou mantido coerentemente com pyproject.
```

O README deve documentar a política escolhida.

### 3.3 Schema mínimo de `models/registry.json`

```json
{
  "model_id": "samba_classic_mvp_v0",
  "spec_version": "v3.0-consolidated",
  "plan_version": "v2.0-consolidated",
  "status": "planned",
  "description": "SAMBA classic calibrated MVP",
  "dynare_file": "model/samba_classic/samba_classic.mod",
  "steady_state_file": "model/samba_classic/steady_state.m",
  "calibration_file": "model/samba_classic/calibration.m",
  "observables_file": "model/samba_classic/observables.inc",
  "shocks_file": "model/samba_classic/shocks.inc",
  "priors_file": null,
  "data_config": "config/classic_mvp.yaml",
  "sample_config": "config/sample.yaml",
  "environment_config": "config/environment.yaml",
  "equation_registry": "docs/01_equation_registry.md",
  "data_dictionary": "docs/02_data_dictionary.md",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD",
  "notes": "Registry metadata only; executable model files live under model/."
}
```

---

## 4. Gates técnicos obrigatórios

| Gate | Nome | Objetivo | Inputs | Outputs | Critérios de aceite | Bloqueia |
|---|---|---|---|---|---|---|
| Preflight | SPEC consolidated verified | Confirmar que o SPEC standalone preserva decisões incorporadas | SPEC v3, matriz se disponível | Nota de validação | Sem divergência material ou divergência documentada | Thread 01 |
| Gate 0 | Modeling decisions human-approved | Fechar decisões macro com aprovação humana | SPEC, literature map preliminar | `docs/00b_modeling_decisions.md`, `config/sample.yaml` | Todas as decisões bloqueantes com `decision_status: approved`, `approved_by`, `approval_date` | Gates 1/2, `.mod`, dados |
| Gate 1a | Data dictionary skeleton | Criar estrutura e política de dados | Gate 0 proposto/aprovado | `docs/02_data_dictionary.md` skeleton | Colunas mínimas e `TBD-verify-in-task-*` válidos | Measurement equations finais |
| Gate 1b | Core source IDs verified | Pinar fontes core antes de dados reais | Gate 1a | Dictionary com fontes core pinadas | Sem TBD em PIB, IPCA, Selic, câmbio, consumo, investimento, governo, exportações, importações | Extração, transformação, dataset |
| Gate 2a | Literature map complete | Ancorar registry em fontes | SPEC, papers, docs | `docs/00a_literature_map.md` | Papers/seções/equações/tabelas mapeados | Equation registry core |
| Gate 2b | Equation registry minimum viable | Registrar núcleo estrutural | Gate 0, Gate 2a | `docs/01_equation_registry.md` | Blocos core, variáveis, choques, parâmetros, testes e status versionados | Dynare |
| Gate 3 | Calibrated Dynare model solves | Validar modelo calibrado | Gates 1b/2b | `.mod`, steady state, IRFs | Dynare roda; residuals baixos; BK passa; IRFs com sinal/timing/magnitude | Identificação |
| Gate 4 | Local identification passes | Evitar MH em parâmetros fracos | Gate 3 | Reports de identificação | Fracos tratados por fixação, prior, restrição ou reparametrização | Estimação |
| Gate 5a | Estimation smoke test passes | Fail-fast de likelihood/filtro/priors | Gate 4 | Smoke outputs | Likelihood finito e pipeline estimável em run mínimo | MH piloto |
| Gate 5b | Bayesian pilot passes | Validar MH piloto | Gate 5a | Pilot chains | Aceitação, modo e R-hat preliminar aceitáveis | MH completo |
| Gate 6 | Validation/backtesting complete | Aceitar modelo estimado | Gate 5b/MH completo | Reports de validação | Momentos, IRFs, decomposições e pseudo-OOS documentados | Redux/soberano |

### 4.1 Regra de aprovação humana no Gate 0

Cada decisão em `docs/00b_modeling_decisions.md` deve seguir o template:

```yaml
decision_id: MON-001
decision_title: Monetary policy rule
decision_status: proposed  # proposed | approved | rejected | deferred
proposed_by: Codex
approved_by:
approval_date:
alternatives_rejected:
rationale:
downstream_files:
  - docs/01_equation_registry.md
  - model/samba_classic/samba_classic.mod
```

Regra dura:

```text
Codex só pode produzir `decision_status: proposed`.
Avanço para Gate 1b, Gate 2b e qualquer `.mod` exige `decision_status: approved` com revisor humano explícito.
```

### 4.2 Regra de Gate 1a/1b

```text
Gate 1a permite placeholders.
Gate 1b não permite placeholders nas fontes core.
```

Core sources que devem estar sem `TBD` antes de qualquer dataset:

```text
PIB real
IPCA cheio
Selic
câmbio nominal/real conforme decisão
consumo privado
investimento
gasto do governo
exportações
importações
```

---

## 5. Roadmap por fases

### Phase PRE — Preflight

Objetivo: validar o SPEC consolidado e registrar divergências antes de qualquer execução.

Entregáveis:

```text
docs/spec_validation_note.md ou seção no README
```

Critério de aceite:

```text
Amostra, COVID, UIP, pi_target, regra fiscal, administrados e variáveis novas preservadas.
```

### Phase 0 — Repository bootstrap and governance

Objetivo: criar Git, baseline commit e governança mínima.

Tarefas:

```text
- Inicializar Git.
- Criar `.gitignore` mínimo.
- Criar README/CONTRIBUTING com política branch/PR.
- Criar baseline commit com SPEC standalone e docs/08.
- Documentar "one thread = one branch + PR".
```

### Phase -1 — Macroeconometric decisions

Objetivo: criar propostas de decisões macro em `docs/00b_modeling_decisions.md`.

Importante:

```text
Todas as decisões saem como `proposed`.
Humano aprova antes dos próximos gates.
```

### Phase 1a — Data dictionary skeleton and contracts

Objetivo: criar o skeleton do data dictionary, políticas de fonte e contratos de validação, sem baixar dados.

### Phase 2a — Literature map

Objetivo: criar `docs/00a_literature_map.md` para ancorar o registry.

### Phase 2b — Equation registry

Objetivo: registrar equações estruturais do SAMBA clássico antes do `.mod`.

Measurement equations finais ficam draft até Gate 1b.

### Phase 1b — Core source verification and data pipeline

Objetivo: pinar fontes core e só então extrair/transformar dados.

### Phase 3 — Calibrated SAMBA classic

Objetivo: implementar modelo clássico calibrado, log-linear, primeira ordem.

### Phase 3.5 — Local identification

Objetivo: rodar identificação local antes de qualquer MH.

### Phase 4 — Bayesian estimation

Objetivo: smoke test, MH piloto e MH completo, nessa ordem.

### Phase 5 — Validation and backtesting

Objetivo: validar o modelo contra momentos, IRFs, decomposições e pseudo-OOS.

### Phase 6 — SAMBA Redux

Fora do MVP. Exige Gate 6 e decisão própria sobre amostra e tratamento de 2002.

### Phase 7 — Sovereign extension

Fora do MVP. Exige `docs/07_sovereign_extension_spec.md`.

---

## 6. Work Breakdown Structure detalhada

| ID | Fase | Tarefa | Descrição | Inputs | Outputs | Arquivos | Dependências | Critério de aceite | Paralelizável? |
|---|---|---|---|---|---|---|---|---|---|
| WBS-PRE-000 | PRE | Validar SPEC consolidado | Comparar SPEC v3 com decisões incorporadas | SPEC v3, matriz se disponível | Nota de validação | `docs/spec_validation_note.md` ou README | Nenhuma | Divergências materiais documentadas | Não |
| WBS-000 | 0 | Initialize git repository | Criar Git e baseline commit | SPEC, plano | Repo versionado | `.git/`, `.gitignore`, README/CONTRIBUTING | WBS-PRE-000 | Initial commit com SPEC e docs/08 | Não |
| WBS-001 | -1 | Criar modeling decisions template | Template com status, aprovação e alternativas | SPEC | Template proposto | `docs/00b_modeling_decisions.md` | WBS-000 | Campos de aprovação presentes | Não |
| WBS-002 | -1 | Propor amostra MVP | 2003Q1–2019Q4, COVID excluído, final-revised | SPEC | Decisão AMOSTRA proposed | `docs/00b_modeling_decisions.md` | WBS-001 | Status `proposed`; sem aprovação automática | Não |
| WBS-003 | -1 | Propor tratamento de tendência | Log-linear, SS determinístico, sem HP bilateral | SPEC | Decisão TREND proposed | `docs/00b_modeling_decisions.md` | WBS-001 | Unidade e transformação especificadas | Não |
| WBS-004 | -1 | Propor Taylor e meta | Regra forward-looking e `pi_target_t` | SPEC | Decisão MON proposed | `docs/00b_modeling_decisions.md` | WBS-001 | Meta e inflação esperada explícitas | Não |
| WBS-005 | -1 | Propor UIP e risco | Baseline NFA/debt-elastic e alternativa | SPEC | Decisão EXT proposed | `docs/00b_modeling_decisions.md` | WBS-001 | UIP testável documentada | Não |
| WBS-006 | -1 | Propor regra fiscal | `sp_target`, dívida/PIB e feedback | SPEC | Decisão FISC proposed | `docs/00b_modeling_decisions.md` | WBS-001 | Regra estabilizadora explícita | Não |
| WBS-007 | -1 | Propor administrados | AR(1), pass-through, meta | SPEC | Decisão ADMIN proposed | `docs/00b_modeling_decisions.md` | WBS-001 | Processo testável | Não |
| WBS-007H | -1 | Aprovação humana Gate 0 | Revisar decisões propostas | WBS-002..007 | Decisões approved/rejected/deferred | `docs/00b_modeling_decisions.md` | WBS-002..007 | Todas bloqueantes approved | Não |
| WBS-008 | -1 | Criar `config/sample.yaml` | Codificar amostras aprovadas | Gate 0 | YAML sample | `config/sample.yaml` | WBS-007H | Sem mistura real-time/final-revised | Sim |
| WBS-009 | -1 | Criar `config/environment.yaml` | Seeds, versões `to_pin`, runtime | SPEC | YAML ambiente | `config/environment.yaml` | WBS-000 | Sem versão inventada | Sim |
| WBS-009.5 | 0 | Verify Dynare/MATLAB/Octave runtime | Detectar runtime local e limitações | Ambiente local | Runtime note | `docs/runtime_verification.md`, `config/environment.yaml` | WBS-009 | Versões detectadas ou limitação documentada | Sim |
| WBS-010 | 0 | README inicial | Explicar gates, diretórios e modelos | Plano | README | `README.md` | WBS-000 | Inclui `models/` vs `model/` | Sim |
| WBS-011 | 0 | `.gitignore` mínimo | Ignorar caches e outputs pesados | Stack | `.gitignore` | `.gitignore` | WBS-000 | Não ignora docs/config essenciais | Sim |
| WBS-012 | 0 | `pyproject.toml` | Configurar package/testes | Stack Python | Python config | `pyproject.toml` | WBS-009 | Fonte de verdade declarada | Sim |
| WBS-013 | 0 | `requirements.txt` compatível | Ambiente simples coerente com pyproject | pyproject | Requirements | `requirements.txt` | WBS-012 | Sem divergência não documentada | Sim |
| WBS-014 | 0 | Makefile inicial | Entry points de check/test | Plano | Makefile | `Makefile` | WBS-012 | `make help` documentado | Sim |
| WBS-015 | 0 | Diretórios mínimos | Criar estrutura sem dados fake | Plano | Diretórios | `config/`, `models/`, `docs/`, `src/`, `tests/`, `outputs/schema/` | WBS-000 | Sem `.mod` ou dados fake | Sim |
| WBS-016 | 0 | `models/registry.json` | Criar registry com schema mínimo | Seção 3.3 | Registry | `models/registry.json` | WBS-015 | JSON válido com campos mínimos | Sim |
| WBS-017 | 0 | Output schemas | Contratos de IRF, moments, posterior | SPEC | Schemas | `outputs/schema/` | WBS-015 | Campos mínimos definidos | Sim |
| WBS-018 | 0 | Teste de estrutura | Garantir bootstrap auditável | Estrutura | Teste | `tests/test_project_structure.py` | WBS-015 | Falha se arquivo obrigatório faltar | Sim |
| WBS-019 | 0 | Teste de registry | Validar schema e paths | Registry | Teste | `tests/test_registry.py` | WBS-016 | Registry inválido falha | Sim |
| WBS-020 | 0 | Templates de validação | Criar targets e validation como template | SPEC | Docs templates | `docs/05_replication_targets.md`, `docs/06_model_validation.md` | WBS-000 | `status: template` no validation | Sim |
| WBS-021 | 1a | Data dictionary skeleton | Colunas mínimas e observáveis planejados | SPEC | Dictionary | `docs/02_data_dictionary.md` | Gate 0 | Gate 1a passa | Não |
| WBS-022 | 1a | Schema `DataSeries` | Contrato de metadata | Dictionary | Schema/validators | `src/data_pipeline/` | WBS-021 | Inclui `source_id` | Sim |
| WBS-023 | 1a | Política de `source_id` | Regras para fonte pinada/TBD | Dictionary | Política | `docs/02_data_dictionary.md` | WBS-021 | Proíbe fonte genérica isolada | Não |
| WBS-024 | 1b | Verificar source PIB | Identificador reproduzível | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-025 | 1b | Verificar source IPCA | Identificador reproduzível | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-026 | 1b | Verificar source Selic | Meta/over conforme decisão | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Selic definida | Sim |
| WBS-027 | 1b | Verificar source câmbio | Nominal/real conforme decisão | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Câmbio definido | Sim |
| WBS-028 | 1a | Validação trimestral | Checar frequência | Schema | Tests | `tests/test_observables.py` | WBS-022 | Frequência errada falha | Sim |
| WBS-029 | 1a | Validação revision policy | Bloquear final-revised/real-time mistos | Schema | Tests | `tests/test_observables.py` | WBS-022 | Mistura falha | Sim |
| WBS-030 | 1a | Missing policy | Flags e interpolação documentada | Schema | Tests | `tests/test_data_transformations.py` | WBS-022 | Missing silencioso falha | Sim |
| WBS-031 | 1a | Transform inflação | Contrato sem dados reais | Dictionary | Transform skeleton | `src/data_pipeline/` | WBS-025 | Não usa média simples se índice | Sim |
| WBS-032 | 1a | Transform juros | Média/efetiva conforme medida | Dictionary | Transform skeleton | `src/data_pipeline/` | WBS-026 | Regra documentada | Sim |
| WBS-033A | 2a | Literature map | Mapear papers/seções/equações | SPEC/papers | Literature map | `docs/00a_literature_map.md` | WBS-PRE-000 | Não usa memória sem fonte | Não |
| WBS-034 | 2b | Equation registry template | IDs, blocos, status, versionamento | Literature map | Template | `docs/01_equation_registry.md` | WBS-033A | IDs/status/versionamento | Não |
| WBS-035 | 2b | Bloco monetário | Taylor, meta, choque monetário | Gate 0 | EQ-MON | `docs/01_equation_registry.md` | WBS-034 | IRF tests definidos | Sim |
| WBS-036 | 2b | Bloco externo | UIP, risco, NFA, câmbio | Gate 0 | EQ-EXT | `docs/01_equation_registry.md` | WBS-034 | Fechamento explícito | Sim |
| WBS-037 | 2b | Bloco fiscal | Gasto, primário, dívida | Gate 0 | EQ-FISC | `docs/01_equation_registry.md` | WBS-034 | Dívida/PIB consistente | Sim |
| WBS-038 | 2b | Administrados | `pi_a`, pass-through, choque | Gate 0 | EQ-PRICE | `docs/01_equation_registry.md` | WBS-034 | Processo testável | Sim |
| WBS-039 | 2b | Famílias | Euler, consumo, hábito, trabalho | Literature map | EQ-HH | `docs/01_equation_registry.md` | WBS-034 | Variáveis mapeadas | Sim |
| WBS-040 | 2b | Firmas | Phillips, investimento, `mc`, `q_k` | Literature map | EQ-FIRM | `docs/01_equation_registry.md` | WBS-034 | `mc` e `q_k` explícitos | Sim |
| WBS-041 | 2b | Agregação | Market clearing, NX, absorção | Literature map | EQ-AGG | `docs/01_equation_registry.md` | WBS-034 | Identidades fecham | Sim |
| WBS-042 | 2b | Choques | AR(1), stds e nomes Dynare | SPEC | EQ-SHOCK | `docs/01_equation_registry.md` | WBS-034 | Choque sem equação falha | Sim |
| WBS-043 | 2b/1b | Equações de medida draft | Measurement equations preliminares | Dictionary | EQ-MEAS draft | `docs/01_equation_registry.md` | WBS-021 | Draft até Gate 1b | Sim |
| WBS-044 | 2b | Testar registry | IDs únicos e órfãos | Registry | Tests | `tests/test_equation_registry.py` | WBS-034 | Orfandade falha | Sim |
| WBS-045 | 1b | Verificar source consumo | Core source | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-046 | 1b | Verificar source investimento | Core source | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-047 | 1b | Verificar source governo | Core source | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-048 | 1b | Verificar source exportações | Core source | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-049 | 1b | Verificar source importações | Core source | Dictionary | Source pinado | `docs/02_data_dictionary.md` | WBS-023 | Sem TBD para Gate 1b | Sim |
| WBS-050 | 1b | Verificar livres/administrados | Auxiliar para MVP/estimação | Dictionary | Source pinado/TBD | `docs/02_data_dictionary.md` | WBS-023 | Composição documentada | Sim |
| WBS-051 | 1b | Verificar externas | Juros, inflação, atividade externa | Dictionary | Source pinado/TBD | `docs/02_data_dictionary.md` | WBS-023 | Fonte reproduzível | Sim |
| WBS-052 | 1b | Gerar dataset | Extrair/transformar só após Gate 1b | Sources | CSV model input | `data/observables/`, `data/model_input/` | Gate 1b, Gate 2b | Testes de dados passam | Não |
| WBS-053 | 3 | Notas de calibração | Parâmetros, SS, racional | Registry | Docs | `docs/03_calibration_notes.md` | Gate 2b | Racional por parâmetro | Não |
| WBS-054 | 3 | Estrutura `samba_classic` | Diretório e arquivos planejados | Gate 2b | Estrutura | `model/samba_classic/` | WBS-053 | Sem equações fora do registry | Não |
| WBS-055 | 3 | Implementar calibração | Parâmetros calibrados | Docs | `calibration.m` | `model/samba_classic/calibration.m` | WBS-053 | Parâmetros documentados | Não |
| WBS-056 | 3 | Implementar steady state | Analítico quando viável | Docs | `steady_state.m` | `model/samba_classic/steady_state.m` | WBS-055 | Residual abaixo de tolerância | Não |
| WBS-057 | 3 | Implementar `.mod` por blocos | Traduzir registry para Dynare | Registry | `.mod` | `model/samba_classic/samba_classic.mod` | Gate 2b, WBS-056 | Dynare parseia | Não |
| WBS-058 | 3 | Implementar shocks | Variâncias calibradas | Registry | `shocks.inc` | `model/samba_classic/shocks.inc` | WBS-057 | Choques mapeados | Sim |
| WBS-059 | 3 | Implementar observables inc | Medidas para smoke/piloto | Registry/Data | `observables.inc` | `model/samba_classic/observables.inc` | WBS-043, WBS-052 | Varobs consistentes | Sim |
| WBS-060 | 3 | Wrapper Dynare | Chamada local reprodutível | Make/model | Wrapper | `src/diagnostics/` | WBS-057 | Comando reproduzível | Sim |
| WBS-061 | 3 | Testar steady state | Residuals | Dynare output | Tests | `tests/test_calibration.py` | WBS-056 | Tolerância passa | Sim |
| WBS-062 | 3 | Testar BK | Blanchard-Kahn | Dynare output | Tests | `tests/test_model_outputs.py` | WBS-057 | BK satisfeito | Sim |
| WBS-063 | 3 | Testar IRFs | Sinal, timing, magnitude, retorno | Outputs | Tests | `tests/test_irf_restrictions.py` | WBS-057 | 5 IRFs passam | Sim |
| WBS-064 | 3 | Relatório MVP | Solve, BK, IRFs | Outputs | Report | `outputs/reports/` | WBS-061..063 | Gate 3 aprovado | Não |
| WBS-065 | 3.5 | Protocolo identificação | Iskrev/Dynare identification | Gate 3 | Strategy | `docs/04_estimation_strategy.md` | WBS-064 | Critérios definidos | Não |
| WBS-066 | 3.5 | Rodar identificação local | Avaliar parâmetros | Model/data | Reports | `outputs/identification/` | WBS-065 | Fracos identificados | Não |
| WBS-067 | 3.5 | Classificar parâmetros | Fixar/estimar/restringir | Reports | Tabelas | `docs/04_estimation_strategy.md` | WBS-066 | Sem fraco sem decisão | Não |
| WBS-068 | 4 | Tabela de priors | Priors com fonte/racional | WBS-067 | Docs | `docs/04_estimation_strategy.md` | WBS-067 | Cada prior tem racional | Não |
| WBS-069 | 4 | `priors.inc` | Traduzir priors para Dynare | Priors | Include | `model/samba_classic/priors.inc` | WBS-068 | Sem prior genérico | Não |
| WBS-070 | 4 | Likelihood finito | Teste na calibração | Model/data | Tests | `tests/test_econometric.py` | WBS-069 | Likelihood finito | Não |
| WBS-071 | 4 | Modo posterior | Posterior mode | Priors/data | Outputs | `outputs/posterior/` | WBS-070 | Modo estável | Não |
| WBS-071a | 4 | Estimation smoke test | Run mínimo para filtro/priors/dados | Mode | Smoke outputs | `outputs/posterior/smoke/` | WBS-071 | Sem NaN/Inf; run conclui | Não |
| WBS-072 | 4 | MH piloto | Cadeias curtas | Smoke | Pilot outputs | `outputs/posterior/pilot/` | WBS-071a | Aceitação/R-hat preliminar | Não |
| WBS-073 | 4 | MH completo | Cadeias completas | Pilot | Full posterior | `outputs/posterior/full/` | WBS-072 | Gate 5b aprovado | Não |
| WBS-074 | 5 | Targets de replicação | IRFs/momentos literatura | Literature | Targets | `docs/05_replication_targets.md` | WBS-064 | Targets verificáveis | Sim |
| WBS-075 | 5 | Comparar momentos | Simulado vs dados | Outputs | CSV/report | `outputs/moments/` | WBS-073 | Diferenças explicadas | Sim |
| WBS-076 | 5 | Comparar IRFs | Posterior/calibradas vs benchmarks | Outputs | Report | `outputs/irfs/` | WBS-073 | Sinal/timing/magnitude | Sim |
| WBS-077 | 5 | Benchmarks forecast | AR(1), VAR/BVAR, Focus se disponível | Data | Forecasts | `outputs/forecasts/` | WBS-073 | Benchmarks rodam | Sim |
| WBS-078 | 5 | Pseudo-OOS | Horizontes 1/4/8/12 | Model/benchmarks | Metrics | `outputs/backtesting/` | WBS-077 | RMSE/MAE/CRPS | Não |
| WBS-079 | 5 | Validação final | Relatório de aceite | Outputs | Validation report | `docs/06_model_validation.md` | WBS-075..078 | Gate 6 aprovado | Não |
| WBS-080 | 6 | Especificar Redux | Planejar Redux após MVP | Gate 6 | Spec | Docs/model redux | WBS-079 | Fora do MVP | Não |
| WBS-081 | 7 | Especificar soberano | Spec dedicada soberana | Gate 6 | Spec | `docs/07_sovereign_extension_spec.md` | WBS-079 | Fora do MVP | Não |

---

## 7. Primeiras 25 tarefas em ordem operacional

| Ordem | ID | Título | Definição de pronto | Desbloqueia |
|---|---|---|---|---|
| 1 | WBS-PRE-000 | Validar SPEC consolidado | Divergências registradas ou validação limpa | WBS-000 |
| 2 | WBS-000 | Inicializar Git | Baseline commit feito | Todas as threads |
| 3 | WBS-001 | Modeling decisions template | Campos de status/aprovação presentes | WBS-002 |
| 4 | WBS-002 | Propor amostra MVP | Sample proposed | WBS-003 |
| 5 | WBS-003 | Propor tendência | Trend proposed | WBS-004 |
| 6 | WBS-004 | Propor Taylor/meta | MON proposed | WBS-005 |
| 7 | WBS-005 | Propor UIP/risco | EXT proposed | WBS-006 |
| 8 | WBS-006 | Propor regra fiscal | FISC proposed | WBS-007 |
| 9 | WBS-007 | Propor administrados | ADMIN proposed | WBS-007H |
| 10 | WBS-007H | Aprovação humana | Decisões bloqueantes approved | Gate 0 |
| 11 | WBS-008 | `sample.yaml` | YAML válido | Configs |
| 12 | WBS-009 | `environment.yaml` | Seeds/to_pin | WBS-009.5 |
| 13 | WBS-009.5 | Runtime verification | Versões/limitações documentadas | Fase 3 |
| 14 | WBS-010 | README inicial | Diretórios/gates explicados | WBS-011 |
| 15 | WBS-011 | `.gitignore` | Artefatos corretos ignorados | WBS-012 |
| 16 | WBS-012 | `pyproject.toml` | Pytest/tooling | WBS-013 |
| 17 | WBS-013 | `requirements.txt` | Compatível com pyproject | WBS-014 |
| 18 | WBS-014 | Makefile | `make help` | WBS-015 |
| 19 | WBS-015 | Diretórios mínimos | Sem dados fake | WBS-016 |
| 20 | WBS-016 | Registry | JSON schema mínimo | WBS-017 |
| 21 | WBS-017 | Output schemas | Schemas mínimos | WBS-018 |
| 22 | WBS-018 | Teste estrutura | Passa | WBS-019 |
| 23 | WBS-019 | Teste registry | Passa | WBS-020 |
| 24 | WBS-020 | Templates validação | `docs/06` marcado template | WBS-021 |
| 25 | WBS-021 | Data dictionary skeleton | Gate 1a | WBS-022 |

---

## 8. Prompts para execução futura no Codex

### Prompt 00 — Preflight and Git baseline

```text
Objetivo: validar o SPEC consolidado e inicializar governança mínima do repositório.

Arquivos permitidos:
- README.md
- CONTRIBUTING.md
- .gitignore
- docs/spec_validation_note.md

Comandos permitidos:
- git status
- git init
- git add
- git commit

Arquivos proibidos:
- model/
- src/
- data/
- tests/
- config/ exceto se estritamente necessário para registrar ausência

Tarefas:
1. Verifique se `samba_dsge_br_spec_standalone_consolidado.md` existe.
2. Registre em `docs/spec_validation_note.md` se o SPEC preserva: amostra classic_mvp 2003Q1–2019Q4, COVID excluído, final-revised, UIP debt-elastic baseline, `pi_target_t`, regra fiscal com `sp_target`, administrados AR(1), variáveis `mc`, `q_k`, `wn`, `lambda`, `y_gap`, `y_pot`, `nfa`, `m_int`, `pi_target`.
3. Inicialize Git se `.git/` não existir.
4. Crie `.gitignore` mínimo.
5. Crie README/CONTRIBUTING com política: uma thread = uma branch + PR.
6. Faça baseline commit com SPEC, docs/08 e arquivos criados.

Critérios de aceite:
- `.git/` existe.
- Baseline commit criado.
- Nenhum `.mod`, dado ou script de pipeline foi criado.
- Diff/resumo apresentado.
```

### Prompt 01 — Modeling decisions baseline

```text
Objetivo: criar `docs/00b_modeling_decisions.md` com decisões macro bloqueantes em modo PROPOSED.

Arquivos permitidos:
- docs/00b_modeling_decisions.md

Arquivos proibidos:
- model/
- src/
- data/
- tests/

Regras:
- Codex deve usar `decision_status: proposed`.
- Não usar `approved`.
- Não criar `.mod`.
- Não baixar dados.

Entregável:
- Documento com decisões propostas para amostra, COVID, tendência, Taylor/meta, UIP/risco, regra fiscal, administrados e observáveis iniciais.
- Cada decisão deve ter `alternatives_rejected` e `rationale`.

Critério de saída:
- Documento pronto para revisão humana.
```

### Prompt 02 — Human-approved configs

```text
Objetivo: criar configs apenas após decisões aprovadas por humano.

Pré-condição:
- `docs/00b_modeling_decisions.md` contém decisões bloqueantes com `decision_status: approved`, `approved_by`, `approval_date`.

Arquivos permitidos:
- config/sample.yaml
- config/environment.yaml
- docs/runtime_verification.md

Arquivos proibidos:
- model/
- data/
- src/data_pipeline/

Critérios:
- YAML válido.
- Sem versão Dynare inventada.
- Runtime local verificado ou limitação documentada.
```

### Prompt 03 — Repository bootstrap and registry

```text
Objetivo: criar estrutura mínima, registry e testes iniciais.

Arquivos permitidos:
- README.md
- pyproject.toml
- requirements.txt
- Makefile
- models/registry.json
- outputs/schema/
- tests/test_project_structure.py
- tests/test_registry.py

Regras:
- `models/` = metadata.
- `model/` = Dynare/MATLAB.
- `pyproject.toml` = fonte de verdade Python.
- Não criar dados fake.
- Não criar `.mod`.

Critérios:
- `pytest --collect-only` roda.
- Registry contém campos mínimos definidos no plano.
```

### Prompt 04 — Data dictionary skeleton

```text
Objetivo: criar `docs/02_data_dictionary.md` como skeleton.

Arquivos permitidos:
- docs/02_data_dictionary.md

Arquivos proibidos:
- data/
- model/

Critérios:
- Colunas obrigatórias presentes.
- `source_id` pinado ou `TBD-verify-in-task-<WBS-ID>`.
- Gate 1a atingido.
```

### Prompt 05 — Core source verification

```text
Objetivo: pinar fontes core para Gate 1b.

Arquivos permitidos:
- docs/02_data_dictionary.md
- docs/source_verification_notes.md

Regra crítica:
Se a fonte não estiver explicitamente disponível no repo, contexto, documentação oficial acessível ou arquivo anexado, mantenha TBD. Não use memória interna para cravar SGS/SIDRA.

Critérios:
- Sem TBD nos nove core sources antes de Gate 1b.
- Se não conseguir verificar, registrar bloqueio e não prosseguir para dados.
```

### Prompt 06 — Data pipeline contracts

```text
Objetivo: criar contratos e testes de dados, sem extração real se Gate 1b não passou.

Arquivos permitidos:
- src/data_pipeline/
- tests/test_data_transformations.py
- tests/test_observables.py

Critérios:
- Teste falha para `source_id` ausente.
- Teste falha para mistura final-revised/real-time.
- Teste aceita TBD apenas antes de Gate 1b.
```

### Prompt 07 — Literature map

```text
Objetivo: criar `docs/00a_literature_map.md`.

Arquivos permitidos:
- docs/00a_literature_map.md

Critérios:
- Colunas: paper, section, equation/table/figure, model block, parameters used, replication target, status.
- Não inventar equações não rastreadas.
```

### Prompt 08 — Equation registry skeleton

```text
Objetivo: criar `docs/01_equation_registry.md`.

Arquivos permitidos:
- docs/01_equation_registry.md
- tests/test_equation_registry.py

Arquivos proibidos:
- model/

Critérios:
- IDs únicos.
- Cada equação tem bloco, fonte, variáveis, parâmetros, choques, status e testes.
```

### Prompt 09 — Equation registry core blocks

```text
Objetivo: preencher blocos MON, EXT, FISC, ADMIN, AGG, HH e FIRM.

Arquivos permitidos:
- docs/01_equation_registry.md
- tests/test_equation_registry.py

Critérios:
- Taylor forward-looking com `pi_target_t`.
- UIP/prêmio de risco testável.
- Regra fiscal com dívida/PIB.
- Administrados com processo testável.
- Measurement equations finais permanecem draft se Gate 1b não passou.
```

### Prompt 10 — Calibration notes and validation templates

```text
Objetivo: preparar calibração e targets antes do `.mod`.

Arquivos permitidos:
- docs/03_calibration_notes.md
- docs/05_replication_targets.md
- docs/06_model_validation.md

Critérios:
- `docs/06_model_validation.md` contém front matter:
  status: template
  do_not_treat_as_validation_result: true
- IRF targets incluem sinal, timing, magnitude e benchmark.
```

### Prompt 11 — Implement calibrated SAMBA classic

```text
Objetivo: implementar SAMBA clássico calibrado somente após Gates 0, 1b, 2b.

Pré-condições:
- Gate 0 approved.
- Gate 1b passed.
- Gate 2b passed.
- Runtime Dynare/MATLAB/Octave verificado.

Arquivos permitidos:
- model/samba_classic/
- src/diagnostics/
- tests/test_calibration.py
- tests/test_model_outputs.py
- tests/test_irf_restrictions.py

Critérios:
- Steady state fecha.
- BK passa.
- IRFs-chave passam sinal, timing e magnitude.
- Sem estimação Bayesiana.
```

### Prompt 12 — Local identification gate

```text
Objetivo: rodar identificação local antes de MH.

Arquivos permitidos:
- docs/04_estimation_strategy.md
- outputs/identification/
- tests/test_econometric.py

Critérios:
- Parâmetros fracos classificados.
- Nenhum parâmetro fraco entra em MH sem tratamento.
- Próximo passo bloqueado se Gate 4 falhar.
```

### Prompt 13 — Estimation smoke test and Bayesian pilot

```text
Objetivo: rodar smoke test de estimação e só então MH piloto.

Pré-condições:
- Gate 4 passed.
- Priors com fonte/racional.

Critérios:
- Likelihood finito.
- Run mínimo sem NaN/Inf.
- MH piloto apenas após smoke test.
```

---

## 9. Estratégia de testes

| Camada | Teste | Propósito | Condição de aprovação | Fase |
|---|---|---|---|---|
| Governança | `test_git_initialized` | Garantir versionamento | `.git/` existe no repo | 0 |
| Governança | `test_no_approved_decisions_from_codex` | Impedir autoaprovação | Propostas Codex não têm `approved_by` | -1 |
| Config | `test_sample_config_valid` | Validar amostras | Datas e policies válidas | -1 |
| Config | `test_environment_runtime_documented` | Runtime rastreável | Versão detectada ou limitação documentada | 0 |
| Registry | `test_model_registry_schema` | Validar registry | Campos mínimos presentes | 0 |
| Dados | `test_source_id_required` | Bloquear fonte sem ID | Todo observable tem `source_id` | 1a |
| Dados | `test_core_sources_no_tbd_after_gate_1b` | Endurecer Gate 1b | Core sources sem TBD | 1b |
| Dados | `test_no_generic_source_only` | Bloquear “BCB/IBGE” genérico | Fonte genérica isolada falha | 1a |
| Dados | `test_final_revised_not_mixed_with_realtime` | Separar revision policies | Mistura falha | 1a |
| Dados | `test_inflation_aggregation` | Evitar média simples inadequada | Transform coerente | 1b |
| Equation registry | `test_equation_ids_unique` | Evitar duplicação | IDs únicos | 2b |
| Equation registry | `test_no_orphan_variables` | Garantir rastreabilidade | Sem órfãs | 2b |
| Dynare | `test_steady_state_residuals_below_tolerance` | Validar SS | Residual abaixo de tolerância | 3 |
| Dynare | `test_bk_conditions_satisfied` | Validar determinacy | BK passa | 3 |
| IRF | `test_irf_magnitude_and_timing` | Evitar plausibilidade vaga | Sinal/timing/magnitude/benchmark | 3 |
| Econométrico | `test_likelihood_is_finite_at_calibration` | Pré-MH | Likelihood finito | 3.5/4 |
| Econométrico | `test_weak_parameters_are_handled` | Evitar MH fraco | Cada fraco tem decisão | 3.5 |
| Econométrico | `test_estimation_smoke_run` | Fail-fast | Run mínimo conclui | 4 |
| Econométrico | `test_posterior_chains_rhat` | Convergência | R-hat < 1.1 em parâmetros-chave | 4 |
| Measurement | `test_measurement_errors_within_allowed_volatility` | Evitar lixeira | Dentro de limite | 4 |
| Backtesting | `test_backtesting_metrics_exist` | Validar pseudo-OOS | RMSE/MAE/CRPS presentes | 5 |

---

## 10. Estratégia de dados

Pipeline:

```text
raw -> interim -> clean -> observables -> model_input
```

Regra nova:

```text
Nenhuma extração real, transformação ou geração de dataset antes de Gate 1b.
```

### 10.1 Core sources obrigatórios para Gate 1b

| Observable | Variável | WBS |
|---|---|---|
| PIB real | `y` | WBS-024 |
| IPCA cheio | `pi` | WBS-025 |
| Selic | `r` | WBS-026 |
| Câmbio | `q`/`s` | WBS-027 |
| Consumo privado | `c` | WBS-045 |
| Investimento | `i` | WBS-046 |
| Gasto do governo | `g` | WBS-047 |
| Exportações | `x` | WBS-048 |
| Importações | `m` | WBS-049 |

### 10.2 Política de fonte

```text
source = instituição/base.
source_id = identificador reproduzível.
```

Exemplos aceitáveis de `source_id`:

```text
SGS code confirmado
SIDRA table/variável/classificação confirmada
URL oficial de arquivo
dataset versionado
arquivo local com checksum
```

Exemplo proibido:

```text
source: BCB
source_id:
```

---

## 11. Estratégia Dynare/MATLAB/Octave

### 11.1 Runtime

Antes da Fase 3:

```text
- detectar versão de Dynare;
- detectar MATLAB ou Octave;
- registrar limitações;
- registrar seeds;
- documentar se CI rodará apenas Python ou também Dynare/Octave.
```

Não fixar versão sem verificação local.

### 11.2 Estrutura

```text
model/samba_classic/
├── samba_classic.mod
├── calibration.m
├── steady_state.m
├── shocks.inc
├── observables.inc
└── priors.inc
```

### 11.3 Ordem

```text
1. calibration.m
2. steady_state.m
3. samba_classic.mod
4. shocks.inc
5. smoke stoch_simul
6. observables.inc
7. tests
8. priors.inc apenas na Fase 4
```

---

## 12. Estratégia de identificação e estimação

Ordem obrigatória:

```text
1. Modelo calibrado resolve.
2. Steady state fecha.
3. BK passa.
4. IRFs calibradas passam.
5. Likelihood finito.
6. Identificação local.
7. Parâmetros fracos tratados.
8. Priors revisados.
9. Posterior mode.
10. Estimation smoke test.
11. MH piloto.
12. MH completo.
```

### 12.1 Estimation smoke test

Objetivo:

```text
Testar filtro, dados, priors e likelihood em configuração mínima antes do MH piloto.
```

Critérios:

```text
- sem NaN/Inf;
- likelihood finito;
- outputs básicos criados;
- nenhuma chain longa iniciada.
```

---

## 13. Estratégia de validação e backtesting

Validação final exige:

```text
- momentos simulados vs dados;
- IRFs calibradas e posteriores vs literatura;
- decomposição de variância;
- decomposição histórica;
- pseudo-OOS;
- benchmarks AR(1), VAR/BVAR e Focus se disponível;
- RMSE, MAE, CRPS;
- horizontes 1, 4, 8, 12.
```

`docs/06_model_validation.md` criado antes do modelo deve ter:

```yaml
---
status: template
do_not_treat_as_validation_result: true
---
```

Só muda para resultado de validação após Gate 6.

---

## 14. Registro de riscos

| Risco | Severidade | Probabilidade | Sintoma | Mitigação | Gate |
|---|---|---|---|---|---|
| Codex aprovar próprias decisões | Alta | Média | `approved_by: Codex` | Gate 0 humano | Gate 0 |
| Sem Git no início | Alta | Média | Mudanças irrecuperáveis | WBS-000 | Preflight |
| Pipeline com TBD core | Alta | Média | Dataset falso | Gate 1b | Gate 1b |
| `source_id` inventado | Alta | Média | Código SGS/SIDRA não verificável | Política TBD | Gate 1 |
| Registry baseado em memória | Alta | Média | Equações sem fonte | Literature map | Gate 2a |
| `models/` vs `model/` confuso | Média | Média | Arquivos no lugar errado | README + tests | Gate 0 |
| `pyproject`/`requirements` divergentes | Média | Média | Ambientes diferentes | Fonte de verdade | Gate 0 |
| Dynare incompatível | Média | Média | Fase 3 falha | WBS-009.5 | Gate 3 |
| BK falha | Alta | Média | Indeterminação | Revisar registry/SS | Gate 3 |
| Identificação fraca | Alta | Alta | Chains ruins | Gate 4 | Gate 4 |
| Measurement error excessivo | Alta | Média | Modelo explica tudo como erro | Limites/teste | Gate 5 |
| Redux entra cedo | Alta | Baixa | MVP inchado | Fase 6 bloqueada | Gate 6 |

---

## 15. Decisões pendentes

| Decisão | Classificação | Resolver em | Observação |
|---|---|---|---|
| Aprovação humana das decisões Gate 0 | Bloqueante para MVP | Gate 0 | Codex só propõe. |
| Versão Dynare/MATLAB/Octave | Bloqueante para `.mod` | Antes da Fase 3 | Verificar runtime local. |
| Forma final da UIP se SAMBA clássico exigir alternativa | Bloqueante para MVP | Gate 0/2 | Registry documenta alternativa. |
| Equação de medida da Selic | Bloqueante para estimação | Gate 1b/2b | Meta vs over. |
| Tratamento exato de `pi_target_t` | Bloqueante para MVP | Gate 0 | Exógena ou `varexo_det`. |
| Core source IDs | Bloqueante para dados | Gate 1b | Sem TBD em core. |
| Priors numéricos | Bloqueante para estimação | Fase 4 | Fonte/racional obrigatórios. |
| Focus no backtesting | Não bloqueante para MVP | Fase 5 | Usar se reproduzível. |
| Rolling vs expanding | Bloqueante para backtesting | Fase 5 | Decidir antes de rodar. |
| Redux 2001Q4–2019Q4 e tratamento de 2002 | Bloqueante para Redux | Fase 6 | Não resolver no improviso. |
| SMC Redux | Bloqueante para Redux | Fase 6 | Exige benchmark compute. |
| Dominância fiscal | Bloqueante para soberano | Fase 7 | Spec própria. |

---

## 16. Paralelização futura

### Sequencial estrito

```text
WBS-PRE-000 -> WBS-000 -> WBS-001..007 -> WBS-007H -> Gate 0
Gate 0 -> Gate 1a / Gate 2a
Gate 1b + Gate 2b -> Gate 3
Gate 3 -> Gate 4 -> Gate 5a -> Gate 5b -> Gate 6
```

### Paralelizável após Gate 0

```text
- Bootstrap técnico: WBS-010..020
- Literature map: WBS-033A
- Dictionary skeleton: WBS-021..023
- Verificação de fontes: WBS-024..027 e WBS-045..051
- Blocos estruturais do equation registry: WBS-035..042
```

### Não paralelizar

```text
- Aprovação humana Gate 0
- Geração de dataset
- Implementação do `.mod`
- Identificação local
- MH completo
- Backtesting final
- Redux
- Extensão soberana
```

---

## 17. Definition of Done geral

### Pronto para começar implementação operacional

```text
- SPEC validado.
- Git inicializado.
- Baseline commit feito.
- Plano v2 consolidado no repo.
```

### Pronto para começar configs/data/registry

```text
- Gate 0 aprovado por humano.
```

### Pronto para começar extração de dados

```text
- Gate 1b aprovado.
- Core source IDs sem TBD.
```

### Pronto para começar o `.mod`

```text
- Gate 0 aprovado.
- Gate 1b aprovado.
- Gate 2b aprovado.
- Runtime verificado.
- Calibration notes criadas.
```

### Pronto para começar estimação

```text
- Gate 3 aprovado.
- Likelihood finito.
- Gate 4 aprovado.
- Priors com fonte/racional.
- Measurement errors com limites.
```

### Pronto para começar Redux

```text
- Gate 6 aprovado.
- Decisão sobre amostra 2001Q4–2019Q4/2002 resolvida.
- SMC/compute especificado.
```

### Pronto para começar soberano

```text
- docs/07_sovereign_extension_spec.md aprovado.
```

---

## 18. Resumo executivo

Sequência recomendada agora:

```text
1. WBS-PRE-000 — Validar SPEC consolidado.
2. WBS-000 — Inicializar Git e baseline commit.
3. Thread 01 — Modeling decisions baseline, modo proposed.
4. Revisão humana e Gate 0 approved.
5. Configs, registry e skeletons.
6. Gate 1a e Gate 2a.
7. Core source verification e Gate 1b.
8. Equation registry mínimo e Gate 2b.
9. Só então SAMBA clássico calibrado.
```

Maior risco persistente:

```text
Pular governança e escrever um `.mod` tecnicamente executável, mas incompatível com amostra, dados, equações de medida e critérios de validação.
```

Primeira thread sugerida:

```text
Thread 00 — Preflight and Git baseline
```

Segunda thread sugerida:

```text
Thread 01 — Modeling decisions baseline
Escopo: criar apenas docs/00b_modeling_decisions.md
Modo: proposed
Saída: decisões prontas para aprovação humana
```

---

## 19. Agrupamento em PRs operacionais

| PR | Escopo | WBS |
|---|---|---|
| PR 00 | Preflight + Git baseline | WBS-PRE-000, WBS-000 |
| PR 01 | Gate 0 decisions proposed | WBS-001..007 |
| PR 02 | Gate 0 human approval + configs | WBS-007H..009.5 |
| PR 03 | Repo bootstrap | WBS-010..020 |
| PR 04 | Data dictionary skeleton | WBS-021..023 |
| PR 05 | Literature map | WBS-033A |
| PR 06 | Core source verification | WBS-024..027, WBS-045..049 |
| PR 07 | Data pipeline contracts | WBS-028..032 |
| PR 08 | Equation registry core | WBS-034..044 |
| PR 09 | Dataset generation | WBS-052 |
| PR 10 | Calibration notes | WBS-053 |
| PR 11 | Dynare classic calibrated | WBS-054..064 |
| PR 12 | Identification gate | WBS-065..067 |
| PR 13 | Priors + estimation smoke | WBS-068..071a |
| PR 14 | Bayesian pilot/full estimation | WBS-072..073 |
| PR 15 | Validation/backtesting | WBS-074..079 |

---

## 20. Autocrítica final

| Pergunta | Resultado |
|---|---|
| O plano começa cedo demais no `.mod`? | Não. `.mod` só depois de Gate 0, Gate 1b, Gate 2b e runtime verificado. |
| O plano permite que Codex aprove decisões macro? | Não. Codex só propõe; humano aprova. |
| O plano permite pipeline com `TBD` core? | Não. Gate 1b bloqueia extração/transformação. |
| O plano exige dados antes de observáveis? | Não. Data dictionary e registry vêm antes do dataset. |
| O plano permite estimação antes de identificação? | Não. Gate 4 e smoke test bloqueiam. |
| O plano mistura MVP com Redux ou soberano? | Não. Ambos estão fora do MVP. |
| O plano tem tarefas vagas demais? | Reduzido via WBS, PRs e critérios de aceite. |
| O plano inventa `source_id`? | Não. Fonte não confirmada fica TBD com WBS. |
| O plano preserva o SPEC? | Sim, com Preflight para verificar divergências. |
