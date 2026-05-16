# Gate 0 Review Packet — samba-dsge-br

**Modo executado:** A — Gate 0 Review Packet  
**Data:** 2026-05-16  
**Branch:** `codex/modeling-decisions-baseline`  
**PR:** `#1 — [codex] Propose Gate 0 modeling decisions`  
**Fonte canônica:** `samba_dsge_br_spec_standalone_consolidado.md`

---

## Gate 0 simplified check — 2026-05-16

Resultado: Gate 0 nao aprovado.

Falha objetiva: `EXT-001` especifica UIP/premio de risco e `risk_t`, mas nao declara uma convencao clara de sinal para `q`/cambio real.

Proximo passo: explicitar em `docs/00b_modeling_decisions.md` se aumento de `q` representa depreciacao ou apreciacao real, e como isso entra na UIP e nas IRFs.

Nenhuma decisao foi aprovada nesta revisao. Nenhum config, dado, pipeline, teste ou `.mod` foi criado.

---

## 1. Executive summary

- O Gate 0 está aprovado? **Não.**
- Decisões que bloqueiam avanço: `SAMPLE-001`, `TREND-001`, `MON-001`, `TARGET-001`, `EXT-001`, `FISC-001`, `ADMIN-001`, `OBS-001`.
- Motivo formal: todas as decisões permanecem com `decision_status: proposed`, `approved_by` vazio e `approval_date` vazio.
- Schema: corrigido; todas as decisões existentes agora contêm `blocking_status: blocking_for_mvp`.
- Próximo passo recomendado: revisão humana de `docs/00b_modeling_decisions.md`, aplicação dos ajustes sugeridos abaixo e nova execução com autorização explícita preenchida para Modo B.

Nenhum config, dado, `.mod`, pipeline, teste, equation registry ou data dictionary deve ser criado antes da aprovação humana explícita do Gate 0.

---

## 2. Arquivos revisados

| Arquivo / contexto | Existe? | Observação |
|---|---:|---|
| `samba_dsge_br_spec_standalone_consolidado.md` | Sim | Fonte canônica do projeto; lido para escopo, decisões macro, observáveis, ordem e gates. |
| `docs/08_implementation_plan.md` | Sim | Plano operacional v2; lido para regras de Gate 0, Modo PR e bloqueios. |
| `docs/00b_modeling_decisions.md` | Sim | Documento proposto de decisões Gate 0; lido integralmente. |
| `README.md` | Sim | Confirma ordem de trabalho, convenções `models/` vs `model/` e MVP. |
| `CONTRIBUTING.md` | Sim | Confirma que Codex não aprova decisões macro e que Gate 0 exige aprovação humana. |
| `git status` | Disponível | Branch atual limpa antes desta alteração: `codex/modeling-decisions-baseline`. |
| PR atual | Disponível | PR `#1`, draft, branch `codex/modeling-decisions-baseline` contra `main`. |

Arquivos esperados mas ainda ausentes neste estágio:

| Arquivo | Status correto agora |
|---|---|
| `config/sample.yaml` | Ausente; só deve ser criado no Modo B após aprovação humana. |
| `config/environment.yaml` | Ausente; só deve ser criado no Modo B após aprovação humana. |
| `docs/runtime_verification.md` | Ausente; só deve ser criado no Modo B após aprovação humana. |
| `docs/01_equation_registry.md` | Ausente; ainda proibido nesta execução. |
| `docs/02_data_dictionary.md` | Ausente; ainda proibido nesta execução. |
| `model/` | Ausente; correto. |
| `data/` | Ausente; correto. |
| `src/data_pipeline/` | Ausente; correto. |
| `tests/` | Ausente; correto. |

---

## 3. Schema check de `docs/00b_modeling_decisions.md`

Campos exigidos:

```text
decision_id
decision_title
decision_status
proposed_by
approved_by
approval_date
alternatives_rejected
rationale
downstream_files
blocking_status
```

