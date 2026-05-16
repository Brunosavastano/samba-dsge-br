# samba-dsge-br

Replica publica, modular e auditavel do modelo SAMBA/DSGE para a economia brasileira.

## Fonte canonica

A fonte superior atual do projeto e:

```text
samba_dsge_br_spec_standalone_consolidado.md
```

O plano mestre de implementacao esta em:

```text
docs/08_implementation_plan.md
```

## Ordem de trabalho

1. Validar o SPEC consolidado.
2. Inicializar governanca Git/GitHub.
3. Propor decisoes macroeconometricas em `docs/00b_modeling_decisions.md`.
4. Obter aprovacao humana explicita para Gate 0.
5. Criar configs, registry, data dictionary e literature map.
6. Implementar o modelo Dynare somente depois de Gate 0, Gate 1b e Gate 2b.

## Convencoes

```text
models/ = metadata registry e versionamento.
model/  = arquivos executaveis Dynare/MATLAB/Octave.
```

`pyproject.toml` sera a fonte de verdade do ambiente Python quando o bootstrap tecnico for criado.

## Escopo do MVP

O MVP cobre SAMBA classico calibrado, log-linear e de primeira ordem. Redux e extensao soberana ficam fora do MVP.

