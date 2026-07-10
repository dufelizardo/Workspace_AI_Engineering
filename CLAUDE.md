# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos essenciais

```powershell
# Instalar/sincronizar dependências (raiz ou após editar qualquer pyproject.toml)
uv sync

# Criar novo projeto a partir do template
.\novo-projeto.ps1 -Nome "nome-do-projeto"

# Adicionar dependência a um projeto específico
uv add <pacote> --package <nome-projeto>

# Rodar testes de um projeto
cd projetos/<nome>
uv run pytest

# Rodar teste único
uv run pytest tests/test_foo.py::test_bar

# Lint + autofix
uv tool run ruff check . --fix

# Formatação
uv tool run ruff format .

# Type check
uv tool run basedpyright

# Pre-commit em todos os arquivos (sem fazer commit)
uv tool run pre-commit run --all-files
```

## Estrutura e arquitetura

Este é um **uv workspace monorepo**. O `pyproject.toml` raiz declara `[tool.uv.workspace] members = ["projetos/*"]` — cada subdiretório em `projetos/` é um pacote Python independente com seu próprio `pyproject.toml` e conjunto de dependências.

O `.venv/` é compartilhado entre todos os projetos. `uv sync` na raiz resolve o lock unificado (`uv.lock`) para todos os membros do workspace.

### Dependências: raiz vs. projeto

O root instala apenas utilitários universais: `pydantic`, `python-dotenv`, `httpx`, `rich`, `loguru`, `typer`, `pytest`, `pytest-cov`. Tudo mais (SDKs de LLM, langchain, qdrant, fastapi, etc.) é declarado no `pyproject.toml` do projeto que o usa — **nunca no root**. O template em `projetos/.template/pyproject.toml` lista todos os pacotes opcionais disponíveis como comentários.

### Layout de cada projeto

```
projetos/<nome>/
├── pyproject.toml      ← deps do projeto; pytest com --cov=src por padrão
├── src/<slug>/         ← código-fonte; <slug> = nome com hífens → underscores
│   └── __init__.py
├── tests/
│   └── __init__.py
└── .env                ← gitignored; copiar de .env.example e preencher
```

### Configuração de qualidade (raiz aplica a todos)

- **Ruff:** `line-length = 88`, regras `E W F I UP B C4 SIM RUF`, `ignore = ["E501"]`
- **BasedPyright:** modo `standard`, aponta para `.venv/` do workspace
- **pre-commit:** ruff lint+format → trailing-whitespace → end-of-file → yaml/toml check → debug-statements → large files (1 MB)

## Convenções críticas

- **Nunca usar `pip` diretamente** — apenas `uv add`, `uv sync`, `uv run`.
- **`.env` nunca é commitado.** Variáveis de ambiente ficam em `.env` (cada projeto tem o seu, copiado do `.env.example` raiz pelo `novo-projeto.ps1`).
- SDKs de LLM providers (`openai`, `anthropic`, etc.) são instalados **por projeto**, não no root.
- `src/<slug>/` usa o **src layout** — o pacote não está na raiz do projeto, então `uv run` é necessário para que o Python encontre o módulo nos testes.
- Hífens no nome do projeto viram underscores no slug do pacote (`meu-agente` → `src/meu_agente/`).
- **Versionamento de projetos está fechado.** `projetos/*` está no `.gitignore`; as únicas exceções são `.template` e `rag-documentos`, já liberadas. Nenhum projeto novo deve receber exceção no `.gitignore` — todo projeto criado a partir de agora recebe `git init` próprio e repositório separado, sem exceção. Nunca remover o `.git` de um projeto independente para incluí-lo aqui sem autorização explícita.
- **Projetos versionados aqui:** `.template`, `rag-documentos`.