| decision_id | decision_id | decision_title | decision_status | proposed_by | approved_by | approval_date | alternatives_rejected | rationale | downstream_files | blocking_status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `SAMPLE-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `TREND-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `MON-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `TARGET-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `EXT-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `FISC-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `ADMIN-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |
| `OBS-001` | Sim | Sim | Sim | Sim | Sim, vazio | Sim, vazio | Sim | Sim | Sim | Sim, `blocking_for_mvp` |

Conclusão do schema check:

```text
Schema corrigido para as decisões existentes: todas contêm `blocking_status`.
Gate 0 continua bloqueado porque `decision_status` permanece proposed e os campos de aprovação humana estão vazios.
```

---

## 4. Decisões encontradas

| decision_id | decision_title | decision_status | blocking_status | approved_by | approval_date | pode avançar? | observação |
|---|---|---|---|---|---|---:|---|
| `SAMPLE-001` | Amostra, COVID e política de revisão de dados | proposed | blocking_for_mvp | vazio | vazio | Não | Formalmente bloqueada por falta de aprovação; conteúdo é majoritariamente alinhado ao SPEC. |
| `TREND-001` | Tratamento de tendência para SAMBA clássico | proposed | blocking_for_mvp | vazio | vazio | Não | Alinhada ao SPEC, mas ainda precisa fixar onde transformações serão decididas por série. |
| `MON-001` | Regra de Taylor forward-looking com meta explícita | proposed | blocking_for_mvp | vazio | vazio | Não | Regra está especificada, mas `y_gap_t` ainda está ambíguo como variável/model measure vs proxy observável. |
| `TARGET-001` | Tratamento de `pi_target_t` no MVP clássico | proposed | blocking_for_mvp | vazio | vazio | Não | Deixa aberta escolha entre série exógena e `varexo_det`, listada como pendência bloqueante no plano. |
| `EXT-001` | UIP com fechamento NFA/debt-elastic e prêmio de risco | proposed | blocking_for_mvp | vazio | vazio | Não | Forma de UIP está bem especificada; proxy/fonte do risco pode ficar para Gate 1b/estimação. |
| `FISC-001` | Regra fiscal com `sp_target` e feedback sobre dívida/PIB | proposed | blocking_for_mvp | vazio | vazio | Não | Alinhada ao SPEC; o status de bloqueio agora está explícito. |
| `ADMIN-001` | Processo para inflação de preços administrados | proposed | blocking_for_mvp | vazio | vazio | Não | Fórmula inclui canais, mas critério ainda pede confirmar quais entram no MVP. |
| `OBS-001` | Conjunto inicial de observáveis do MVP e primeira estimação | proposed | blocking_for_mvp | vazio | vazio | Não | Lista de observáveis está alinhada; falta lista explícita de variáveis estruturais mínimas do Gate 0. |

---

## 5. Revisão macroeconômica adversarial

### 5.1 Amostra

Problema: a proposta está alinhada ao SPEC e agora tem `blocking_status`, mas ainda não tem aprovação humana.  
Por que importa: amostra define todos os datasets, calibração, estimação futura e comparabilidade.  
Correção proposta: manter `blocking_status: blocking_for_mvp` e `classic_mvp` em 2003Q1-2019Q4, com Redux explicitamente fora do MVP.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.2 Tratamento de COVID

Problema: a exclusão de COVID está correta, mas ainda precisa ser aprovada por humano e vinculada a baseline linear-Gaussiano.  
Por que importa: COVID pode quebrar o filtro, distorcer likelihood e contaminar estimação.  
Correção proposta: manter `covid_treatment: exclude` no MVP e registrar que dummies/outlier-robust likelihood ficam fora do MVP.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.3 Final-revised vs real-time

Problema: a proposta separa final-revised e real-time, mas permanece proposed.  
Por que importa: misturar vintages invalida reprodutibilidade e backtesting.  
Correção proposta: aprovar `final_revised` para MVP acadêmico e manter `real_time_vintage` como `out_of_mvp`.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.4 Tratamento de tendência

Problema: a decisão confirma log-linear/steady state determinístico, mas não fixa ainda a regra operacional por observable real.  
Por que importa: crescimento, log-desvio, deflação, sazonalidade e medidas de hiato precisam ser compatíveis com equações de medida.  
Correção proposta: manter a decisão macro no Gate 0 e exigir que `docs/02_data_dictionary.md` detalhe transformação por série antes de Gate 1b.  
Severidade: Média.  
Bloqueia Gate 0? Sim, por falta de aprovação; o detalhamento por série pode ficar para Gate 1a/1b.

### 5.5 Regra de Taylor

Problema: a equação forward-looking está especificada, mas `y_gap_t` ainda aparece como "variável ou proxy observável documentada".  
Por que importa: regra de Taylor, measurement equations e identificação dependem do status de `y_gap_t`.  
Correção proposta: antes de aprovação, escolher uma formulação de Gate 0: `y_gap_t` como variável estrutural do modelo com measurement equation futura, ou como proxy observável documentada. Se a escolha ficar adiada, registrar explicitamente como bloqueante para Gate 2b.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.6 Inflação-meta / `pi_target_t`

Problema: `TARGET-001` deixa aberta a escolha entre série exógena e `varexo_det`. O próprio plano lista o tratamento exato de `pi_target_t` como bloqueante para MVP.  
Por que importa: muda a implementação Dynare, o registry e a equação de medida da regra monetária.  
Correção proposta: revisar antes de aprovação para fixar uma opção de MVP, preferencialmente "série exógena/determinística documentada; `eps_pi_target` desligado no MVP calibrado", ou declarar explicitamente a decisão como `deferred` e bloqueante para `.mod`.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.7 UIP / prêmio de risco

Problema: a UIP está suficientemente especificada para proposta, mas o texto pede confirmar proxy/fonte futura de prêmio de risco.  
Por que importa: a fonte de prêmio de risco é assunto de data dictionary/estimação; tentar resolver agora pode induzir `source_id` inventado.  
Correção proposta: aprovar a forma estrutural NFA/debt-elastic se o humano concordar, e mover proxy/fonte de risco para Gate 1b ou estratégia de estimação sem inventar fonte.  
Severidade: Média.  
Bloqueia Gate 0? Sim, formalmente por falta de aprovação; tecnicamente a proxy/fonte não precisa bloquear Gate 0.

### 5.8 Regra fiscal

Problema: a regra está alinhada ao SPEC, mas a equação de dívida ainda está descrita como "função de" em vez de identidade operacional.  
Por que importa: a identidade de dívida/PIB afetará steady state, BK e canal fiscal.  
Correção proposta: para Gate 0, aprovar separação `sp_target` vs `sp`, `b` como dívida/PIB e feedback `phi_b > 0`; exigir identity precisa no equation registry antes de `.mod`.  
Severidade: Média.  
Bloqueia Gate 0? Sim, por falta de aprovação; a identidade detalhada pode ficar para Gate 2b se marcada.

### 5.9 Preços administrados

Problema: a fórmula inclui meta, câmbio e preço importado, mas a seção de aprovação pergunta "quais canais entram no MVP".  
Por que importa: canais diferentes mudam parâmetros, choques, dados e testes de IRF.  
Correção proposta: revisar antes de aprovação para fixar os canais do MVP. Se todos os três canais forem mantidos, escrever isso explicitamente como decisão proposta.  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.10 Observáveis iniciais

Problema: lista de observáveis está alinhada ao SPEC, mas ainda não define fonte nem measurement equation, corretamente adiadas.  
Por que importa: observable set define Gate 1b e singularidade estocástica futura.  
Correção proposta: aprovar lista mínima como escopo de pipeline, sem `source_id`; manter fontes para Gate 1b e measurement equations finais para Gate 2b após dictionary.  
Severidade: Média.  
Bloqueia Gate 0? Sim, por falta de aprovação; fontes não bloqueiam Gate 0.

### 5.11 Variáveis estruturais mínimas

Problema: `docs/00b_modeling_decisions.md` não traz uma decisão ou tabela explícita consolidando variáveis estruturais mínimas como `mc`, `q_k`, `wn`, `lambda`, `y_gap`, `y_pot`, `nfa`, `m_int`, `pi_target`.  
Por que importa: o SPEC incorporou essas variáveis como correção de risco; sem lista explícita, o equation registry pode omitir estados/controles necessários.  
Correção proposta: adicionar uma decisão `STRUCT-001` ou expandir `OBS-001` com uma lista "variáveis estruturais mínimas a carregar para o equation registry".  
Severidade: Alta.  
Bloqueia Gate 0? Sim.

### 5.12 Exclusão de Redux e soberano do MVP

Problema: a exclusão está presente em várias decisões, mas não aparece como decisão própria com status e bloqueio.  
Por que importa: evita que Redux, SMC, desemprego ou extensão soberana contaminem o MVP clássico.  
Correção proposta: adicionar `SCOPE-001` ou expandir `SAMPLE-001`/`OBS-001` para registrar explicitamente "Redux e soberano fora do MVP".  
Severidade: Média.  
Bloqueia Gate 0? Não, se a exclusão for mantida nas decisões existentes; recomendado deixar explícito antes de aprovação final.

---

## 6. Recomendação de aprovação

| decision_id | recomendação | motivo | alteração necessária antes de aprovação |
|---|---|---|---|
| `SAMPLE-001` | approve_after_human_review | Conteúdo alinhado ao SPEC para amostra, COVID e final-revised. | Humano preencher `approved_by` e `approval_date` se concordar. |
| `TREND-001` | approve_after_human_review | Alinhado ao SPEC; detalhamento por série pode ficar no data dictionary. | Explicitar que transformações por observable entram em Gate 1a/1b. |
| `MON-001` | revise_before_approval | `y_gap_t` ainda está operacionalmente ambíguo. | Fixar status de `y_gap_t` para MVP ou marcar como bloqueante para Gate 2b antes de `.mod`. |
| `TARGET-001` | revise_before_approval | Escolha entre série exógena e `varexo_det` ainda está aberta. | Escolher tratamento do MVP ou marcar decisão como deferred bloqueante para `.mod`. |
| `EXT-001` | approve_after_human_review | Forma estrutural está bem definida e preserva alternativa AR(1). | Remover exigência de proxy/fonte do Gate 0 e empurrar para Gate 1b/estimação. |
| `FISC-001` | approve_after_human_review | Regra fiscal mínima está alinhada ao SPEC. | Explicitar que identidade completa de dívida entra no equation registry. |
| `ADMIN-001` | revise_before_approval | Canais do processo ainda precisam ser fixados. | Declarar se MVP usa meta + câmbio + importados, ou subconjunto específico. |
| `OBS-001` | revise_before_approval | Observáveis estão bons, mas faltam variáveis estruturais mínimas. | Adicionar lista estrutural mínima ou nova decisão `STRUCT-001`. |

Recomendação geral:

```text
Não aprovar Gate 0 no estado atual.
Preparar uma revisão pequena em docs/00b_modeling_decisions.md antes da aprovação humana.
```

---

## 7. Patch sugerido, se necessário

Não aplicado automaticamente.

### 7.1 Campo `blocking_status`

Já aplicado às decisões existentes:

```yaml
blocking_status: blocking_for_mvp
```

Categorias permitidas para decisões futuras:

```text
blocking_for_mvp
blocking_for_estimation
blocking_for_redux
blocking_for_sovereign
non_blocking
```

Se o humano optar por diferir uma decisão, manter `blocking_status` conforme o impacto real e registrar o diferimento em campo separado, sem transformar a decisão em aprovada.

### 7.2 Revisão sugerida para `MON-001`

Texto substituto sugerido para requisitos associados:

```text
Requisitos associados:
- `pi_target_t` entra explicitamente.
- Para o MVP, `y_gap_t` será tratado como variável estrutural do modelo, com measurement equation/proxy apenas no registry/data dictionary futuro.
- A definição de measurement equation de `y_gap_t` é bloqueante para Gate 2b, mas não altera a forma da regra monetária aprovada no Gate 0.
- A IRF de choque monetário deve exigir sinal, timing, magnitude e benchmark.
```

### 7.3 Revisão sugerida para `TARGET-001`

Texto substituto sugerido para proposta:

```text
Fase clássica:
- `pi_target_t` entra como série exógena/determinística documentada.
- A implementação Dynare preferida para o MVP será decidida antes da Fase 3 entre `varexo_det` e leitura via dados/observables, sem alterar a regra monetária aprovada.
- `eps_pi_target` fica desligado no MVP calibrado, salvo aprovação humana posterior.

