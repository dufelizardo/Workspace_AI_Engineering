# Proposta de camada de validacao DOM - Limites de Posições

## Objetivo

Criar uma camada objetiva de validacao de DOM para a tela `Limites de Posições`, baseada no snapshot real atual e preparada para evoluir quando a funcionalidade for corrigida.

## Baseline atual

- Tela: `Limites de Posições`
- Snapshot oficial: `DOM-LIMITES_POSICOES-20260701-001`
- Arquivo do snapshot: `snapshots/DOM-LIMITES_POSICOES-20260701-001.html`
- Contract atual: `contracts/dom_contract.json`

## Escopo da camada

A camada deve validar:

1. Estrutura base da pagina
   - `main#conteudo`
   - `section[aria-label='Limites de Posições']`
   - breadcrumb
   - titulo `h1`
   - subtitulo e data de atualizacao
   - botao `Voltar`

2. Abas de mercado
   - `Mercado Listado`
   - `Mercado Balcão`
   - estado ativo com `aria-selected`
   - troca de aba sem quebrar o DOM esperado

3. Busca e filtros
   - input de busca por ativo
   - mensagem de apoio de 2+ caracteres
   - filtros por mercado
   - estado visual de filtros aplicados
   - botao `Limpar Filtros`

4. Exportacao
   - botao exportar
   - menu de exportacao
   - opcoes CSV / XLSX / TXT
   - escopo `consulta atual` e `base completa`
   - estado habilitado/desabilitado das opcoes conforme contexto

5. Tabela
   - tabela por mercado
   - cabecalhos corretos por aba
   - `role='columnheader'`
   - `aria-sort`
   - tooltips por coluna
   - badges de natureza, nivel e barreira

6. Paginação
   - contador de registros
   - `Linhas por página`
   - navegacao primeira / anterior / proxima / ultima
   - estados disabled quando aplicavel

## Regras de validacao

### Regras duras

- Nao validar apenas texto; validar tambem atributos semanticos quando existirem.
- Nao assumir seletor por classe quando houver `aria-label`, `role`, `id` ou `data-testid`.
- Quando houver divergencia entre aba e tabela, tratar como falha de DOM.
- Quando houver nova versao do DOM, registrar diff antes de atualizar locators.

### Regras de evolucao

- Se o DOM mudar por correcoes da funcionalidade, gerar novo snapshot.
- Se mudarem apenas classes visuais, manter prioridade em seletores semanticos.
- Se mudarem `aria-label` ou `role`, revisar o contrato e os locators.

## Sugestao de keywords Robot

### Basicas
- `Limites Posicoes - Validar estrutura base da pagina`
- `Limites Posicoes - Validar abas de mercado`
- `Limites Posicoes - Validar filtros da aba atual`
- `Limites Posicoes - Validar tabela do mercado`
- `Limites Posicoes - Validar paginacao`
- `Limites Posicoes - Validar exportacao`

### Semanticas
- `Limites Posicoes - Validar atributo aria-selected`
- `Limites Posicoes - Validar atributo aria-sort`
- `Limites Posicoes - Validar tooltip da coluna`
- `Limites Posicoes - Validar badge de natureza`
- `Limites Posicoes - Validar badge de nivel`
- `Limites Posicoes - Validar estado disabled do botao`

## Mapa de locators prioritarios

Prioridade 1:
- `section[aria-label='Limites de Posições']`
- `h1.b3-section__title`
- `button[aria-label='Voltar para a página inicial']`
- `a[role='tab'][aria-selected]`
- `table[aria-label^='Tabela de Limites de Posições']`
- `button[aria-label='Abrir menu de exportação de arquivo com opções de formato e escopo']`

Prioridade 2:
- `input#searchTicker_listado`
- `input#searchTicker_balcao`
- `button[aria-label^='Filtrar por Tipo de Limite']`
- `button[aria-label^='Filtrar por Natureza']`
- `button[aria-label^='Filtrar por Nível de Agregação']`
- `p.pagina-dinamica`
- `b3-select-item[idinput='limitesPageSizeId']`

Prioridade 3:
- `th[role='columnheader']`
- `b3-icon.info-icon`
- badges de natureza, nivel e barreira com `aria-label`

## Observacao importante

Este documento foi criado para orientar a camada de DOM da tela correta. Se a funcionalidade mudar, o snapshot deve ser atualizado e o contrato deve ser revisto antes de mexer nos locators da automacao Robot.
