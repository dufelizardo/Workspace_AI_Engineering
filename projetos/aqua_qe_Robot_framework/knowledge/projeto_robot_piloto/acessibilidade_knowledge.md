# Base transversal de acessibilidade

## Objetivo

Centralizar criterios reutilizaveis de acessibilidade para automacao LKDF, com foco em WCAG 2.2 AA e aplicacao incremental por modulo.

## Referencias oficiais

- W3C WAI: https://www.w3.org/WAI/standards-guidelines/
- Guia WCAG: https://guia-wcag.com/
- axe-core local: `src/resource/acessibilidade/axe.min.js`
- Lighthouse: auditoria complementar por pagina

## Modelo de cobertura reutilizavel

### 1) Baseline automatizado (pipeline)

- Executar axe-core em telas prioritarias.
- Validar interacoes basicas de teclado em acoes primarias.
- Validar nome acessivel de botoes/links criticos.
- Validar estrutura minima de headings e landmarks.
- Classificar findings por severidade.

### 2) Baseline manual assistido (checklist)

- Leitura e compreensao sem sobrecarga visual em fluxo real.
- Ordem de foco coerente em componentes customizados.
- Feedback de erro compreensivel e associado ao campo.
- Confirmacao de contexto para leitores de tela em fluxos sensiveis.

## Politica de severidade sugerida

- Bloqueante: quebra de navegacao ou uso por teclado/leitor de tela.
- Alta: impede conclusao de tarefa principal com autonomia.
- Media: causa atrito relevante, mas com contorno viavel.
- Baixa: melhoria recomendada sem impacto funcional imediato.

## Matriz de adocao por modulo

- Home: navegacao, cards, foco e nome acessivel.
- Limites de Posicoes: filtros, tabela, tooltip, paginação, exportacao.
- Consulta ISIN: formulario de busca, resultados e feedback.
- Ativos Aceitos em Garantia: tabela, filtros e estados vazios.
- Links e Acessos Rapidos: cards e links de navegacao.

## Saida LKDF recomendada

- `test_suites/acessibilidade/`
- `src/scenarios/acessibilidade/`
- `src/flows/acessibilidade/`
- `src/pom/acessibilidade/`

## Historias relacionadas

- `knowledge/stories/KB-A11Y-001.md`
- `knowledge/stories/KB-RESP-001.md`