Fase Redux:
- processo persistente de meta de inflação fica fora do MVP.
```

Se o revisor considerar a escolha `varexo_det` vs série exógena bloqueante para Gate 0, então `TARGET-001` deve continuar `proposed` até a escolha ser feita.

### 7.4 Revisão sugerida para `ADMIN-001`

Texto substituto sugerido:

```text
Para o MVP, manter os três canais no processo proposto:
- persistência de `pi_a`;
- componente de meta `pi_target_t`;
- pass-through cambial via `Δq_t`;
- preço de importados `pi_m_t`, se o registry confirmar variável e dado compatível.

Se `pi_m_t` não estiver disponível no Gate 1b, o canal de importados deve ser parametrizado/desligado explicitamente, sem substituir por measurement error.
```

### 7.5 Nova decisão sugerida `STRUCT-001`

Adicionar após `OBS-001`:

```yaml
decision_id: STRUCT-001
decision_title: Variáveis estruturais mínimas para o equation registry
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Permitir que variáveis estruturais sejam descobertas apenas durante a escrita do .mod."
  - "Omitir variáveis incorporadas pelo SPEC, como mc, q_k, wn, lambda, y_gap, y_pot, nfa, m_int e pi_target."
rationale: >
  O SPEC consolidado incorporou variáveis estruturais ausentes como correção técnica.
  O equation registry deve carregá-las explicitamente antes de qualquer implementação Dynare.
