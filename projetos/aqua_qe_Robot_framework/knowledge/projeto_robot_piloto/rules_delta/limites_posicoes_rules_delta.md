# LIMITES_POSICOES rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo limites_posicoes.

## EDUQ-1981

### Regras novas em vigor

- Deve existir card Limites de Posicoes na Home da Projeto Piloto.
- O card deve ser posicionado em ordem alfabetica considerando todos os cards existentes da Home.
- O card deve exibir titulo, descricao oficial e botao ACESSAR.
- Ao clicar em ACESSAR, a navegacao deve ocorrer para tela de Limites na mesma aba.

### Regras que deixam de valer

- Ausencia de card de entrada para funcionalidade Limites de Posicoes na Home.
- Posicionamento sem criterio alfabetico entre cards da Projeto Piloto.
- Acesso que abra fora da mesma aba para o fluxo de Limites.

### Pontos de atencao

- Ordenacao alfabetica depende do conjunto ativo de cards no ambiente e perfil.
- Confirmar nome final da tela de destino apos clique no card para evitar assert fragil.
- Garantir consistencia do texto da descricao oficial entre design e front-end.

### Impacto de automacao esperado

- Incluir teste de exibicao do card com titulo e descricao.
- Incluir teste de ordenacao alfabetica do card na Home.
- Incluir teste de clique no CTA ACESSAR com navegacao em mesma aba.
- Incluir teste de carregamento da tela de Limites apos navegacao.

## EDUQ-1984

### Regras novas em vigor

- Tela de Limites de Posicoes deve exibir titulo, descricao, botao Voltar e ultima atualizacao.
- Dados apresentados devem ter origem na base SLP.
- Resultado da pesquisa deve ser paginado com 50 registros por pagina.
- Contador de pagina deve seguir formato Mostrando X-Y de Z registros.
- Paginacao deve permitir ir para primeira, ultima, proxima e anterior.

### Regras que deixam de valer

- Tela sem contexto inicial completo para leitura e confiabilidade dos dados.
- Exibicao de resultados sem padrao de 50 registros por pagina.
- Ausencia de contador padronizado de totalizacao.
- Paginacao sem controles completos de navegacao.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com EDUQ-1981.
- EDUQ-1981 cobre o acesso via card na Home e EDUQ-1984 cobre o contexto interno da tela.

### Pontos de atencao

- A validacao da ultima atualizacao depende de referencia do ultimo arquivo publicado.
- Confirmar em ambiente de teste como obter a referencia do SLP para assert confiavel.
- Definir estrategia para validar exatamente 50 registros por pagina em diferentes massas de dados.

### Impacto de automacao esperado

- Incluir teste de layout inicial da tela (titulo, descricao, Voltar, ultima atualizacao).
- Incluir teste de regex para contador Mostrando X-Y de Z registros.
- Incluir testes de navegacao de paginacao (primeira, ultima, proxima, anterior).
- Incluir teste de quantidade maxima de 50 itens por pagina.

## EDUQ-1997

### Regras novas em vigor

- Busca por Ativo/Ticker passa a ser automatica a partir do terceiro caractere digitado.
- Busca por Ativo/Ticker passa a aceitar apenas caracteres alfanumericos.
- Busca por Ativo/Ticker passa a ter limite maximo de 20 caracteres.
- Busca deve considerar apenas o mercado atualmente selecionado.
- Filtros exibidos passam a variar por mercado:
  - Mercado Listado: Tipo de Limite, Natureza e Nivel de Agregacao.
  - Mercado Balcao: Tipo de Limite, Vertice, Tipo de Barreira, Natureza e Nivel de Agregacao.
- Um mesmo filtro passa a aceitar multiselecao.
- Filtros aplicados passam a ser exibidos individualmente na tela.
- Usuario passa a poder remover um filtro especifico ou limpar todos de uma vez.
- Busca e filtros passam a impactar tabela, paginacao e exportacao.
- Campo Tipo de Limite passa a ter validacao propria por tipo de dado e tamanho.
- Campo Natureza passa a ter validacao propria por tipo de dado e tamanho.

