# LINKS_ACESSOS_RAPIDOS rules delta ledger

Documento para registrar regras novas e regras descontinuadas por historia do modulo links_acessos_rapidos.

## EDUQ-514

### Regras novas em vigor

- Fluxo completo de CRUD de links rapidos (criar, editar e excluir).
- Acesso oficial via Home > Meus acessos rapidos.
- Botao ADICIONAR LINK condicionado a Titulo + URL preenchidos.
- Validacao de URL com mensagem: Insira uma URL valida.
- Exibicao de toast de sucesso para criar, editar e excluir.
- Atualizacao da quantidade de links apos operacoes de inclusao/exclusao.
- Ordenacao alfabetica crescente (A-Z) da lista de links.
- Paginacao obrigatoria (quantidade por pagina a definir pelo produto).
- Exibicao da tag de header abaixo do titulo (limite de 100 caracteres).
- Exibicao de favicon antes da URL com fallback para icone generico.
- Consistencia por usuario logado (escopo individual de visualizacao/gestao).

### Regras que deixam de valer

- Lista de links apenas estatica, sem gestao completa.
- Inclusao de link sem validacao estrita de campos obrigatorios.
- Inclusao de URL sem validacao de formato.
- Ausencia de mensagens de feedback para operacoes de CRUD.
- Falta de ordenacao definida e de paginacao.

### Pontos de atencao

- A historia cita premissa de ausencia de segregacao por usuario/participante, mas tambem exige reflexo apenas para usuario logado.
- Recomendacao de automacao: tratar como isolamento por sessao/identidade autenticada e registrar a premissa no teste.
- Definir em refinamento o tamanho de pagina para evitar assert fraco em paginacao.

### Impacto de automacao esperado

- Expandir suite `EDUQ-514.robot` para cobrir todos os CAs descritos.
- Incluir cenarios negativos de validacao de campo e URL.
- Incluir verificacoes de contador, ordenacao, paginacao e persistencia.
- Incluir verificacoes de edicao/exclusao com toast esperado.
- Incluir verificacoes de favicon com fallback generico.