downstream_files:
  - docs/01_equation_registry.md
  - docs/03_calibration_notes.md
  - model/samba_classic/samba_classic.mod
```

Lista proposta:

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

### 7.6 Nova decisão sugerida `SCOPE-001`

Adicionar se o revisor quiser tornar a fronteira de escopo inequívoca:

```yaml
decision_id: SCOPE-001
decision_title: Escopo do MVP e exclusões explícitas
decision_status: proposed
proposed_by: Codex
approved_by:
approval_date:
blocking_status: blocking_for_mvp
alternatives_rejected:
  - "Incluir Redux no MVP."
  - "Incluir extensão soberana no MVP."
  - "Iniciar estimação completa antes de identificação local."
rationale: >
  O MVP deve entregar SAMBA clássico calibrado, log-linear, primeira ordem, com gates
  de dados, registry, steady state, BK e IRFs antes de estimação.
downstream_files:
  - docs/08_implementation_plan.md
  - docs/01_equation_registry.md
  - model/samba_classic/samba_classic.mod
```

---

## 8. Critério objetivo para passar Gate 0

Gate 0 passa somente se todos os itens forem verdadeiros:

1. Todas as decisões bloqueantes têm `decision_status: approved`, salvo decisões explicitamente `deferred` com `blocking_status` não bloqueante e fase futura definida.
2. Nenhuma decisão bloqueante permanece `proposed`.
3. Nenhuma decisão bloqueante permanece com `approved_by` vazio.
4. Nenhuma decisão bloqueante permanece com `approval_date` vazio.
5. Todas as decisões têm `blocking_status`.
6. O revisor humano consta no campo `approver` do bloco de aprovação.
7. O campo `approval_date` do bloco de aprovação está preenchido.
8. O campo `approved_decision_ids` do bloco de aprovação cobre as decisões bloqueantes ou registra diferimentos explícitos.
9. `TARGET-001` não deixa ambíguo o tratamento de `pi_target_t` sem marcar bloqueio posterior.
10. `MON-001` não deixa ambíguo o status operacional de `y_gap_t` sem marcar bloqueio posterior.
11. `ADMIN-001` define quais canais entram no MVP ou marca indisponibilidade condicionada a Gate 1b.
12. Variáveis estruturais mínimas do SPEC estão explicitamente listadas em `STRUCT-001` ou em decisão equivalente.
13. Redux e extensão soberana permanecem fora do MVP.
14. Nenhum `source_id`, código SGS, tabela SIDRA, URL ou versão de software foi inventado.

---

## 9. Próximo prompt recomendado

Como Gate 0 ainda não está aprovado:

1. Revisão humana deve ler `docs/00b_modeling_decisions.md` e este pacote.
2. Ajustar `docs/00b_modeling_decisions.md` conforme necessário, especialmente `blocking_status`, `TARGET-001`, `MON-001`, `ADMIN-001` e variáveis estruturais mínimas.
3. Preencher explicitamente:

```text
APROVACAO_GATE0:

