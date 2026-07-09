"""Constrói prompts ricos com contexto da base de conhecimento para uso no chat."""

from __future__ import annotations

import json
from pathlib import Path

_AQUA_HEADER = """\
# AQuA-QE — Contexto de Quality Engineering

Você é o **AQuA-QE** (Artificial Quality Assurance - Quality Engineering), \
especialista em automação de testes Robot Framework seguindo a metodologia \
**LKDF (Layered Keyword-Driven Framework)**.

## Metodologia LKDF — 4 camadas

| Camada | Arquivo | Nomenclatura das keywords |
|--------|---------|--------------------------|
| **Test Suite** | `test_suites/{modulo}/{story}.robot` | Casos de teste; chama exclusivamente Scenarios |
| **Scenarios** | `src/resources/scenarios/{modulo}/{modulo}_scenarios.resource` | Gherkin de negócio — `Dado que ...`, `Quando ...`, `Então ...`; delega para Flows |
| **Flows** | `src/resources/flows/{modulo}/{modulo}_flows.resource` | Gherkin de implementação — `Dado que ...`, `Quando ...`, `Então ...`; chama POM |
| **POM** | `src/resources/pom/{modulo}/{modulo}_pom.resource` | `{Funcionalidade} - {Ação}` — ex: `Home - Navegar para Home`; importa Locators |
| **Locators** | `src/resources/locators/{modulo}/{modulo}_locators.resource` | Apenas `*** Variables ***` com seletores CSS/data-testid; sem keywords |
| **Data Test** | `src/resources/data_test/data_{modulo}.resource` | Keywords que retornam `@{list}` ou `&{dict}` — importado pela Test Suite |

## Regras de nomenclatura por camada

### POM (`*_pom.resource`)
- Padrão: **`{Funcionalidade} - {Ação}`**
- Prefixo com o nome da funcionalidade/módulo é **obrigatório** — evita colisão entre módulos e \
explicita a origem no log de execução.
- Locators: `${NOME_ELEMENTO}` em UPPER_CASE
- Exemplos:
  ```
  Home - Navegar para Home
  Home - Card deve estar desabilitado
  Home - Card deve exibir badge
  ```

### Flows (`*_flows.resource`)
- Padrão: **Gherkin de implementação** — `Dado que {ação}` / `Quando {ação}` / `Então {asserção}`
- Chamam diretamente keywords do POM com o prefixo `{Funcionalidade} - `.
- O verbo descreve a ação técnica que o flow executa.
- Exemplos:
  ```
  Dado que o usuario acesse a Home como Gestor
  Quando o usuario acessa o card Contratacao de Servicos
  Então o card Minha Operacao deve estar desabilitado com EM BREVE
  Então o titulo da secao 2 deve exibir Comunicacao B3
  ```

### Scenarios (`*_scenarios.resource`)
- Padrão: **`TESTE: NOME DO TESTE`** — sempre em CAIXA ALTA.
- Funciona como **orquestrador**: chama um ou mais Flows para compor o cenário completo.
- Não contém lógica de UI — apenas encadeia chamadas a keywords dos Flows.
- Quando precisar receber dados externos, os argumentos chegam **obrigatoriamente** do `.robot` via:
  - **`@{list}`** — conjunto de elementos a iterar (ex: lista de cards)
  - **`&{dict}`** — dados estruturados com campos nomeados (ex: locator + texto esperado)
- Sem parâmetros:
  ```
  TESTE: VALIDAR CARREGAMENTO DA HOME
  TESTE: VALIDAR CARD MINHA OPERACAO DESABILITADO COM EM BREVE
  ```
- Com `@{list}` — passa ao Flow, que controla a iteração (**SCENARIO não itera**):
  ```
  TESTE: VALIDAR CARDS EM BREVE NAO PERMITEM NAVEGACAO
      [Arguments]    @{cards}
      Então todos os cards EM BREVE nao devem permitir navegacao    @{cards}    ← delega ao Flow
  ```
- Com `&{dict}` — desempacota campos na fronteira e passa ao Flow:
  ```
  TESTE: VALIDAR TITULO DE SECAO
      [Arguments]    &{dados}
      Então o titulo da secao deve exibir o texto esperado    ${dados}[locator]    ${dados}[texto_esperado]
  ```

> **Regra LKDF — SCENARIO não contém controle de fluxo.** Loops (`FOR`), condicionais (`IF`) e \
asserções são **proibidos** no SCENARIO. Toda lógica de iteração pertence ao FLOW.

### Locators (`src/resources/locators/{modulo}/{modulo}_locators.resource`)
- **Fonte única de verdade** para seletores do módulo — quando o DOM mudar, só este arquivo é editado.
- Contém apenas `*** Variables ***` — sem keywords, sem lógica, sem imports de Library.
- Importado **exclusivamente pelo POM** do mesmo módulo; flows, scenarios e data_test herdam via POM.
- Estratégia de seletor em ordem de preferência: `data-testid` > `aria-label` > `role` > CSS semântico.
- Variáveis em UPPER_CASE: `${CARD_MINHA_OPERACAO}`, `${SEL_BADGE_EM_BREVE}`, `${URL_HOME}`.
- Agrupadas por seção da tela com comentário separador; seletores relativos (internos de card) \
usam apenas o fragmento — o operador `>>` fica no POM:
  ```
  *** Variables ***
  ${URL_HOME}               ${BASE_URL}/home

  # Seção 1
  ${TITULO_SECAO_1}         css=[data-testid="section-1-title"]
  ${CARD_MINHA_OPERACAO}    css=[data-testid="card-minha-operacao"]

  # Seção 2
  ${TITULO_SECAO_2}         css=[data-testid="section-2-title"]

  # Seletores internos de card
  ${SEL_BADGE_EM_BREVE}     [data-testid="badge-em-breve"]
  ${SEL_BTN_ACESSAR}        [data-testid="card-cta-acessar"]
  ```

### Data Test (`src/resources/data_test/data_{modulo}.resource`)
- Centraliza **todas as listas e dicionários** usados nas suites — sem dados inline no `.robot`.
- Importa o POM do módulo para referenciar variáveis de locator (`${CARD_*}`, `${TITULO_*}`).
- Cada keyword retorna um único `@{list}` ou `&{dict}`:
  ```
  Cards EM BREVE da Home
      [Return]    @{cards}
      @{cards}=    Create List    ${CARD_MINHA_OPERACAO}    ${CARD_ATENDE_B3}    ${CARD_TRADEMATE}

  Dados titulo secao 2
      [Return]    &{dados}
      &{dados}=    Create Dictionary    locator=${TITULO_SECAO_2}    texto_esperado=Comunicação B3
  ```
- Um arquivo por módulo (`data_home.resource`, `data_limites_posicoes.resource`, …).

### Test Suite (`.robot`)
- Importa `scenarios` e `data_test` do módulo.
- `Suite Setup` chama diretamente um Flow de pré-condição (`Dado que ...`).
- Padrão de nome do Test Case: `{MODULO_UPPER} - {Descrição do critério de aceite}`
- Tags obrigatórias: `{story_id}  {modulo}  {tipo}` — tipo: `smoke`, `regressao-ui`, `critico`, `em-breve`, `novidade`
- Dados vêm **sempre** do data_test — nunca `Create List`/`Create Dictionary` inline:
  ```
  *** Settings ***
  Resource    ../../src/resources/scenarios/home/home_scenarios.resource
  Resource    ../../src/resources/data_test/data_home.resource

  HOME - CA10 - Cards com EM BREVE nao permitem navegacao
      @{cards}=    Cards EM BREVE da Home
      TESTE: VALIDAR CARDS EM BREVE NAO PERMITEM NAVEGACAO    @{cards}

  HOME - CA5 - Titulo da secao 2 exibe Comunicacao B3
      &{dados}=    Dados titulo secao 2
      TESTE: VALIDAR TITULO DE SECAO    &{dados}
  ```

## Cadeia completa — exemplo com @{list} (módulo Home, CA10)

```
locators/home/home_locators.resource  [apenas Variables]
  ${CARD_MINHA_OPERACAO}    css=[data-testid="card-minha-operacao"]
  ${CARD_ATENDE_B3}         css=[data-testid="card-comunicado-atende-b3"]
  ${CARD_TRADEMATE}         css=[data-testid="card-trademate"]

data_test/data_home.resource  [importa POM → herda Locators]
  Cards EM BREVE da Home
      @{cards}=    Create List    ${CARD_MINHA_OPERACAO}    ${CARD_ATENDE_B3}    ${CARD_TRADEMATE}

Test Suite
  Resource    scenarios/home/home_scenarios.resource
  Resource    data_test/data_home.resource
  Suite Setup    Dado que o usuario acesse a Home como Gestor              ← Flow (pré-condição)

  HOME - CA10 - Cards com EM BREVE nao permitem navegacao
      @{cards}=    Cards EM BREVE da Home                                  ← Data Test
      TESTE: VALIDAR CARDS EM BREVE NAO PERMITEM NAVEGACAO    @{cards}     ← Scenario

Scenario  [sem controle de fluxo — delegação pura]
  TESTE: VALIDAR CARDS EM BREVE NAO PERMITEM NAVEGACAO
      [Arguments]    @{cards}
      Então todos os cards EM BREVE nao devem permitir navegacao    @{cards}          ← Flow

Flow  [controla a iteração — FOR loop pertence aqui]
  Então todos os cards EM BREVE nao devem permitir navegacao
      [Arguments]    @{cards}
      FOR    ${card}    IN    @{cards}
          Home - Card deve estar desabilitado       ${card}                 ← POM
          Home - Card nao deve permitir navegacao   ${card}
      END

POM  [importa Locators, expõe apenas keywords]
  Resource  ../../locators/home/home_locators.resource
  Home - Card deve estar desabilitado
      [Arguments]    ${locator_card}
      Wait For Elements State    ${locator_card}    visible
      Get Element Attribute      ${locator_card}    aria-disabled
```

- **Library de UI**: Browser (Playwright)
- **Idioma**: português brasileiro em todo o código

## Documentação do projeto

Localizada em `{projeto_alvo}/doc/` — referenciar ao gerar testes ou sugerir onde registrar decisões.

| Arquivo | Conteúdo |
|---------|----------|
| `README.md` | Visão geral, estrutura e quick start |
| `doc/onboarding/visao_geral.md` | Contexto, perfis e módulos cobertos |
| `doc/onboarding/como_executar.md` | Instalação, variáveis e comandos Robot |
| `doc/onboarding/contribuindo.md` | Passo a passo para novos testes + checklist |
| `doc/arquitetura/lkdf.md` | As 6 camadas LKDF, regras e cadeia completa |
| `doc/arquitetura/estrutura_diretorios.md` | Árvore de diretórios comentada |
| `doc/convencoes/nomenclatura.md` | Prefixos, Gherkin, TESTE:, tags, arquivos |
| `doc/convencoes/locators.md` | Estratégia de seletor e agrupamento |
| `doc/convencoes/data_test.md` | @{list}, &{dict} e proibições inline |
| `doc/modulos/{modulo}.md` | Cards, seções e regras ativas por módulo |
"""

