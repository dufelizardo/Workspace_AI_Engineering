# HOME rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia.

## EDUQ-90

### Regras novas em vigor

- Negociacao vira Minha Operacao, desabilitado, com EM BREVE.
- Contratacao de Servicos recebe NOVIDADE e redireciona para Contratacao.
- B3 for Developers recebe NOVIDADE e mantem redirecionamento atual.
- Secao Comunicados B3 passa para Comunicacao B3.
- Comunicado AtendeB3 fica desabilitado com EM BREVE, icone notifications e descricao oficial.
- Novidades B3 recebe NOVIDADE.
- iMercado e BTB devem redirecionar.
- Trademate fica desabilitado com EM BREVE.

### Regras que deixam de valer

- Nome Negociacao como comportamento anterior na secao 1.
- Titulo Comunicados B3 na secao 2.
- Ausencia de selo NOVIDADE nos cards citados.
- Estado habilitado de Comunicado AtendeB3 e Trademate.

### Pontos de atencao para QA

- Seletores que referenciam texto "Negociacao" vao quebrar; atualizar para "Minha Operacao" em todo o POM.
- Estados EM BREVE e NOVIDADE podem ser controlados por feature flag ou backend — definir massa de dados controlavel para cada estado.
- Cards com URL externa (B3 for Developers, Oficios e Comunicados) podem abrir nova aba/janela; tratar com `Wait For Page` ou `Switch Page`.
- Validar ordenacao visual dos cards para detectar regressao de posicao.
- CA10 (cards EM BREVE nao permitem clique) deve ser testado por `aria-disabled=true` no container E `disabled` no botao ACESSAR.

### Riscos de QA

- Regressao de cards existentes ao mudar ordem ou estado de qualquer card da secao 1.
- Testes de redirecionamento de B3 for Developers e Oficios e Comunicados dependem de ambiente com URL externa acessivel.
- Badge NOVIDADE pode desaparecer apos X dias — nao depender de estados de producao para o teste.

### Arquivos gerados (2026-07-08)

- `test_suites/home/EDUQ-90-ajuste-cards.robot` — 11 casos de teste, tags: smoke/regressao-ui/cards/novidade/em-breve
- `src/scenarios/home/home_scenarios.resource` — keywords BDD de alto nivel
- `src/flows/home/home_flows.resource` — flows de validacao de estado e redirecionamento
- `src/pom/home/home_pom.resource` — locators via data-testid para todos os cards das 3 secoes
- Projeto alvo: `C:\dev\projeto_robot_piloto`

### Impacto de automacao esperado

- Atualizar assertions de rotulo em Home (Negociacao -> Minha Operacao).
- Atualizar assertions de estado habilitado/desabilitado.
- Atualizar validacoes de badge NOVIDADE e EM BREVE.
- Atualizar asserts de redirecionamento por card.
- Atualizar titulo da secao 2 (Comunicados B3 -> Comunicacao B3).

## EDUQ-274

### Regras novas em vigor

- Cards Minhas Ordens, Tarifacao e Lancamentos Futuros, Eventos Corporativos, Monitoramento de Plataforma, Atende B3 e Hub Balcao ficam ocultos na Home para R1.
- Contratacao de Servicos nao deve exibir o selo NOVIDADE na Home para R1.
- Logica de visibilidade deve ser flexivel para habilitacao futura dos cards ocultos.

### Regras que deixam de valer

- Exibicao dos cards listados acima na Home de R1.
- Exibicao de NOVIDADE em Contratacao de Servicos na Home de R1.

### Conflitos identificados com historias anteriores

- EDUQ-90 dizia que Contratacao de Servicos deveria exibir NOVIDADE.
- EDUQ-274 remove NOVIDADE em Contratacao de Servicos para R1.
- Precedencia recomendada: aplicar a regra da historia mais recente por release/contexto.

### Impacto de automacao esperado

- Atualizar testes para validar ausencia de cards ocultos.
- Atualizar testes para validar ausencia do selo NOVIDADE em Contratacao de Servicos.
- Introduzir cenarios de toggle/release para evitar quebra quando cards voltarem a aparecer.

## EDUQ-495

### Regras novas em vigor

- Novo card Inteligencia de Dados deve ser exibido na Home da Projeto Piloto.
- O card deve conter titulo, descricao oficial e botao ACESSAR.
- O botao ACESSAR deve redirecionar para landing page da Neoway.

### Regras que deixam de valer

- Ausencia de card Neoway (Inteligencia de Dados) na Home.
- Fluxo sem acesso direto da Home para landing page da Neoway.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com EDUQ-90 e EDUQ-274 para o mesmo card.
- Necessario validar coexistencia visual com cards ocultos de R1 definidos em EDUQ-274.

### Impacto de automacao esperado

- Incluir testes positivos de exibicao do card Inteligencia de Dados.
- Incluir teste de assertiva textual da descricao do card.
- Incluir teste de redirecionamento via botao ACESSAR para landing page da Neoway.

## EDUQ-1578

### Regras novas em vigor

- Meus acessos rapidos passa a exibir botao VOLTAR no canto superior direito.
- Novidades passa a exibir botao VOLTAR no canto superior direito.
- Breadcrumb de Meus acessos rapidos deve usar Home > Meus acessos rapidos.
- Cards da secao Comunicacao B3 devem usar CTA ACESSAR no lugar de VERIFICAR.

### Regras que deixam de valer

- Ausencia do botao VOLTAR em Meus acessos rapidos e Novidades.
- Texto Quick Links no breadcrumb de Meus acessos rapidos.
- CTA VERIFICAR na secao Comunicacao B3.

### Conflitos identificados com historias anteriores

- Nao ha conflito funcional com EDUQ-90, EDUQ-274 e EDUQ-495; trata-se de padronizacao de navegacao e rotulos.
- Complementa EDUQ-514 ao padronizar nomenclatura e navegacao de Meus acessos rapidos.

### Impacto de automacao esperado

- Atualizar validacoes de breadcrumb em Meus acessos rapidos.
- Incluir validacoes de presenca do botao VOLTAR em Meus acessos rapidos e Novidades.
- Atualizar assertions de texto dos CTAs da secao Comunicacao B3 para ACESSAR.
