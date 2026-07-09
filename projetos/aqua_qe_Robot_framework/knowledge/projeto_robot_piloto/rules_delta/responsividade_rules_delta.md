# RESPONSIVIDADE rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo responsividade.

## KB-RESP-001

### Regras novas em vigor

- Responsividade passa a ser tratada como criterio transversal obrigatorio de aceite para telas web do ecossistema BLC/ADG.
- A resolucao `768 x 1024` passa a ser a baseline minima suportada para validacao funcional e visual.
- O conjunto minimo de resolucoes de referencia passa a incluir: `768 x 1024`, `1024 x 768`, `1280 x 800`, `1366 x 768`, `1440 x 900`, `1600 x 900` e `1920 x 1080`.
- Nao pode haver quebra de layout que impeça o uso da tela, incluindo campos, botoes, modais ou filtros inacessiveis.
- Grids, tabelas, modais e formularios passam a exigir adaptacao preservando legibilidade, espacamento minimo e integridade visual.
- Botoes de acao principal, mensagens de erro e titulos passam a ter obrigacao de permanencia visivel sem scroll horizontal.
- Scroll horizontal inesperado em fluxo funcional passa a ser tratado como defeito de layout.

### Regras que deixam de valer

- Validacao visual restrita a uma unica resolucao de desktop.
- Aceitar sobreposicao de texto, truncamento ou desalinhamento como impacto cosmetico sem relevancia funcional.
- Considerar normal a necessidade de scroll horizontal para acessar acoes primarias ou mensagens criticas.
- Aprovar tela com componentes criticos parcialmente ocultos desde que o restante do fluxo funcione.

### Pontos de atencao

- Definir por modulo quais elementos sao considerados criticos para cada tela antes da execucao automatizada.
- Confirmar se alguns componentes usam comportamento responsivo distinto por breakpoint e exigem locators ou asserts diferenciados.
- Alinhar se validacoes de responsividade serao feitas apenas por viewport ou tambem por evidencia visual complementar (screenshot/comparacao).
- Garantir que modais, tabelas com muitas colunas e mensagens de erro tenham estrategia especifica de validacao em resolucoes menores.

### Impacto de automacao esperado

- Criar camada reutilizavel de validacao por viewport/resolucao para reuso entre modulos.
- Parametrizar suites para repetir fluxos principais nas resolucoes de referencia.
- Incluir verificacoes de ausencia de scroll horizontal, visibilidade de elementos criticos e ausencia de overlap.
- Mapear evidencias minimas por resolucao para apoiar triagem de regressao visual/funcional.
