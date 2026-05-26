# Contributing

## Fluxo de trabalho

- Uma thread Codex deve corresponder a uma branch e a um PR logico.
- Use branches com prefixo `codex/`.
- Mantenha cada PR pequeno, auditavel e alinhado a uma tarefa WBS do plano.
- Nao misture mudancas de documentacao, pipeline, Dynare e estimacao no mesmo PR sem motivo explicito.

## Gates

- Codex pode propor decisoes macroeconometricas, mas nao pode aprova-las.
- Gate 0 exige aprovacao humana explicita.
- Gate 1b exige fontes core sem `TBD`.
- O `.mod` so deve ser criado apos Gate 0, Gate 1b, Gate 2b e verificacao de runtime.

## Dados e fontes

- Nao invente `source_id`.
- Se uma fonte nao estiver verificada, use `TBD-verify-in-task-<WBS-ID>`.
- Nao misture dados final-revised e real-time no mesmo experimento.

## Python

- `pyproject.toml` e a fonte de verdade para package, pytest e tooling.
- `requirements.txt` e arquivo de compatibilidade, nao fonte primaria.
- Nao instale dependencias em rede como parte de tarefas de bootstrap.
