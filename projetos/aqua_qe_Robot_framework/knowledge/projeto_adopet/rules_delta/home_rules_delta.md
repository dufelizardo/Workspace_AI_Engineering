# HOME rules delta ledger

Documento para registrar regras novas e regras descontinuadas por história do módulo home.

## ADOP-0001

### Regras novas em vigor

- Landing page pública — acessível sem autenticação prévia (RN01).
- Botão "Ver pets disponíveis para adoção" redireciona para `/home` (RN02).
- Link "Cadastrar" redireciona para `/cadastro` (RN02).
- Link "Fazer login" redireciona para `/login` (RN02).
- Layout responsivo obrigatório para mobile, tablet e desktop (RN03).

### Regras que deixam de valer

- Nenhuma — história inaugural do módulo home.

### Pontos de atenção

- DOM sem `data-testid`: seletores usam `data-test` (Cadastrar/Login), `aria-label` (header) e CSS semântico (CTA Ver Pets, footer). Se o time de front adicionar `data-testid`, atualizar `home_locators.resource`.
- Botão "Ver pets" usa `css=a.button[href="/home"]` — frágil se a classe ou href mudar. Prioridade: solicitar `data-test` ao time de front.
- CA6, CA7 e CA8 navegam para fora da landing page: cada teste usa `Test Setup` individual para recarregar a URL antes de clicar.
- Texto de boas-vindas validado por igualdade exata (`Should Be Equal`) — qualquer alteração tipográfica quebra o CA2. Centralizado em `data_home.resource`.

### Impacto de automação esperado

- Arquivos criados (2026-07-09): 6 camadas LKDF completas para o módulo home.
- `home_locators.resource` é o único ponto a atualizar se o DOM mudar.
- `data_home.resource` é o único ponto a atualizar se o texto de boas-vindas mudar.