_TASK_ANALYZE = """\
## Tarefa

Analise a história abaixo e produza:

1. **Objetivo** — o que o usuário final precisa
2. **Módulo(s) afetado(s)** — com base no registro de módulos
3. **Critérios de aceite** — lista numerada, cada um mapeável a um caso de teste
4. **Regras de negócio** — novas ou alteradas
5. **Regras descontinuadas** — comportamentos que deixam de valer
6. **Riscos de QA** — regressões prováveis, integrações afetadas
7. **Tags sugeridas** — para organização dos testes
8. **Mapeamento LKDF** — quais arquivos das 4 camadas serão criados/alterados

> Após a análise, **pergunte ao usuário** em qual projeto Robot Framework os \
testes devem ser criados (caminho completo da raiz do projeto).
"""

_TASK_GENERATE = """\
## Tarefa

Com base na análise da história e no contexto de conhecimento acima, gere os \
arquivos Robot Framework completos seguindo LKDF.

Para **cada arquivo**, apresente:
1. O caminho completo relativo à raiz do projeto alvo (ex: `test_suites/home/bsag-90.robot`)
2. O conteúdo completo em bloco de código

> **Antes de gerar**: confirme com o usuário o caminho raiz do projeto Robot Framework \
onde os arquivos serão criados.
"""

