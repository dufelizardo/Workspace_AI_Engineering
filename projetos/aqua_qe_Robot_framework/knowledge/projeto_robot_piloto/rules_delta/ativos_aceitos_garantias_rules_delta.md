# ATIVOS_ACEITOS_GARANTIAS rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo ativos_aceitos_garantias.

## EDUQ-1717

### Regras novas em vigor

- O card Ativos Aceitos em Garantia deve existir na primeira secao da Home da Projeto Piloto.
- O card deve conter titulo, descricao informativa oficial e botao ACESSAR.
- O clique em ACESSAR deve abrir a funcionalidade na mesma aba.
- Quando houver atualizacao proveniente do NGA, o card deve exibir indicador estatico NOVO ao lado do titulo.
- O layout deve seguir padrao visual da plataforma.
- A tela de destino deve exibir skeleton durante o carregamento.
- Devem ser previstos criterios de acessibilidade e tagueamento de analytics.

### Regras que deixam de valer

- Ausencia de acesso dedicado para Ativos Aceitos em Garantia na Home.
- Qualquer comportamento de navegacao que abra o fluxo fora da mesma aba.
- Ausencia de indicador visual de novidade quando houver atualizacao NGA.

### Pontos de atencao

- A regra do indicador NOVO depende de sinal de atualizacao vindo do NGA; em automacao, definir massa/flag controlavel para estados com e sem badge.
- Confirmar com produto quais eventos de tagueamento sao obrigatorios (impressao do card, clique em ACESSAR, exibicao de badge NOVO).
- Definir criterios minimos de acessibilidade para aceite (tab order, nome acessivel, contraste e foco visivel).

### Impacto de automacao esperado

- Incluir testes de exibicao e posicionamento do card na primeira secao da Home.
- Incluir teste de navegacao em mesma aba via ACESSAR.
- Incluir validacoes condicionais de badge NOVO com base em retorno NGA.
- Incluir teste de carregamento com skeleton na tela de destino.
- Incluir verificacoes de acessibilidade basica e de eventos de tagueamento.
