# EDUQ-90 [HOME] Ajuste Cards Home

## Story metadata

- story_id: EDUQ-90
- modulo: home
- perfil: Gestor de Fundos
- origem: Jira
- status_conhecimento: consolidado

## Objetivo

Como Gestor de Fundos, eu quero acessar a Home da Tela do Gestor para visualizar os cards atualizados e seus estados (habilitado/desabilitado), incluindo rotulos de novidade e redirecionamentos corretos.

## Escopo funcional

### Secao 1

1. Negociacao:
   - novo rotulo: Minha Operacao
   - estado: desabilitado
   - marcador visual: EM BREVE
2. Tarifacao e Lancamentos
3. Eventos Corporativos
4. Atendimento Buy Side
5. Monitoramento de Plataformas
6. Contratacao de Servicos:
   - incluir marcador visual: NOVIDADE
   - redirecionar para tela de Contratacao
7. B3 for Developers:
   - incluir marcador visual: NOVIDADE
   - redirecionar para B3 for Developers (comportamento atual mantido)

### Secao 2

1. Alterar titulo de secao:
   - de: Comunicados B3
   - para: Comunicacao B3
2. Comunicado AtendeB3:
   - estado: desabilitado
   - marcador visual: EM BREVE
   - icone: notifications
   - descricao: Avisos emitidos pela Central de Atendimento sobre incidentes ou orientacoes
3. Oficios e Comunicados:
   - redirecionar para site como ocorre hoje
4. Novidades B3:
   - incluir marcador visual: NOVIDADE

### Secao 3

1. iMercado:
   - redirecionar para iMercado
2. BTB:
   - redirecionar para BTB
3. Trademate:
   - estado: desabilitado
   - marcador visual: EM BREVE

## Regras novas em vigor

- R1: Card Negociacao passa a ser Minha Operacao e deve ficar desabilitado com EM BREVE.
- R2: Contratacao de Servicos deve exibir selo NOVIDADE e redirecionar para Contratacao.
- R3: B3 for Developers deve exibir selo NOVIDADE e manter redirecionamento atual.
- R4: Titulo da secao Comunicados B3 muda para Comunicacao B3.
- R5: Comunicado AtendeB3 deve ficar desabilitado com EM BREVE, icone notifications e descricao definida.
- R6: Novidades B3 deve exibir selo NOVIDADE.
- R7: iMercado e BTB devem redirecionar corretamente.
- R8: Trademate deve ficar desabilitado com EM BREVE.

## Regras que deixam de fazer sentido

- L1: Nome do card Negociacao como item ativo padrao.
- L2: Titulo de secao Comunicados B3.
- L3: Ausencia de selo NOVIDADE em Contratacao de Servicos, B3 for Developers e Novidades B3.
- L4: Disponibilidade ativa de Comunicado AtendeB3 e Trademate.

## Criterios de aceite mapeados para automacao

- CA1: Home carrega para perfil Gestor de Fundos.
- CA2: Secao 1 exibe cards esperados e estados corretos.
- CA3: Secao 2 exibe titulo atualizado e comportamento correto por card.
- CA4: Secao 3 exibe redirecionamentos/estados corretos.
- CA5: Cards com NOVIDADE exibem marcador visual.
- CA6: Cards com EM BREVE nao permitem navegacao.

## Mapeamento LKDF recomendado

- test_suite: test_suites/home/EDUQ-90-home-ajuste-cards.robot
- scenarios: src/scenarios/home/home_scenarios.resource
- flows: src/flows/home/home_flows.resource
- pom: src/pom/home/home_pom.resource
- dados: src/date_test/home_data.resource

## Tags recomendadas

- EDUQ-90
- home
- smoke
- regressao-ui
- cards

## Casos de teste sugeridos

1. EDUQ-90 - validar rotulos e estados da secao 1
2. EDUQ-90 - validar comunicacao B3 e cards da secao 2
3. EDUQ-90 - validar redirecionamentos e bloqueios da secao 3
4. EDUQ-90 - validar selos NOVIDADE e EM BREVE