### Regras que deixam de valer

- Busca com um ou dois caracteres disparando filtro automaticamente.
- Conjunto fixo de filtros independente do mercado selecionado.
- Ausencia de exibicao individual dos filtros aplicados.
- Reset manual campo a campo como unica forma de remover filtros.
- Exportacao desconectada do estado corrente de busca e filtros.
- Permitir caracteres especiais no campo de busca.
- Permitir mais de 20 caracteres no campo de busca.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com `EDUQ-1981`; `EDUQ-1981` cobre o acesso via Home.
- Complementa `EDUQ-1984`, porque paginação e contador passam a refletir o estado filtrado.
- Exige cuidado para nao invalidar asserts anteriores de contexto, contador e paginacao ao aplicar filtros.

### Pontos de atencao

- Confirmar em ambiente se a busca e debounce/automatica sem necessidade de Enter.
- Confirmar se a mensagem de validacao exibida para 1 ou 2 caracteres e exatamente: `A Busca por Ativo (Ticker) deve conter no mínimo 3 caracteres.`
- Confirmar quais combinacoes de filtros possuem massa estavel para regressao.
- Validar estrategia de assert para exportacao filtrada, caso download ainda nao esteja automatizado.
- Garantir que nomes acentuados de filtros (ex.: Nível de Agregação, Vértice) estejam aderentes ao front-end final.
- Confirmar se o contrato de `maxlength` do front-end ja foi corrigido para 20 caracteres ou se permanece divergente do baseline operacional atual.

### Impacto de automacao esperado

- Incluir teste de limiar minimo da busca (1 e 2 vs 3 caracteres).
- Incluir teste de busca respeitando o mercado selecionado.
- Incluir teste de combinacao de busca com filtros.
- Incluir teste de filtros por mercado, multiselecao e chips individuais.
- Incluir teste de remocao individual e limpeza total de filtros.
- Incluir teste de restricao a caracteres especiais e de limite maximo no campo de busca.
- Incluir testes de validacao dos campos Tipo de Limite e Natureza.

## EDUQ-1985

### Regras novas em vigor

- A tela passa a explicitar duas abas de mercado: `Mercado Listado` e `Mercado de Balcao`.
- O mercado selecionado passa a determinar a estrutura da tabela exibida.
- A troca de mercado passa a exigir reset de busca, filtros, ordenacao e paginacao.
- O sistema passa a expor quantidade de registros carregados conforme o mercado selecionado.
- Cabecalhos da tabela passam a exigir icones informativos com descricao contextual do campo.

### Regras que deixam de valer

- Estrutura unica de colunas independente do mercado.
- Persistencia de estado da consulta ao alternar entre mercados.
- Cabecalho sem ajuda contextual/tooltip por coluna.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com `EDUQ-1981`, que cobre apenas o card de acesso via Home.
- Complementa `EDUQ-1984`, pois especializa o comportamento da grade e do contador por mercado.
- Complementa `EDUQ-1997`, adicionando a obrigacao de resetar busca/filtros ao trocar de aba.
- Ha conflito interno na propria historia: RN02/RN04 indicam `Mercado Listado` selecionado por padrao, enquanto CA01 descreve ausencia inicial de selecao com mensagem orientativa.

### Pontos de atencao

- Alinhar com Produto qual comportamento inicial deve prevalecer antes da execucao E2E final.
- Confirmar os textos finais das colunas com acentuacao (`Vértice`, `Início do Vértice`, `Nível de Agregação`).
- Definir estratégia robusta para validar tooltip quando a descricao vier por `title`, `aria-label` ou componente visual dedicado.
- Garantir massa de dados suficiente em ambos os mercados para validar carregamento e reset.

### Impacto de automacao esperado

