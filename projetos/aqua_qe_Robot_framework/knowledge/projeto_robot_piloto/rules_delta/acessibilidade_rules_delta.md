# ACESSIBILIDADE rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo acessibilidade.

## KB-A11Y-001

### Regras novas em vigor

- Acessibilidade passa a ser tratada como criterio transversal de qualidade para os modulos UI do ecossistema.
- WCAG 2.2 nivel AA passa a ser baseline de referencia para criterios de aceite.
- axe-core (via `axe.min.js`) passa a ser estrategia automatizada recomendada para varredura recorrente.
- Lighthouse passa a ser evidencia complementar para diagnostico e priorizacao de risco.
- Findings devem ser classificados por severidade para decisao de bloqueio/release.

### Regras que deixam de valer

- Validacao de acessibilidade somente manual e sem rastreabilidade por historia.
- Ausencia de criterios minimos de aceitacao para navegacao por teclado e nome acessivel.
- Uso de score agregado como unico criterio de aprovacao.

### Pontos de atencao

- Nem todo criterio WCAG e totalmente automatizavel; manter checklist manual para casos de julgamento.
- Configurar limiar de severidade para falha de pipeline sem aumentar ruído de falso positivo.
- Definir escopo inicial por pagina/fluxo para adocao incremental sem travar entregas.
- Revisar componentes customizados com prioridade (tabelas, filtros, modais e dropdowns complexos).

### Impacto de automacao esperado

- Criar biblioteca LKDF reutilizavel para acessibilidade em `test_suites/scenarios/flows/pom`.
- Padronizar keyword de injecao e execucao do axe-core por pagina.
- Padronizar coleta de evidencias Lighthouse e anexos por modulo.
- Consolidar relatorio de findings por severidade com recomendacao de acao.
