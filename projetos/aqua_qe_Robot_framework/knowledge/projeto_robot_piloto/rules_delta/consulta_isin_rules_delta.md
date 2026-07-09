# CONSULTA_ISIN rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo consulta_isin.

## EDUQ-1724

### Regras novas em vigor

- Novo card Consulta de ISIN deve existir na Home da Projeto Piloto.
- O card deve exibir titulo, descricao oficial e CTA ACESSAR.
- O posicionamento do card deve seguir ordenacao alfabetica dos cards da secao.
- O clique em ACESSAR deve navegar para Consulta de ISIN na mesma aba.
- O acesso inicial nao deve disparar consulta de dados automaticamente.

### Regras que deixam de valer

- Ausencia de card de entrada para Consulta de ISIN na Home.
- Posicionamento sem criterio alfabetico entre cards equivalentes.
- Disparo de consulta de dados sem acao explicita do usuario ao entrar na tela.

### Pontos de atencao

- A ordenacao alfabetica depende do conjunto ativo de cards da Home; validar com massa de dados e perfil padrao.
- Confirmar se o comportamento sem consulta inicial exige estado vazio, placeholder ou mensagem de orientacao.
- Revisar seletores de card para evitar ambiguidade com outros cards na primeira secao.

### Impacto de automacao esperado

- Incluir teste de exibicao do card com titulo e descricao.
- Incluir teste de ordenacao alfabetica do card na Home.
- Incluir teste de navegacao em mesma aba ao clicar no CTA ACESSAR.
- Incluir teste de nao execucao automatica de consulta ao abrir a tela.
- Incluir teste de exibicao da tela Consulta de ISIN apos navegacao.
