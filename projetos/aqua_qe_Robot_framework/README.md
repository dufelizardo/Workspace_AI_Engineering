# AQuA-QE — Robot Framework

**Artificial Quality Assurance — Quality Engineering**

CLI de geração de contexto para automação de testes Robot Framework seguindo a metodologia **LKDF (Layered Keyword-Driven Framework)**. O AQuA-QE monta prompts ricos com a base de conhecimento do projeto e os entrega para o Claude Code, que atua como motor de IA para análise e geração dos arquivos de teste.

Projeto localizado em: `C:\dev\Workspace AI-Engineering\projetos\aqua_qe_Robot_framework`

---

## Como funciona

```
aqua-qe context → prompt.md → cola no Claude Code → Claude gera os arquivos LKDF
```

O AQuA-QE não chama nenhuma API de LLM. Ele organiza e contextualiza o conhecimento do projeto (módulos, histórias, regras, DOM) em um prompt estruturado. O Claude Code lê esse prompt e gera os 6 arquivos da cadeia LKDF no projeto Robot Framework alvo.

---

## Instalação

Este projeto faz parte do **uv workspace** `Workspace AI-Engineering`. Use `uv` — nunca `pip` diretamente.

```powershell
# Na raiz do workspace
uv sync

# Ou instalar apenas este projeto
uv add --package aqua_qe_Robot_framework .
```

Requer Python 3.10+.

---

## Uso

### Gerar contexto de uma história

```bash
aqua-qe context --story-id EDUQ-90 --module home --output scripts/eduq90_context.md
```

Cole o conteúdo de `eduq90_context.md` no chat do Claude Code. O Claude analisa a história e gera os 6 arquivos LKDF.

### Registrar uma nova história

```bash
aqua-qe register --story-id EDUQ-999 --module home --title "[HOME] Nova funcionalidade" --tags "home,smoke"
```

Cria `knowledge/{projeto}/stories/EDUQ-999.md` e adiciona a entrada em `stories_index.yaml`.

### Trabalhar com múltiplos projetos

```bash
# Projeto padrão (projeto_robot_piloto) — não precisa de --project
aqua-qe context --story-id EDUQ-90 --module home

# Outro projeto
aqua-qe --project projeto_adopet context --story-id ADOP-0001 --module home
```

### Registrar snapshot DOM

```bash
aqua-qe --project projeto_adopet dom --module home --html-file snapshot.html --story-id ADOP-0001
```

### Validar cadeia LKDF

```bash
aqua-qe validate --target "C:\dev\Workspace Robot\projeto_adopet" --module home
```

### Consultar a base de conhecimento

```bash
aqua-qe knowledge --scope all
aqua-qe knowledge --query "regras de cards EM BREVE"
```

---

## Projetos registrados

| Projeto | Knowledge base | Projeto Robot alvo | IDs |
|---------|---------------|-------------------|-----|
| `projeto_robot_piloto` | `knowledge/projeto_robot_piloto/` | `C:\dev\projeto_robot_piloto` | EDUQ-* |
| `projeto_adopet` | `knowledge/projeto_adopet/` | `C:\dev\Workspace Robot\projeto_adopet` | ADOP-* |

---

## Estrutura do projeto

```
aqua_qe_Robot_framework/
├── src/aqua_qe/
│   ├── cli.py              # Entry point — comandos: context, register, dom, knowledge, validate
│   ├── config.py           # AQuAConfig — resolve knowledge root por projeto
│   ├── prompt_builder.py   # AQuAPromptBuilder — monta o prompt com metodologia + knowledge + história
│   ├── story_registry.py   # Registro de novas histórias na knowledge base
│   ├── dom_registry.py     # Registro de snapshots DOM com SHA256 e diffs
│   ├── validator.py        # Validação da cadeia LKDF e consistência da knowledge base
│   └── templates.py        # Esqueletos Robot Framework para novos módulos
├── knowledge/
│   ├── projeto_robot_piloto/   # Plataforma B3/BLC — histórias EDUQ
│   │   ├── modules_registry.yaml
│   │   ├── stories_index.yaml
│   │   ├── stories/
│   │   ├── rules_delta/
│   │   └── dom/
│   └── projeto_adopet/         # AdoPet ONG — histórias ADOP
│       ├── modules_registry.yaml
│       ├── stories_index.yaml
│       ├── stories/
│       ├── rules_delta/
│       └── dom/
├── tests/                  # 71 testes unittest
└── scripts/                # Prompts gerados (.md) — não versionar
```

---

## Metodologia LKDF — 6 camadas

O prompt gerado pelo AQuA-QE instrui o Claude a produzir os 6 arquivos da cadeia abaixo:

| Camada | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| **Locators** | `src/resources/locators/{modulo}/` | Apenas `*** Variables ***` com seletores — fonte única de verdade para o DOM |
| **POM** | `src/resources/pom/{modulo}/` | Ações atômicas de UI — importa Locators |
| **Flows** | `src/resources/flows/{modulo}/` | Lógica Gherkin, FOR loops — chama POM |
| **Scenarios** | `src/resources/scenarios/{modulo}/` | Orquestradores `TESTE:` — delegação pura |
| **Data Test** | `src/resources/data_test/` | Keywords que retornam `@{list}` ou `&{dict}` |
| **Test Suite** | `test_suites/{modulo}/` | Casos de teste — importa Scenarios e Data Test |

Dependência unidirecional:
```
Test Suite → Scenarios → Flows → POM → Locators
Test Suite → Data Test → POM → Locators
```

---

## Testes

```bash
uv run pytest tests/ -v
```

71 testes, cobrindo: config, prompt_builder, story_registry, dom_registry, validator, templates.

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework
[github.com/dufelizardo/AQuA-QE-Robot-Framework](https://github.com/dufelizardo/AQuA-QE-Robot-Framework)