approver: <nome humano>
approval_date: <YYYY-MM-DD>
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
rejected_decision_ids:
deferred_decision_ids:
notes:
```

4. Rodar nova execução em Modo B somente se a aprovação estiver explícita e suficiente.

---

## 10. Critérios de aceite do Modo A

- Não alterei `decision_status` para `approved`.
- Não criei configs.
- Não criei dados.
- Não criei model files.
- Não criei tests.
- Criei/atualizei apenas `docs/00c_gate0_review_packet.md`.

---

## 11. Autocrítica

| Pergunta | Resposta |
|---|---|
| Eu aprovei alguma decisão sem autorização humana explícita? | Não. |
| Eu criei config antes de Gate 0 aprovado? | Não. |
| Eu criei `.mod`, dados, pipeline ou testes indevidamente? | Não. |
| Eu inventei alguma fonte ou versão de software? | Não. |
| Eu mantive Redux e soberano fora do MVP? | Sim. |
| O próximo passo está claramente bloqueado ou desbloqueado? | Bloqueado até revisão humana explícita. |

---

## Bloco de aprovação humana — template

Para aprovar o Gate 0, preencher explicitamente:

```text
APROVACAO_GATE0:

approver:
approval_date:
approved_decision_ids:
rejected_decision_ids:
deferred_decision_ids:
notes:
```

Gate 0 só pode avançar se todas as decisões com `blocking_status: blocking_for_mvp` estiverem aprovadas ou explicitamente diferidas com justificativa compatível com o MVP.
