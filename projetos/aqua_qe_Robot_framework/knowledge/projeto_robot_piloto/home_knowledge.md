# Base de Conhecimento Home (MVP)

## Escopo

Modulo inicial para validar navegacao basica da Home.

## Cenarios alvo

1. Abrir Home com sucesso.
2. Validar elemento principal visivel.
3. Validar acesso rapido principal.

## Regras LKDF

- `test_suites/home/home.robot` chama keywords do scenarios.
- `src/scenarios/home/home_scenarios.resource` usa keywords do flow.
- `src/flows/home/home_flows.resource` usa keywords do POM.
- `src/pom/home/home_pom.resource` concentra interacao UI.

## Dados e variaveis

- Reaproveitar variaveis centralizadas em `src/resource/config` do projeto alvo.
- Evitar hardcode de URL se houver variavel de ambiente disponivel.