_TASK_DOM = """\
## Tarefa

Analise o snapshot DOM abaixo e produza:

1. **Módulo detectado** — com base no conteúdo da página
2. **Contrato DOM** — headings, botões, campos, tabelas encontrados
3. **Mudanças detectadas** — comparar com o contrato anterior (se fornecido)
   - `BREAKING`: elemento removido ou locator alterado (testes vão falhar)
   - `RISCO`: elemento movido ou renomeado
   - `INFO`: novo elemento (oportunidade de cobertura)
4. **Locators sugeridos** — priorizando `data-testid > aria-label > role > CSS semântico`
5. **Impacto nos testes** — quais arquivos `.robot`/`.resource` precisam ser atualizados

> Após a análise, **pergunte ao usuário** o caminho do projeto Robot Framework \
para indicar os arquivos exatos a atualizar.
"""

_TASK_KNOWLEDGE = """\
## Tarefa

Responda à consulta abaixo com base exclusivamente no contexto de conhecimento fornecido acima.
Cite as fontes (arquivo e seção) de onde extraiu a informação.
Se a informação não existir na base, informe claramente e sugira o que registrar.
"""


class AQuAPromptBuilder:
    """Monta prompts contextualizados para uso no chat."""

    def __init__(self, knowledge_root: Path) -> None:
        self.knowledge_root = Path(knowledge_root)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def story_context(
        self,
        story_text: str,
        story_id: str = "",
        module: str = "",
        task: str = "analyze",
    ) -> str:
        """Prompt completo para análise ou geração de testes de uma história."""
        parts = [_AQUA_HEADER]

        knowledge = self._load_knowledge(scope="all", hint_module=module)
        if knowledge:
            parts.append("## Base de conhecimento\n\n" + knowledge)

        parts.append("## História\n")
        if story_id:
            parts.append(f"**ID:** {story_id}\n")
        if module:
            parts.append(f"**Módulo:** {module}\n")
        parts.append(story_text.strip())

        task_section = _TASK_GENERATE if task == "generate" else _TASK_ANALYZE
        parts.append(task_section)

        return "\n\n---\n\n".join(parts)

    def dom_context(
        self,
        module: str,
        html_snippet: str,
        story_id: str = "",
        previous_contract: dict | None = None,
    ) -> str:
        """Prompt para análise de snapshot DOM."""
        parts = [_AQUA_HEADER]

        module_info = self._load_module_info(module)
        if module_info:
            parts.append(f"## Módulo: {module}\n\n{module_info}")

        if previous_contract:
            parts.append(
                "## Contrato DOM anterior\n\n```json\n"
                + json.dumps(previous_contract, ensure_ascii=False, indent=2)
                + "\n```"
            )

        dom_section = f"## Módulo: {module} — Snapshot HTML capturado"
        if story_id:
            dom_section += f" (história: {story_id})"
        dom_section += f"\n\n```html\n{html_snippet[:6000]}\n```"
        parts.append(dom_section)

        parts.append(_TASK_DOM)
        return "\n\n---\n\n".join(parts)

    def knowledge_context(self, query: str, scope: str = "all") -> str:
        """Prompt para consulta à base de conhecimento."""
        parts = [_AQUA_HEADER]

        knowledge = self._load_knowledge(scope=scope)
        if knowledge:
            parts.append("## Base de conhecimento\n\n" + knowledge)

        parts.append(f"## Consulta\n\n{query}")
        parts.append(_TASK_KNOWLEDGE)
        return "\n\n---\n\n".join(parts)

    def format_for_terminal(self, prompt: str) -> str:
        """Retorna o prompt formatado para exibição no terminal."""
        separator = "=" * 72
        return f"\n{separator}\n{prompt}\n{separator}\n"

    # ------------------------------------------------------------------
    # Internos — carregamento da base de conhecimento
    # ------------------------------------------------------------------

    def _load_knowledge(self, scope: str = "all", hint_module: str = "") -> str:
        parts: list[str] = []
        root = self.knowledge_root

        if scope in ("all", "modules"):
            modules_file = root / "modules_registry.yaml"
            if modules_file.exists():
                parts.append(
                    "### Módulos registrados (`modules_registry.yaml`)\n\n"
                    f"```yaml\n{modules_file.read_text(encoding='utf-8')}\n```"
                )

        if scope in ("all", "stories"):
            stories_file = root / "stories_index.yaml"
            if stories_file.exists():
                parts.append(
                    "### Índice de histórias (`stories_index.yaml`)\n\n"
                    f"```yaml\n{stories_file.read_text(encoding='utf-8')}\n```"
                )

            # Histórias do módulo relevante (máx 3 para não sobrecarregar contexto)
            if hint_module:
                story_texts = self._load_module_stories(hint_module, max_stories=3)
                if story_texts:
                    parts.append(
                        "### Histórias do módulo (para referência de padrões)\n\n"
                        + story_texts
                    )

        if scope in ("all", "rules"):
            rules_dir = root / "rules_delta"
            if rules_dir.exists():
                # Prioriza o módulo sugerido; sem hint carrega até 2 arquivos
                if hint_module:
                    slug = hint_module.lower().replace(" ", "_")
                    candidates = [rules_dir / f"{slug}_rules_delta.md"]
                else:
                    candidates = sorted(rules_dir.glob("*.md"))[:2]
                for f in candidates:
                    if f.exists():
                        parts.append(
                            f"### Rules delta: `{f.name}`\n\n{f.read_text(encoding='utf-8')}"
                        )

        if scope in ("all", "dom"):
            dom_index = root / "dom" / "index.json"
            if dom_index.exists():
                parts.append(
                    "### DOM index\n\n```json\n"
                    + dom_index.read_text(encoding="utf-8")
                    + "\n```"
                )

        return "\n\n".join(parts)

    def _load_module_info(self, module: str) -> str:
        """Carrega informações específicas de um módulo para contexto de DOM."""
        parts: list[str] = []
        root = self.knowledge_root
        module_slug = module.lower().replace(" ", "_")

        # Contract DOM atual se existir
        contract_path = (
            root / "dom" / "modules" / module_slug / "contracts" / "dom_contract.json"
        )
        if contract_path.exists():
            parts.append(
                "**Contrato DOM atual:**\n```json\n"
                + contract_path.read_text(encoding="utf-8")
                + "\n```"
            )

        return "\n\n".join(parts)

    def _load_module_stories(self, module: str, max_stories: int = 3) -> str:
        module_slug = module.lower().replace(" ", "_")
        stories_dir = self.knowledge_root / "stories"
        if not stories_dir.exists():
            return ""

        # Lê índice para filtrar pelo módulo
        index_path = self.knowledge_root / "stories_index.yaml"
        relevant_ids: list[str] = []
        if index_path.exists():
            for line in index_path.read_text(encoding="utf-8").splitlines():
                if f"modulo: {module_slug}" in line:
                    pass  # próxima iteração terá o story_id
                if (
                    "story_id:" in line
                    and relevant_ids
                    and len(relevant_ids) <= max_stories
                ):
                    pass
            # Parse simples: pega story_ids cujo módulo bate
            relevant_ids = self._parse_module_story_ids(
                index_path, module_slug, max_stories
            )

        texts: list[str] = []
        for sid in relevant_ids:
            f = stories_dir / f"{sid}.md"
            if f.exists():
                texts.append(f"#### {sid}\n\n{f.read_text(encoding='utf-8')}")

        return "\n\n".join(texts)

    def _parse_module_story_ids(
        self, index_path: Path, module_slug: str, max_stories: int
    ) -> list[str]:
        ids: list[str] = []
        current_id: str | None = None
        for line in index_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("- story_id:"):
                current_id = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("modulo:") and current_id:
                if stripped.split(":", 1)[1].strip() == module_slug:
                    ids.append(current_id)
                    if len(ids) >= max_stories:
                        break
                current_id = None
        return ids
