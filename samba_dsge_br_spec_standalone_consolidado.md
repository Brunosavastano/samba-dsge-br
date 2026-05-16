# SPEC Standalone Consolidado — Réplica SAMBA/DSGE Brasil

**Projeto:** `samba-dsge-br`  
**Documento:** SPEC standalone consolidado  
**Versão:** v3.0-consolidated  
**Data:** 2026-05-16  
**Status:** pronto para servir como fonte única de referência antes da criação do plano de implementação.

---

## Como usar este documento

Este arquivo consolida, em um único Markdown standalone:

```text
1. a versão revisada do SPEC do projeto SAMBA/DSGE Brasil;
2. a revisão adversarial incorporada ao SPEC;
3. as decisões explícitas sobre o que foi aceito, aceito parcialmente ou rejeitado;
4. a versão operacional final do escopo, arquitetura, gates, roadmap, riscos e critérios de aceite.
```

Este documento deve substituir o uso separado dos arquivos:

```text
00_project_spec_samba_dsge_br_v2.md
01_adversarial_review_incorporation_decisions.md
```

O feedback sobre o prompt do Codex e o respectivo prompt operacional não fazem parte do corpo deste SPEC. Eles são artefatos de execução, não da especificação macroeconométrica do projeto.

---

## Índice

1. [Resumo executivo consolidado](#1-resumo-executivo-consolidado)
2. [Decisões de incorporação da revisão crítica](#2-decisões-de-incorporação-da-revisão-crítica)
3. [SPEC consolidado do projeto](#3-spec-consolidado-do-projeto)
4. [Ordem obrigatória de execução](#4-ordem-obrigatória-de-execução)
5. [Checklist de prontidão para implementação](#5-checklist-de-prontidão-para-implementação)
6. [Fonte única de verdade](#6-fonte-única-de-verdade)

---

# 1. Resumo executivo consolidado

O projeto `samba-dsge-br` busca construir uma réplica pública, modular, auditável e extensível do modelo SAMBA/DSGE para a economia brasileira.

A revisão crítica mostrou que a versão inicial do SPEC tinha boa engenharia de projeto, mas subespecificava decisões macroeconométricas bloqueantes. A versão consolidada corrige isso incorporando, antes da implementação Dynare:

```text
1. decisão explícita de amostra;
2. tratamento de COVID e quebras estruturais;
3. separação final-revised vs real-time;
4. tratamento de tendência;
5. regra monetária forward-looking com inflação-meta explícita;
6. UIP/prêmio de risco especificado;
7. regra fiscal com feedback sobre dívida/PIB;
8. processo para preços administrados;
9. variáveis estruturais antes ausentes;
10. data dictionary com source_id obrigatório;
11. identificação local antes de Metropolis-Hastings;
12. backtesting e validação preditiva;
13. gates técnicos entre fases.
```

O MVP permanece deliberadamente limitado:

```text
- SAMBA clássico;
- modelo calibrado;
- log-linear;
- primeira ordem;
- Dynare/MATLAB/Octave;
- pipeline mínimo de dados;
- IRFs e checagens BK;
- sem Redux;
- sem extensão soberana;
- sem estimação Bayesiana completa.
```

O projeto só deve avançar para estimação depois de:

```text
1. steady state fechado;
2. Blanchard-Kahn satisfeito;
3. IRFs calibradas com sinal, timing e magnitude plausíveis;
4. likelihood finito;
5. identificação local concluída;
6. priors documentados.
```

---

# 2. Decisões de incorporação da revisão crítica

# Decisões de incorporação — Revisão crítica do SPEC SAMBA/DSGE

## Veredito

A revisão crítica é majoritariamente útil, mas deve ser tratada como triagem de risco, não como substituto do design do projeto. Incorporei as recomendações que reduzem retrabalho e risco econométrico. Não incorporei recomendações excessivamente prescritivas, não verificadas ou prematuras para o MVP.

---

## Aceito e incorporado

| Tema | Decisão incorporada | Motivo |
|---|---|---|
| Camada de configuração | Adicionado `config/` com `sample.yaml`, `classic_mvp.yaml`, `classic_estimation.yaml`, `redux_smc.yaml` | Sem isso, amostra, priors e runs ficam hardcoded. |
| Registry de modelos | Adicionado `models/registry.json` | Necessário para rastrear `.mod`, dados, priors, calibração e versão do registry. |
| Schema de outputs | Adicionado `outputs/schema/` | Evita quebra silenciosa de relatórios e artefatos. |
| Decisões macro antes do código | Adicionado `docs/00b_modeling_decisions.md` como Sprint -1 | UIP, regra fiscal, tendência, amostra e COVID não podem ser decididos depois do `.mod`. |
| Amostra e COVID | Definidos defaults: `classic_mvp` 2003Q1-2019Q4; `redux_replication` 2001Q4-2019Q4; COVID excluído no baseline | Reduz quebras estruturais e evita contaminar Kalman/MH com pandemia. |
| Tratamento de tendência | Explicitado: clássico em torno de steady state determinístico; sem HP bilateral na estimação | Evita look-ahead bias e inconsistência entre dados e modelo. |
| Regra monetária | Forward-looking com inflação esperada, hiato e meta explícita | Remove ambiguidade "inflação esperada ou corrente". |
| Inflação-meta | Adicionados `pi_target_t` e `eps_pi_target` | Mudanças de meta não devem ser absorvidas por choque monetário. |
| UIP/prêmio de risco | Especificada UIP baseline com NFA/debt-elastic closure e risco AR(1) | "UIP modificada" sem equação não é especificação. |
| Regra fiscal | Adicionado `sp_target` com feedback sobre dívida/PIB e hiato | Sem regra fiscal o bloco fiscal fica subidentificado. |
| Preços administrados | Processo AR(1) com pass-through cambial/importados e meta | Evita tratar administrados como choque genérico. |
| Variáveis ausentes | Adicionados `mc`, `q_k`, `wn`, `lambda`, `y_gap`, `y_pot`, `nfa`, `m_int`, `pi_target` | Necessários para Phillips, investimento com Q, regra de Taylor e setor externo. |
| Data dictionary | Adicionados `source_id`, `base_year`, `revision_policy`, `vintage_date`, `sa_method` | Reprodutibilidade exige fonte pinada. |
| Identificação local | Adicionada Sprint 3.5 antes de MH | Evita rodar MCMC em parâmetros fracamente identificados. |
| Priors | Exigida tabela de priors com fonte/racional | Templates genéricos não bastam para Brasil. |
| Testes econométricos | Adicionados likelihood finito, R-hat, Hessiana, ML estável, measurement errors | Testes funcionais não validam DSGE estimado. |
| Backtesting | Adicionado protocolo pseudo-OOS contra AR(1), VAR/BVAR e Focus se disponível | Modelo precisa competir com benchmarks. |
| Roadmap | Alongadas Sprints 2, 3, 4, 6 e 7 | Cronograma original era otimista demais. |

---

## Parcialmente aceito

| Tema | Parte aceita | Parte não aceita |
|---|---|---|
| `Dynare 6.1+` | Concordo que a versão deve ser pinada. | Não vou fixar `6.1+` cegamente. O spec agora exige `to_pin` após validação local. |
| SMC com 4.000-8.000 partículas | Concordo que Redux precisa de plano computacional, ESS e tempering. | Não incorporei número fixo; o WP578 usa estratégia própria e benchmark computacional deve vir antes. |
| SGU debt-elastic UIP | Concordo que é baseline razoável de fechamento. | Não trato como única opção; o registry deve permitir alternativa alinhada ao SAMBA clássico. |
| 2003Q1-2019Q4 | Concordo para `classic_mvp`. | Para Redux, preservo 2001Q4-2019Q4, que é a amostra documentada no WP578. |
| Snakemake/Prefect | Concordo que Make sozinho pode ficar frágil. | Para MVP, Make segue como entrypoint; Snakemake/Prefect entra como opcional. |
| CI com MATLAB/Dynare | Concordo que é difícil. | Não excluo smoke tests com Octave/Dynare se o ambiente permitir. |
| Priors numéricos sugeridos | Concordo com priors brasileiros informativos. | Não incorporei números específicos sem tabela de fontes e validação. |

---

## Não incorporado

| Recomendação/afirmação | Por que não incorporar |
|---|---|
| “Como está, não roda” como formulação literal | Um spec não “roda”. A crítica correta é que o projeto não deveria ir ao `.mod` antes das decisões macroeconométricas. |
| “Castro-Souza-Sobrinho (2016) como Redux mais próximo” | O alvo público moderno mais claro é o WP578 de Fasolo et al. (2023). A referência sugerida precisa ser verificada antes de entrar como canônica. |
| Setorializar markup de livres já no MVP | É válido para extensão, mas amplia demais o MVP. Mantido como possibilidade futura. |
| Modelar regimes fiscais 2016/2023 no MVP | Importante para análise histórica longa, mas desloca o MVP para regime-switching. Mantido fora da primeira fase. |
| Real-time data como requisito do MVP | Para réplica acadêmica, final-revised é suficiente. Real-time entra em fase operacional/backtesting avançado. |
| Número fixo de partículas SMC | Prematuro sem benchmark de runtime e sem implementação Redux. |
| FTPL/dominância fiscal já no core | Importante para extensão soberana, mas não deve contaminar a réplica SAMBA clássica. Vai para spec dedicada. |

---

## Próxima ação recomendada

Antes de escrever qualquer `.mod`, escrever:

```text
docs/00b_modeling_decisions.md
```

com as seguintes decisões fechadas:

```text
1. amostra;
2. tratamento de COVID;
3. tratamento de tendência;
4. regra de Taylor;
5. inflação-meta;
6. UIP/prêmio de risco;
7. regra fiscal;
8. processo de preços administrados;
9. conjunto inicial de observáveis;
10. versão de Dynare/MATLAB/Octave.
```


---

# 3. SPEC consolidado do projeto

# Spec do Projeto — Réplica SAMBA/DSGE Brasil v2

**Projeto:** `samba-dsge-br`  
**Versão do spec:** v2.0  
**Status:** revisado após crítica técnica adversarial  
**Objetivo:** construir uma réplica pública, modular, auditável e extensível do modelo SAMBA/DSGE para a economia brasileira, começando por um núcleo clássico calibrado, evoluindo para estimação Bayesiana e, depois, para uma versão inspirada no SAMBA Redux e uma extensão soberana.

---

## 0. Decisões incorporadas nesta versão

Esta versão incorpora apenas as recomendações da revisão crítica que reduzem risco técnico, macroeconométrico ou operacional. As principais mudanças são:

```text
1. Adição de camada de configuração em config/.
2. Adição de models/registry.json para versionar modelo, dados, priors e calibração.
3. Adição de outputs/schema/ para padronizar artefatos.
4. Criação obrigatória de docs/00b_modeling_decisions.md antes do .mod.
5. Definição explícita de amostra, tratamento de COVID e dados revisados vs real-time.
6. Definição explícita de tratamento de tendência.
7. Definição preliminar de UIP/prêmio de risco.
8. Definição preliminar de regra fiscal.
9. Inclusão de inflação-meta como variável/processo.
10. Inclusão de variáveis estruturais ausentes: mc, q_k, wn, lambda, y_gap, y_pot, nfa.
11. Separação entre variáveis provisórias e variáveis derivadas do equation registry.
12. Especificação de data dictionary com source_id, vintage, base_year e revision metadata.
13. Inclusão de identificação local antes de Metropolis-Hastings.
14. Inclusão de testes econométricos, não apenas testes funcionais.
15. Inclusão de protocolo de backtesting.
16. Revisão do roadmap com Sprint -1 e Sprint 3.5.
17. Separação clara entre réplica SAMBA, Redux e extensão soberana.
```

---

## 1. Referências canônicas do projeto

O projeto deve se ancorar em duas referências públicas principais:

```text
1. SAMBA clássico:
   Castro, Gouvea, Minella, Santos e Souza-Sobrinho.
   "SAMBA: Stochastic Analytical Model with a Bayesian Approach".
   Banco Central do Brasil, Working Paper 239, 2011.

2. SAMBA Redux:
   Fasolo, Araújo, Jorge, Kornelius e Marinho.
   "Brazilian Macroeconomic Dynamics Redux: Shocks, Frictions, and Unemployment in SAMBA Model".
   Banco Central do Brasil, Working Paper 578, 2023.
```

Referências secundárias para componentes específicos:

```text
- Smets-Wouters para rigidezes nominais, hábito, custos de ajustamento e estrutura medium-scale.
- Erceg-Henderson-Levin para rigidez salarial.
- Galí-Smets-Wouters para desemprego involuntário na fase Redux.
- Schmitt-Grohé-Uribe para fechamento de economia pequena aberta via prêmio de risco debt-elastic.
- Iskrev e Komunjer-Ng para identificação local.
- Lenza-Primiceri para tratamento de outliers pandêmicos, apenas em fase pós-MVP.
```

---

## 2. Princípio central de execução

O projeto não começa com o arquivo `.mod`.

O projeto começa com decisões macroeconométricas documentadas, porque sem elas o `.mod` vira uma coleção de equações incompatíveis com os observáveis.

Ordem obrigatória:

```text
1. docs/00b_modeling_decisions.md
2. docs/01_equation_registry.md
3. docs/02_data_dictionary.md
4. model/samba_classic/samba_classic.mod
5. model/samba_classic/observables.inc
6. model/samba_classic/priors.inc
7. estimation/backtesting
```

---

## 3. Escopo

### 3.1 Fase 1 — MVP calibrado

A Fase 1 entrega o núcleo SAMBA clássico calibrado, log-linear, resolvido em primeira ordem.

Entregas:

```text
1. decisões macroeconométricas documentadas;
2. equation registry mínimo;
3. data dictionary mínimo;
4. modelo Dynare calibrado;
5. steady state analítico quando viável;
6. checagem Blanchard-Kahn;
7. IRFs para choques-chave;
8. testes funcionais e econômicos básicos;
9. outputs reproduzíveis;
10. relatório de validação do MVP.
```

A Fase 1 não estima o modelo completo.

### 3.2 Fase 2 — Estimação Bayesiana

A Fase 2 adiciona:

```text
1. equações de medida;
2. priors ancorados na literatura brasileira;
3. análise de identificação local antes de MH;
4. estimação Bayesiana;
5. posterior IRFs;
6. decomposição de variância;
7. decomposição histórica;
8. backtesting pseudo-out-of-sample.
```

### 3.3 Fase 3 — Redux

A Fase 3 adiciona:

```text
1. desemprego involuntário;
2. participação na força de trabalho;
3. bens importados na cesta de consumo;
4. VAR estrutural externo com choques identificados;
5. conjunto expandido de observáveis;
6. SMC ou alternativa computacional validada.
```

### 3.4 Fase 4 — Extensão soberana

A Fase 4 só começa depois de uma spec própria:

```text
docs/07_sovereign_extension_spec.md
```

Essa spec deve escolher explicitamente:

```text
1. forma do prêmio de risco endógeno;
2. regra fiscal;
3. framework de dominância fiscal;
4. cenários quantitativos;
5. elasticidades fiscal-risco-câmbio-inflação-Selic-dívida.
```

---

## 4. Não escopo

O projeto não tentará reconstruir o modelo operacional interno do Banco Central do Brasil.

Também não faz parte do MVP:

```text
1. nowcasting de alta frequência;
2. uso operacional em tempo real;
3. integração automática com Focus em tempo real;
4. frontend web;
5. julgamento discricionário de política monetária;
6. dados proprietários;
7. estimação Redux;
8. extensão soberana.
```

---

## 5. Decisões macroeconométricas obrigatórias

Arquivo obrigatório:

```text
docs/00b_modeling_decisions.md
```

### 5.1 Amostra

Configuração inicial:

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
    rationale: "Amostra documentada no SAMBA Redux."
  future_operational:
    start: "2003Q1"
    end: "current"
    covid_treatment: "to_be_defined"
    data_revision: "real_time_vintage"
    status: "out_of_mvp"
```

Regra:

```text
- MVP e réplica acadêmica usam dados final-revised.
- Real-time vintages entram apenas na fase operacional/backtesting avançado.
- COVID é excluído da estimação linear-Gaussiana inicial.
- Tratamento via dummies/outlier-robust likelihood fica fora do MVP.
```

### 5.2 Tratamento de tendência

Escolha inicial:

```text
SAMBA clássico:
- modelo log-linear em torno de steady state determinístico;
- observáveis reais em crescimento ou log-desvio conforme equação de medida;
- inflação e juros em desvios de steady state/meta quando aplicável;
- não usar HP bilateral na estimação.

SAMBA Redux:
- permitir produtividade não estacionária e inflação-meta não estacionária conforme especificação do Redux;
- hiato do produto observado ou semi-observado documentado separadamente;
- tratamento de tendência deve seguir a documentação do WP578 quando for fase Redux.
```

### 5.3 Política monetária

Regra-base:

```text
r_t = rho_r * r_{t-1}
      + (1 - rho_r) * [r_ss + phi_pi * (E_t pi_{t+1} - pi_target_t) + phi_y * y_gap_t]
      + eps_monetary_t
```

Decisão:

```text
- A regra deve usar inflação esperada, não ficar ambígua entre inflação corrente e esperada.
- pi_target_t entra explicitamente.
- y_gap_t deve existir como variável ou proxy observável, não apenas como texto.
```

### 5.4 Inflação-meta

Variáveis/processos:

```text
pi_target_t
eps_pi_target
```

Implementação inicial:

```text
Fase clássica:
- pi_target_t como série exógena ou deterministic exogenous variable;
- choque de meta opcional, desligado no MVP calibrado se necessário.

Fase Redux:
- processo persistente de meta de inflação com choques antecipados, conforme documentação do Redux.
```

### 5.5 UIP e prêmio de risco

A UIP não pode ficar como “modificada” sem especificação.

Baseline provisório do MVP:

```text
r_t - E_t pi_{t+1}
=
r_star_t - E_t pi_star_{t+1}
+ E_t Δq_{t+1}
+ psi_nfa * (nfa_t - nfa_ss)
+ risk_t
```

Processo do risco:

```text
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

Observação:

```text
A forma debt-elastic/NFA-elastic é baseline de fechamento para o MVP.
No registry, deve haver uma alternativa documentada para UIP com prêmio de risco AR(1) puro, caso a réplica do SAMBA clássico exija essa forma.
```

### 5.6 Política fiscal

A regra fiscal deve ser explícita.

Baseline provisório:

```text
sp_target_t =
rho_sp_target * sp_target_{t-1}
+ (1 - rho_sp_target) * [sp_ss + phi_b * (b_t - b_ss) + phi_y_sp * y_gap_t]
+ eps_sp_target_t
```

Dívida:

```text
b_{t+1} = função de b_t, r_t, crescimento nominal do PIB e resultado primário.
```

Decisões:

```text
- sp_target é variável separada de sp realizado.
- b é dívida/PIB.
- phi_b > 0 é condição de estabilização fiscal em torno do steady state.
- regimes fiscais 2016/2023 não entram no MVP; entram como dummies/regime switches apenas em extensões.
```

### 5.7 Preços administrados

Processo mínimo:

```text
pi_a_t =
rho_a * pi_a_{t-1}
+ (1 - rho_a) * [alpha_a_target * pi_target_t + alpha_a_fx * Δq_t + alpha_a_m * pi_m_t]
+ eps_admin_t
```

Decisão:

```text
- pi_a não é apenas “choque genérico”.
- pass-through cambial e/ou preço de importados deve ser testável.
- composição e quebras de administrados devem ser documentadas no data dictionary.
```

---

## 6. Arquitetura do repositório

```text
samba-dsge-br/
│
├── README.md
├── pyproject.toml
├── requirements.txt
├── Makefile
├── .gitignore
│
├── config/
│   ├── sample.yaml
│   ├── classic_mvp.yaml
│   ├── classic_estimation.yaml
│   ├── redux_smc.yaml
│   └── sovereign_scenarios.yaml
│
├── models/
│   └── registry.json
│
├── docs/
│   ├── 00_project_spec.md
│   ├── 00b_modeling_decisions.md
│   ├── 01_equation_registry.md
│   ├── 02_data_dictionary.md
│   ├── 03_calibration_notes.md
│   ├── 04_estimation_strategy.md
│   ├── 05_replication_targets.md
│   ├── 06_model_validation.md
│   └── 07_sovereign_extension_spec.md
│
├── data/
│   ├── raw/
│   │   └── YYYY-MM-DD/
│   ├── interim/
│   ├── clean/
│   ├── observables/
│   ├── vintages/
│   └── metadata/
│
├── src/
│   ├── data_pipeline/
│   ├── diagnostics/
│   ├── plotting/
│   ├── orchestration/
│   └── utils/
│
├── model/
│   ├── samba_classic/
│   │   ├── samba_classic.mod
│   │   ├── steady_state.m
│   │   ├── calibration.m
│   │   ├── priors.inc
│   │   ├── observables.inc
│   │   └── shocks.inc
│   │
│   ├── samba_redux/
│   │   ├── samba_redux.mod
│   │   ├── steady_state.m
│   │   ├── foreign_var/
│   │   ├── smc/
│   │   └── observables.inc
│   │
│   └── sovereign_extension/
│       ├── samba_sov.mod
│       ├── fiscal_rule.inc
│       ├── risk_premium.inc
│       └── scenarios/
│
├── outputs/
│   ├── schema/
│   ├── irfs/
│   ├── moments/
│   ├── posterior/
│   ├── variance_decomposition/
│   ├── historical_decomposition/
│   ├── forecasts/
│   ├── backtesting/
│   ├── identification/
│   └── reports/
│
└── tests/
    ├── test_data_transformations.py
    ├── test_observables.py
    ├── test_calibration.py
    ├── test_model_outputs.py
    ├── test_econometric.py
    ├── test_irf_restrictions.py
    └── test_replication_targets.py
```

---

## 7. Registry de modelos

Arquivo:

```text
models/registry.json
```

Exemplo:

```json
{
  "samba_classic_mvp_v0": {
    "model_file": "model/samba_classic/samba_classic.mod",
    "calibration_file": "model/samba_classic/calibration.m",
    "steady_state_file": "model/samba_classic/steady_state.m",
    "observables_file": "model/samba_classic/observables.inc",
    "priors_file": null,
    "data_file": "data/observables/classic_mvp_2003Q1_2019Q4.csv",
    "sample_config": "config/sample.yaml",
    "estimation_config": null,
    "status": "calibrated_mvp",
    "equation_registry_version": "classic_registry_v0.1"
  }
}
```

---

## 8. Data dictionary

Arquivo obrigatório:

```text
docs/02_data_dictionary.md
```

Colunas mínimas:

```text
observable_id
model_var
description
source
source_id
native_frequency
target_frequency
unit
base_year
seasonal_adjustment_method
transformation
revision_policy
last_revision_date
vintage_date
sample_start
sample_end
missing_value_policy
measurement_equation_id
notes
```

Exemplo:

```text
selic_policy_rate
r
Taxa Selic/meta ou over, conforme decisão de equação de medida
BCB/SGS
[code_to_confirm]
monthly/daily
quarterly
annualized percent
not_applicable
quarterly_average_or_effective_rate
demeaned_or_deviation_from_ss
final_revised_for_mvp
YYYY-MM-DD
YYYY-MM-DD
2003Q1
2019Q4
no_interpolation_without_flag
MEAS-R-001
Escolha entre meta e over precisa estar fixada antes da estimação.
```

Regra:

```text
Nenhuma fonte pode ser descrita apenas como “BCB”, “IBGE” ou “externa”.
Toda fonte precisa de código, tabela, URL ou identificador reproduzível.
```

---

## 9. Variáveis endógenas e estados

A lista abaixo é provisória até o equation registry fechar.

### 9.1 Atividade e demanda

```text
y          PIB real
c          consumo privado total
c_d        consumo de bens domésticos
c_m        consumo de importados, fase Redux
i          investimento
i_d        investimento em bens domésticos
i_m        investimento em bens importados, se necessário
g          consumo do governo
x          exportações
m          importações
m_int      importações como insumo intermediário
nx         exportações líquidas
abs        absorção doméstica
```

### 9.2 Produção e fatores

```text
k          capital
q_k        Tobin's Q / preço relativo do capital
n          emprego/horas
u          desemprego, fase Redux
lfp        participação, fase Redux
w          salário real
wn         salário nominal
mc         custo marginal real
lambda     utilidade marginal / multiplicador da restrição orçamentária
tfp        produtividade
y_pot      produto potencial ou componente tendencial, se usado
y_gap      hiato do produto
```

### 9.3 Preços

```text
pi         inflação cheia
pi_f       inflação de livres
pi_a       inflação de administrados/monitorados
pi_m       inflação de importados
pi_x       inflação de exportados
pi_target  meta de inflação
p_rel_a    preço relativo de administrados
p_rel_m    preço relativo de importados
```

### 9.4 Política monetária e fiscal

```text
r          taxa nominal doméstica
rr         taxa real ex-ante
b          dívida pública/PIB
sp         resultado primário/PIB
sp_target  meta de resultado primário/PIB
tau        tributação
transfers  transferências
```

### 9.5 Setor externo

```text
q          câmbio real
s          câmbio nominal, se necessário
nfa        posição externa líquida
risk       prêmio de risco doméstico
risk_global aversão global ao risco, fase Redux/VAR externo
y_star     produto externo
r_star     juros externos
pi_star    inflação externa
comm       commodities
tot        termos de troca
```

---

## 10. Choques

### 10.1 Choques estruturais mínimos

```text
eps_monetary
eps_pi_target
eps_fiscal_g
eps_sp_target
eps_tax
eps_tfp
eps_pref
eps_investment
eps_price_free
eps_price_admin
eps_wage
eps_import_price
eps_risk
eps_foreign_y
eps_foreign_r
eps_foreign_pi
eps_commodity
```

### 10.2 Erros de mensuração

Permitidos, mas documentados:

```text
me_y
me_c
me_i
me_g
me_x
me_m
me_pi
me_r
me_q
me_w
me_gap
```

Regra:

```text
Erro de mensuração não pode ser usado como “lixeira”.
Cada erro deve ter justificativa, limite de volatilidade e equação de medida.
```

---

## 11. Equation Registry

Arquivo:

```text
docs/01_equation_registry.md
```

Cada equação deve ter versão semântica:

```markdown
## EQ-MON-001-v1 — Regra de Taylor forward-looking

Bloco: Política monetária

Status:
- draft / validated / deprecated

Equação:
...

Forma log-linear:
...

Variáveis endógenas:
- r
- y_gap
- pi

Variáveis exógenas:
- pi_target

Choques:
- eps_monetary

Parâmetros:
- rho_r
- phi_pi
- phi_y

Fonte:
- SAMBA clássico / Redux / literatura auxiliar

Implementação:
- model/samba_classic/samba_classic.mod

Testes:
- BK conditions
- sinal da IRF
- magnitude da IRF
- equação de medida associada
```

Categorias:

```text
HH
FIRM
AGG
MON
FISC
EXT
LAB
MEAS
SHOCK
TREND
```

---

## 12. Pipeline de dados

### 12.1 Estados

```text
raw -> interim -> clean -> observables -> model_input
```

### 12.2 Regras

```text
1. Nenhuma transformação manual fora do código.
2. Toda série tem metadata.
3. Toda transformação tem teste unitário.
4. Toda amostra é versionada.
5. Toda quebra de série é documentada.
6. Toda interpolação é sinalizada.
7. Dados mensais convertidos para trimestrais têm regra fixa.
8. raw snapshots são salvos por data de coleta.
9. final-revised e real-time não são misturados.
```

### 12.3 Conversões trimestrais

```text
Inflação:
- composição acumulada ou log-diferença do índice, não média simples de inflação mensal.

Juros:
- média trimestral ou taxa efetiva trimestral, escolhida pela equação de medida.

Câmbio:
- média trimestral para baseline; fim de período apenas em robustez.

Expectativas:
- média trimestral ou fim de trimestre, definido antes da estimação.

CDS/prêmio de risco:
- média trimestral.

Atividade:
- séries reais dessazonalizadas quando apropriado.
```

---

## 13. Observáveis

### 13.1 MVP calibrado

O MVP calibrado pode rodar sem `varobs`, mas o pipeline deve gerar a base mínima:

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

### 13.2 Primeira estimação Bayesiana

A primeira estimação deve começar com um subconjunto menor do que o dataset total:

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

### 13.3 Redux

A fase Redux expande para o conjunto documentado de variáveis:

```text
- preços;
- atividade;
- mercado de trabalho;
- política fiscal;
- política monetária;
- setor externo;
- hiato do produto;
- inflação-meta;
- commodities.
```

---

## 14. Estimação

### 14.1 Ordem obrigatória

```text
1. Modelo calibrado resolve.
2. Steady state fecha.
3. BK conditions satisfeitas.
4. IRFs básicas plausíveis.
5. Likelihood finito na calibração.
6. Identificação local.
7. Priors revisados.
8. Modo posterior.
9. MH piloto.
10. MH completo.
11. posterior IRFs.
12. decomposição de variância.
13. decomposição histórica.
14. backtesting.
```

### 14.2 Priors

Arquivo:

```text
model/samba_classic/priors.inc
docs/04_estimation_strategy.md
```

Tabela obrigatória:

```text
parameter
block
description
prior_distribution
prior_mean
prior_std
bounds
source
rationale
estimated_in_phase
```

Regra:

```text
Não usar apenas templates genéricos.
Cada prior relevante deve ter fonte ou justificativa macroeconômica.
```

Priors iniciais por tipo:

```text
Parâmetros [0,1]:
- Beta.

Desvios-padrão:
- Inverse Gamma / Gamma.

Elasticidades positivas:
- Gamma / Lognormal.

Resposta de política:
- Gamma ou Normal truncada.

Parâmetros fiscais:
- priors conservadores, com restrições de estabilidade.
```

### 14.3 Identificação local

Sprint obrigatória:

```text
Sprint 3.5 — Identification analysis
```

Outputs:

```text
outputs/identification/iskrev_report.md
outputs/identification/komunjer_ng_report.md
outputs/identification/weakly_identified_parameters.csv
```

Critério:

```text
Parâmetro fracamente identificado não entra no MH completo sem:
1. prior mais informativo;
2. calibração fixa;
3. reparametrização;
4. redução do conjunto estimado.
```

### 14.4 Metropolis-Hastings

Config inicial:

```yaml
mh:
  pilot:
    chains: 4
    draws_per_chain: 50000
    burn_in: 0.5
    target_acceptance_band: [0.20, 0.35]
  full:
    chains: 4
    draws_per_chain: 250000
    burn_in: 0.5
    target_acceptance_band: [0.20, 0.35]
    run_only_if_pilot_passes: true
```

Critérios:

```text
1. R-hat < 1.1 nos principais parâmetros.
2. modo posterior estável.
3. Hessiana utilizável no modo, quando aplicável.
4. posterior não colapsa no prior.
5. likelihood finito.
6. marginal likelihood comparável entre especificações.
```

### 14.5 SMC para Redux

A fase Redux deve documentar:

```text
1. número de partículas/draws;
2. schedule de tempering;
3. critério de ESS;
4. número de mutações MH por estágio;
5. paralelização;
6. seeds;
7. requisitos computacionais.
```

Não fixar o número de partículas no spec principal antes de benchmark computacional.

---

## 15. Implementação computacional

### 15.1 Stack

```text
Dynare + MATLAB/Octave
Python para ETL, validação, relatórios e gráficos
Make como entrypoint
Snakemake ou Prefect opcional para orquestração maior
```

### 15.2 Versionamento

Arquivo:

```text
config/environment.yaml
```

Campos:

```yaml
dynare_version: "to_pin"
matlab_version: "to_pin_if_used"
octave_version: "to_pin_if_used"
python_version: "to_pin"
os: "to_pin"
random_seed:
  stoch_simul: 12345
  mh: 12345
  bootstrap: 12345
```

Regra:

```text
- A versão exata de Dynare deve ser pinada antes da estimação.
- Não hard-code versão sem verificar compatibilidade local.
- CI roda todos os testes Python.
- Dynare smoke tests entram no CI apenas se Octave/Dynare estiverem disponíveis no runner.
- MATLAB completo pode ser validado localmente com snapshots de outputs versionados.
```

### 15.3 Steady state

Decisão:

```text
- SAMBA clássico: preferir steady state analítico.
- Redux: documentar quais blocos exigem solução numérica.
- Toda derivação entra em docs/03_calibration_notes.md.
```

---

## 16. Testes

### 16.1 Testes de dados

```python
def test_no_duplicate_dates(): ...
def test_quarterly_frequency(): ...
def test_no_unexpected_missing_values(): ...
def test_inflation_aggregation(): ...
def test_observable_units(): ...
def test_source_ids_are_pinned(): ...
def test_final_revised_not_mixed_with_realtime(): ...
```

### 16.2 Testes de modelo

```python
def test_dynare_outputs_exist(): ...
def test_steady_state_residuals_below_tolerance(): ...
def test_bk_conditions_satisfied(): ...
def test_no_unit_roots_unless_declared(): ...
def test_forward_looking_variable_count_matches_bk(): ...
def test_variance_decomposition_sums_to_one(): ...
```

### 16.3 Testes econométricos

```python
def test_likelihood_is_finite_at_calibration(): ...
def test_hessian_positive_definite_at_mode_if_required(): ...
def test_posterior_chains_pass_rhat_threshold(): ...
def test_marginal_likelihood_stable_across_chains(): ...
def test_measurement_errors_within_allowed_volatility(): ...
```

### 16.4 Testes econômicos

```python
def test_monetary_shock_raises_policy_rate_on_impact(): ...
def test_monetary_shock_reduces_output_with_lag(): ...
def test_monetary_shock_reduces_inflation_with_lag(): ...
def test_risk_premium_shock_depreciates_currency(): ...
def test_fiscal_expansion_raises_demand_short_run(): ...
```

Critérios de IRF devem incluir:

```text
1. sinal;
2. magnitude aproximada;
3. timing do pico;
4. retorno gradual ao steady state;
5. comparação qualitativa com literatura.
```

---

## 17. Backtesting

Backtesting é obrigatório na Fase 2.

Configuração inicial:

```yaml
backtesting:
  scheme: "expanding_window_or_rolling_window"
  horizons: [1, 4, 8, 12]
  metrics:
    - RMSE
    - MAE
    - CRPS
  benchmarks:
    - AR1
    - VAR
    - BVAR_Minnesota
    - Focus_if_available
  variables:
    - inflation
    - policy_rate
    - output_growth
    - exchange_rate
```

Outputs:

```text
outputs/backtesting/forecast_errors.csv
outputs/backtesting/benchmark_comparison.csv
outputs/backtesting/backtesting_report.md
```

---

## 18. Critérios de aceite

### 18.1 MVP calibrado

Aceito se:

```text
1. docs/00b_modeling_decisions.md existe e está completo.
2. equation registry mínimo existe.
3. data dictionary mínimo existe.
4. modelo Dynare roda sem erro.
5. steady state fecha.
6. BK conditions são satisfeitas.
7. 5 IRFs-chave têm sinal, timing e magnitude plausíveis.
8. outputs são gerados em schema padronizado.
9. testes de dados e modelo passam.
10. execução é reproduzível com seed definido.
```

### 18.2 Estimação Bayesiana

Aceita se:

```text
1. likelihood finito na calibração.
2. identificação local foi rodada antes do MH.
3. parâmetros fracamente identificados foram tratados.
4. priors documentados por fonte/racional.
5. MH piloto passa critérios mínimos.
6. MH completo tem R-hat < 1.1 para parâmetros-chave.
7. posterior IRFs são coerentes.
8. decomposição de variância é interpretável.
9. decomposição histórica não atribui eventos óbvios a choques absurdos.
10. backtesting compara o modelo com benchmarks.
```

### 18.3 Redux

Aceito se:

```text
1. mercado de trabalho entra com desemprego e participação.
2. consumo importado entra no bundle final.
3. VAR externo está acoplado e documentado.
4. SMC tem especificação computacional completa.
5. observáveis Redux estão documentados.
6. histórico 2001Q4-2019Q4 é replicável qualitativamente.
```

---

## 19. Roadmap revisado

### Sprint -1 — Decisões macroeconométricas

Duração: 1 semana.

Entregas:

```text
docs/00b_modeling_decisions.md
config/sample.yaml
config/environment.yaml
```

### Sprint 0 — Setup de engenharia

Duração: 1 semana.

Entregas:

```text
estrutura de repo
Makefile
config/
models/registry.json
outputs/schema/
testes Python básicos
```

### Sprint 1a — Dados mínimos

Duração: 1 semana.

Entregas:

```text
PIB
IPCA
Selic
câmbio real
data dictionary stub
```

### Sprint 2 — Equation registry

Duração: 4 a 6 semanas.

Entregas:

```text
40-60 equações registradas
variáveis derivadas do registry
choques derivados do registry
equações de medida preliminares
```

### Sprint 1b — Dados expandidos

Duração: 2 semanas.

Entregas:

```text
observáveis alinhados ao registry
source_id pinado
transformações testadas
```

### Sprint 3 — Modelo clássico calibrado

Duração: 6 a 8 semanas.

Entregas:

```text
samba_classic.mod
steady state analítico
BK check
IRFs
relatório MVP
```

### Sprint 3.5 — Identificação local

Duração: 1 semana.

Entregas:

```text
identification report
lista de parâmetros estimáveis
lista de parâmetros fixos
```

### Sprint 4 — Estimação Bayesiana

Duração: 6 a 10 semanas.

Entregas:

```text
priors.inc
observables.inc
MH piloto
MH completo
posterior IRFs
diagnóstico
```

### Sprint 5 — Validação e backtesting

Duração: 3 a 4 semanas.

Entregas:

```text
momentos
decomposição de variância
decomposição histórica
backtesting
relatório de validação
```

### Sprint 6 — Redux

Duração: 16 a 24 semanas.

Subfases:

```text
6a mercado de trabalho
6b consumo importado
6c VAR externo
6d SMC
6e validação Redux
```

### Sprint 7 — Extensão soberana

Duração: 8 a 12 semanas, após spec própria.

Entregas:

```text
docs/07_sovereign_extension_spec.md
risk premium fiscal
cenários soberanos
dominância fiscal escolhida
```

---

## 20. Backlog priorizado

### P0

```text
docs/00b_modeling_decisions.md
config/sample.yaml
models/registry.json
equation registry
data dictionary
modelo calibrado
steady state
BK
IRFs
```

### P1

```text
identificação local
priors brasileiros
equações de medida
MH piloto
testes econométricos
```

### P2

```text
MH completo
posterior IRFs
decomposição histórica
backtesting
```

### P3

```text
Redux
SMC
VAR externo
mercado de trabalho
consumo importado
```

### P4

```text
extensão soberana
dashboard
real-time vintages
cenários operacionais
```

---

## 21. Riscos principais

### 21.1 Mapeamento incorreto dos observáveis

Mitigação:

```text
equações de medida versionadas
data dictionary com source_id
testes de unidade
comparação de momentos
```

### 21.2 Identificação fraca

Mitigação:

```text
Sprint 3.5
priors informativos
redução do conjunto estimado
calibração de parâmetros fracos
```

### 21.3 Singularidade estocástica

Mitigação:

```text
começar com poucos observáveis
adicionar measurement errors justificados
checar rank e likelihood
expandir observáveis gradualmente
```

### 21.4 Ambição excessiva

Mitigação:

```text
Redux e Sovereign fora do MVP
roadmap alongado
gates técnicos entre fases
```

### 21.5 Fragilidade computacional

Mitigação:

```text
versões pinadas
seeds fixos
outputs schema
steady state analítico
CI limitado ao que é reprodutível
```

---

## 22. Definição objetiva do MVP v2

O MVP estará completo quando:

```text
1. as decisões macroeconométricas estão fechadas;
2. o equation registry mínimo está versionado;
3. as variáveis derivam do registry;
4. o pipeline gera observáveis reproduzíveis;
5. o modelo calibrado resolve;
6. o steady state fecha;
7. BK conditions são satisfeitas;
8. IRFs-chave passam testes de sinal, magnitude e timing;
9. outputs seguem schema;
10. o projeto está pronto para identificação local e estimação.
```

A estimação só começa depois disso.


---

# 4. Ordem obrigatória de execução

A implementação deve obedecer à seguinte ordem. Qualquer tentativa de inverter essa sequência deve ser tratada como risco técnico:

```text
1. docs/00b_modeling_decisions.md
2. docs/01_equation_registry.md
3. docs/02_data_dictionary.md
4. config/sample.yaml
5. config/environment.yaml
6. models/registry.json
7. pipeline mínimo de dados
8. model/samba_classic/samba_classic.mod
9. steady_state.m / calibration.m / shocks.inc
10. checagem BK
11. IRFs calibradas
12. identificação local
13. priors.inc
14. estimação Bayesiana piloto
15. estimação Bayesiana completa
16. validação/backtesting
17. Redux
18. extensão soberana
```

---

# 5. Checklist de prontidão para implementação

Antes de pedir ao Codex ou a qualquer desenvolvedor para começar a escrever código, verificar:

```text
[ ] O documento docs/00b_modeling_decisions.md foi escrito.
[ ] A amostra do MVP está definida.
[ ] O tratamento de COVID está definido.
[ ] O tratamento de tendência está definido.
[ ] A regra de Taylor está especificada.
[ ] pi_target está especificado.
[ ] A UIP/prêmio de risco está especificada.
[ ] A regra fiscal está especificada.
[ ] O processo de preços administrados está especificado.
[ ] A lista provisória de variáveis foi validada contra o equation registry.
[ ] O data dictionary exige source_id reproduzível.
[ ] Não há source_id inventado.
[ ] Dados final-revised e real-time estão separados.
[ ] O MVP não inclui Redux.
[ ] O MVP não inclui extensão soberana.
[ ] A estimação não começa antes da identificação local.
[ ] IRFs têm critério de sinal, timing, magnitude e benchmark.
[ ] Measurement errors têm justificativa e limite de volatilidade.
[ ] Dynare/MATLAB/Octave serão versionados antes da estimação.
```

---

# 6. Fonte única de verdade

Este arquivo standalone deve ser tratado como a fonte canônica do projeto até que seja substituído por uma nova versão consolidada.

Arquivos operacionais derivados, como prompts para Codex ou planos de implementação, devem referenciar este documento como fonte superior.

Ordem de precedência recomendada depois deste consolidation:

```text
1. SPEC Standalone Consolidado — este documento;
2. docs/00b_modeling_decisions.md;
3. docs/01_equation_registry.md;
4. docs/02_data_dictionary.md;
5. models/registry.json;
6. arquivos .mod/.m/.inc;
7. relatórios e outputs.
```

---