- Incluir teste de exibicao e ordem das abas de mercado.
- Incluir testes dedicados de estrutura de colunas para `Mercado Listado` e `Mercado de Balcao`.
- Incluir teste de reset de busca, filtros, ordenacao e paginacao ao trocar de mercado.
- Incluir teste de icones informativos e tooltip dos cabecalhos.

## EDUQ-1999

### Regras novas em vigor

- A tabela passa a exibir identificacao visual de direcao para `Comprado`, `Vendido`, `Potencial de Recebimento` e `Potencial de entrega`.
- Quando nao houver resultados, a tela deve exibir a mensagem `Nenhum resultado encontrado`.
- Cada coluna da tabela passa a possuir um icone de informacao `(i)`.
- Ao interagir com o icone informativo, deve ser apresentada a descricao do campo via tooltip.
- O dicionario de testes deve contemplar campos dos dois mercados.

### Regras que deixam de valer

- Registros sem indicacao visual de direcao.
- Estado vazio sem mensagem clara ao usuario.
- Cabecalhos sem ajuda contextual por coluna.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com `EDUQ-1981`.
- Complementa `EDUQ-1984`, adicionando estados visuais e estado vazio ao comportamento da tabela.
- Complementa `EDUQ-1985`, que ja introduziu abas de mercado e ajuda contextual por coluna.
- Complementa `EDUQ-1997`, porque estados sem resultado podem ocorrer apos busca/filtros.

### Pontos de atencao

- Confirmar com Produto/UX como a direcao visual sera representada (cor, icone, selo ou seta).
- Confirmar se a mensagem de vazio substitui totalmente a tabela ou coexistira com area vazia padronizada.
- Validar se o tooltip usa `title`, `aria-label` ou componente visual dedicado.
- Confirmar se os estados visuais sao iguais em ambos os mercados.

### Impacto de automacao esperado

- Incluir teste de identificacao visual da direcao dos registros.
- Incluir teste de tooltip/descricao dos campos por coluna.
- Incluir teste de mensagem de nenhum resultado encontrado.

## EDUQ-1998

### Regras novas em vigor

- Exportacao passa a oferecer os formatos `CSV`, `XLSX` e `TXT`.
- Exportacao deve respeitar o estado atual da consulta: mercado, filtros e busca.
- Arquivo exportado deve conter apenas os dados visiveis na tabela da busca/filtro.
- Arquivo exportado deve conter todas as colunas do mercado selecionado.
- Nome do arquivo exportado passa a seguir o padrao `Limite_[Mercado]_YYYYMMDD.ext`.

### Regras que deixam de valer

- Exportacao sem considerar o estado corrente da consulta.
- Nome de arquivo livre, sem padrao de mercado e data.
- Formatos de exportacao adicionais fora de CSV, XLSX e TXT.

### Conflitos identificados com historias anteriores

- Nao ha conflito direto com `EDUQ-1981`.
- Complementa `EDUQ-1984`, porque exportacao deve refletir o mesmo conjunto de dados paginado/contado na tela.
- Complementa `EDUQ-1985`, pois exportacao passa a respeitar o mercado selecionado.
- Complementa `EDUQ-1997`, porque busca e filtros impactam a consulta exportada.
- Complementa `EDUQ-1999`, porque os estados visuais e vazios nao alteram o contrato de exportacao.

### Pontos de atencao

- Confirmar se a exportacao usa `download` direto do browser ou um endpoint assinado.
- Confirmar se o nome do arquivo usa mercado traduzido exatamente como aparece na aba.
- Confirmar se a exportacao de consulta atual replica apenas a pagina corrente ou toda a consulta filtrada.
- Validar massa para checar se o nome do arquivo inclui a data do dia da exportacao.

### Impacto de automacao esperado

- Incluir teste para abrir menu e exibir formatos disponíveis.
- Incluir teste para exportacao de consulta atual com estado filtrado.
- Incluir teste para gerar arquivos CSV, XLSX e TXT.
- Incluir teste de nome do arquivo com mercado e data.
