# Workspace AI-Engineering

Ambiente dedicado ao desenvolvimento de aplicações modernas baseadas em **LLMs, RAG, agentes, MCP e orquestração de IA**.

> **AI Engineering ≠ Data Science.**
> O foco aqui é construir *produtos* sobre modelos de linguagem — pipelines de inferência, agentes autônomos, sistemas RAG, servidores MCP e APIs de IA — não treinar ou explorar dados.

---

## Stack

| Camada | Tecnologias |
|---|---|
| **Base** | Python 3.12, uv, Git, Docker |
| **LLM Providers** | OpenAI, Anthropic, Google GenAI, Groq, Mistral |
| **Orquestração** | LangChain, LangGraph, LangSmith |
| **MCP** | Model Context Protocol SDK |
| **Embeddings** | sentence-transformers, transformers, accelerate |
| **Banco Vetorial** | Qdrant, ChromaDB, FAISS |
| **Banco de Grafos** | Neo4j |
| **Banco de Dados** | SQLAlchemy, psycopg, pymongo, redis |
| **API** | FastAPI, Uvicorn |
| **Configuração** | Pydantic, python-dotenv |
| **Observabilidade** | OpenTelemetry |
| **Documentos** | PyMuPDF, PyPDF, Unstructured, BeautifulSoup4 |
| **Dados** | Pandas, NumPy |
| **Utilitários** | Rich, Loguru, Typer, HTTPX |
| **Qualidade** | Ruff, BasedPyright, Pytest, pre-commit |

---

## Pré-requisitos

Ferramentas instaladas na máquina (não no workspace):

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Git
- Docker Desktop
- Ollama (modelos locais)
- Node.js via `nvm` (ferramentas MCP em JS/TS)
- VS Code

---

## Início rápido

```bash
# 1. Clonar o repositório
git clone <url> "Workspace AI-Engineering"
cd "Workspace AI-Engineering"

# 2. Instalar dependências base
uv sync

# 3. Instalar hooks de qualidade
uv tool run pre-commit install

# 4. Criar um novo projeto
.\novo-projeto.ps1 -Nome "meu-agente"

# 5. Configurar variáveis de ambiente
cp .env.example projetos/meu-agente/.env
# editar projetos/meu-agente/.env com suas chaves de API

# 6. Adicionar dependências ao projeto
cd projetos/meu-agente
# editar pyproject.toml e descomentar as deps necessárias
uv sync
```

---

## Estrutura

```
Workspace AI-Engineering/
├── pyproject.toml              ← workspace root (deps base)
├── uv.lock                     ← lock único para todos os projetos
├── .venv/                      ← virtualenv compartilhado
├── projetos/
│   ├── .template/              ← base para novos projetos
│   └── <nome-projeto>/
│       ├── pyproject.toml      ← deps específicas do projeto
│       ├── src/<slug>/         ← código-fonte
│       ├── tests/              ← testes
│       └── .env                ← variáveis de ambiente (gitignored)
├── novo-projeto.ps1            ← scaffolding
├── .pre-commit-config.yaml
├── .env.example                ← template de variáveis de ambiente
├── .gitignore
├── README.md
├── REQUIREMENTS.md
├── requirements.txt
└── WHITEPAPER.md
```

---

## Criando um novo projeto

```powershell
.\novo-projeto.ps1 -Nome "nome-do-projeto"
```

O script:
1. Copia o template `projetos/.template/` para `projetos/<nome>/`
2. Ajusta o `pyproject.toml` com o nome do projeto
3. Cria `src/<slug>/__init__.py`
4. Copia `.env.example` para `projetos/<nome>/.env`

Após criar o projeto, edite o `pyproject.toml` e descomente apenas as dependências que o projeto precisa, depois execute `uv sync`.

---

## Convenções

- `uv add <pkg> --package <nome>` — adiciona dep em projeto específico
- `uv run pytest` — rodar testes dentro de `projetos/<nome>/`
- `uv sync` — atualiza o venv após alterar qualquer `pyproject.toml`
- Dados sensíveis e modelos grandes são gitignored
- Cada projeto mantém seu próprio `.env` (nunca commitado)
- SDKs de LLM providers são instalados por projeto, não no root

### Versionamento de projetos

Por padrão, `projetos/*` está no `.gitignore` — projetos com escopo independente devem ter seu próprio repositório Git. Projetos que fazem parte do workspace podem ser explicitamente liberados com uma exceção no `.gitignore`:

```gitignore
projetos/*
!projetos/.template
!projetos/rag-documentos   ← exemplo de projeto versionado no workspace
```

**Projetos versionados neste workspace:**

| Projeto | Descrição |
|---|---|
| `.template` | Base para scaffolding de novos projetos |
| `rag-documentos` | Pipeline RAG: ingestão → embedding → Qdrant → query |

**Para projetos com repositório próprio:**

```powershell
cd projetos/<nome>
git init
git remote add origin <url>
git add .
git commit -m "chore: scaffold inicial"
git push -u origin main
```

---

## Modelos locais com Ollama

```bash
ollama serve

ollama pull qwen3
ollama pull llama3.3
ollama pull nomic-embed-text
```

Configure `OLLAMA_BASE_URL=http://localhost:11434` no `.env` do projeto.

---

## VS Code

Abra o workspace raiz no VS Code. As extensões recomendadas estão em `.vscode/extensions.json`.

Para aceitar todas as recomendações: `Ctrl+Shift+P` → *Extensions: Show Recommended Extensions*.

---

*Eduardo Felizardo Cândido*
*Senior QA Automation Engineer | AI-driven Testing | Robot*
