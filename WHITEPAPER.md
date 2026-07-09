# Whitepaper — Workspace AI-Engineering

**Autor:** Eduardo Felizardo Cândido
**Cargo:** Senior QA Automation Engineer | AI-driven Testing | Robot
**Versão:** 1.0
**Data:** Julho 2026

---

## Sumário

1. [Contexto e Motivação](#1-contexto-e-motivação)
2. [AI Engineering vs. Data Science](#2-ai-engineering-vs-data-science)
3. [Princípios de Design](#3-princípios-de-design)
4. [Arquitetura da Stack](#4-arquitetura-da-stack)
5. [Padrões de Aplicação](#5-padrões-de-aplicação)
6. [Observabilidade e Qualidade](#6-observabilidade-e-qualidade)
7. [Modelo Context Protocol (MCP)](#7-model-context-protocol-mcp)
8. [Fluxo de Trabalho](#8-fluxo-de-trabalho)
9. [Decisões de Arquitetura](#9-decisões-de-arquitetura)
10. [Roadmap](#10-roadmap)

---

## 1. Contexto e Motivação

O surgimento de modelos de linguagem de grande escala (LLMs) como Claude, GPT-4o e Gemini criou uma nova disciplina de engenharia de software: **AI Engineering**.

Diferente do aprendizado de máquina tradicional, AI Engineering não exige domínio de álgebra linear, treinamento de modelos ou pipelines de feature engineering. O foco está em **orquestrar modelos já treinados** para resolver problemas de negócio reais por meio de APIs, prompts, agentes e sistemas de recuperação de contexto.

Este workspace foi criado para estruturar o desenvolvimento dessas aplicações com a mesma disciplina aplicada a qualquer projeto de software profissional: controle de versão, testes, tipagem estática, linting e observabilidade.

---

## 2. AI Engineering vs. Data Science

| Dimensão | Data Science | AI Engineering |
|---|---|---|
| **Objetivo** | Explorar dados, gerar insights, treinar modelos | Construir produtos e pipelines sobre modelos prontos |
| **Artefato principal** | Notebook, modelo treinado, relatório | API, agente, pipeline RAG, servidor MCP |
| **Ferramentas centrais** | Jupyter, Pandas, Scikit-learn, PyTorch | LangChain, LangGraph, MCP, FastAPI, Qdrant |
| **Repositório de modelos** | HuggingFace (treino/fine-tune) | HuggingFace (inferência de embeddings) |
| **Infraestrutura** | Clusters de GPU, notebooks gerenciados | Docker, APIs REST, bancos vetoriais, grafos |
| **Perfil técnico** | Estatística, ML, visualização | Engenharia de software, arquitetura de sistemas |

Por isso, **este workspace é separado do Workspace Data Science**: as dependências, os padrões de código e os objetivos são fundamentalmente diferentes.

---

## 3. Princípios de Design

### 3.1 Dependências explícitas por projeto

Cada projeto declara apenas as dependências que usa. O root do workspace fornece apenas utilitários universais. SDKs de providers LLM, bancos vetoriais e frameworks de orquestração são instalados por projeto.

### 3.2 Configuração por variáveis de ambiente

Nenhuma chave de API, URL de banco ou credencial é hardcoded. Toda configuração sensível passa por `.env` (nunca commitado) carregado via `python-dotenv`.

### 3.3 Tipagem estática como contrato

`pydantic` para dados de entrada/saída de agentes e APIs. `basedpyright` em modo `standard` para verificação estática. O tipo é documentação executável.

### 3.4 Testes são cidadãos de primeira classe

Cada projeto tem `tests/` desde o scaffolding. `pytest-cov` mede cobertura. Prompts e chains também são testáveis via injeção de dependência (substituindo a chamada ao LLM por um mock ou resposta fixa).

### 3.5 Observabilidade desde o início

`OpenTelemetry` para traces distribuídos. `LangSmith` para rastreamento de chains e agentes LangChain. `Loguru` para logs estruturados. Uma aplicação que não pode ser observada não pode ser melhorada.

---

## 4. Arquitetura da Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Interface / Entrega                   │
│              FastAPI + Uvicorn  |  Typer CLI             │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                  Camada de Orquestração                  │
│           LangChain  |  LangGraph  |  MCP SDK            │
└──────┬──────────────────┬──────────────────┬────────────┘
       │                  │                  │
┌──────▼──────┐  ┌────────▼────────┐  ┌─────▼──────────┐
│ LLM Provider│  │  Banco Vetorial │  │  Banco de Grafos│
│ OpenAI      │  │  Qdrant         │  │  Neo4j          │
│ Anthropic   │  │  ChromaDB       │  │  (Knowledge     │
│ Groq        │  │  FAISS          │  │   Graph / RAG)  │
│ Ollama      │  └─────────────────┘  └────────────────┘
└─────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│                  Camada de Embeddings                    │
│      sentence-transformers  |  transformers + accelerate │
└─────────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│              Ingestão e Processamento de Docs            │
│    PyMuPDF  |  PyPDF  |  Unstructured  |  BS4  |  lxml  │
└─────────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│                    Infraestrutura                        │
│   Docker  |  PostgreSQL  |  MongoDB  |  Redis  |  Neo4j  │
└─────────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│                    Observabilidade                       │
│        OpenTelemetry  |  LangSmith  |  Loguru            │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Padrões de Aplicação

### 5.1 RAG (Retrieval-Augmented Generation)

Padrão principal para conectar LLMs a bases de conhecimento privadas.

```
Documento → Chunking → Embedding → Banco Vetorial
                                         ↓
Query do usuário → Embedding → Busca vetorial → Contexto relevante
                                                        ↓
                                              LLM + Contexto → Resposta
```

**Stack recomendada:** `pymupdf` + `sentence-transformers` + `qdrant-client` + `anthropic`

### 5.2 Agentes com LangGraph

Para tarefas que requerem planejamento, uso de ferramentas e múltiplos passos.

```
Entrada → [Planner] → [Tool Use] → [Reflection] → [Output]
              ↑              ↓
           Estado        Ferramentas
          (grafo)     (APIs, DBs, código)
```

**Stack recomendada:** `langgraph` + `langsmith` + `openai`

### 5.3 Servidor MCP

Para expor ferramentas e recursos de forma padronizada a clientes MCP (Claude Desktop, Claude Code, etc.).

```
Cliente MCP ←→ Servidor MCP (Python) ←→ Ferramenta/Recurso
```

**Stack recomendada:** `mcp` + `fastapi` (transporte HTTP/SSE)

### 5.4 API de IA

Wrapper de LLMs como serviço interno.

```
Cliente → FastAPI → [Validação Pydantic] → LLM Provider → Resposta
                         ↓
                   [Observabilidade OTel]
```

**Stack recomendada:** `fastapi` + `uvicorn` + `pydantic` + `opentelemetry-sdk`

---

## 6. Observabilidade e Qualidade

### Rastreamento de LLMs

| Ferramenta | Escopo |
|---|---|
| LangSmith | Chains, agentes e retrieval LangChain |
| OpenTelemetry | Traces distribuídos da aplicação inteira |
| Loguru | Logs estruturados locais |

### Pipeline de qualidade de código

```
git commit
    ↓
pre-commit hooks
    ├── ruff (lint + autofix)
    ├── ruff-format
    ├── trailing-whitespace
    ├── end-of-file-fixer
    ├── check-yaml / check-toml
    ├── debug-statements
    └── check-added-large-files (1 MB)
    ↓
basedpyright (type check — CI)
    ↓
pytest + pytest-cov (testes — CI)
```

---

## 7. Model Context Protocol (MCP)

MCP é o protocolo aberto desenvolvido pela Anthropic para padronizar a comunicação entre modelos de linguagem e ferramentas/recursos externos.

### Por que MCP importa para AI Engineering

- **Interoperabilidade:** um servidor MCP funciona com qualquer cliente compatível (Claude, Cursor, VS Code, etc.)
- **Segurança:** o modelo não executa código diretamente; ele invoca ferramentas via protocolo controlado
- **Composabilidade:** servidores MCP podem ser compostos e reutilizados entre projetos

### Padrões de implementação neste workspace

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("nome-servidor")

@app.list_tools()
async def list_tools():
    ...

@app.call_tool()
async def call_tool(name, arguments):
    ...
```

O SDK Python `mcp` é suficiente como ponto de partida para a maioria dos servidores.

---

## 8. Fluxo de Trabalho

### Criar um novo projeto

```powershell
.\novo-projeto.ps1 -Nome "rag-documentos"
```

### Ciclo de desenvolvimento

```
1. Editar pyproject.toml → descomentar deps necessárias
2. uv sync
3. Configurar .env com chaves de API
4. Desenvolver em src/<slug>/
5. Testar com uv run pytest
6. Commitar (pre-commit executa automaticamente)
```

### Executar modelos locais

```bash
ollama serve
ollama pull qwen3              # chat / reasoning
ollama pull nomic-embed-text   # embeddings locais
```

Usar `OLLAMA_BASE_URL=http://localhost:11434` no `.env` do projeto.

---

## 9. Decisões de Arquitetura

### Por que uv e não pip/poetry/conda?

`uv` combina gerenciamento de pacotes, resolução de dependências, virtualenv e workspaces em uma única ferramenta escrita em Rust. É ordens de magnitude mais rápido que pip+venv e mais simples que Poetry para monorepos.

### Por que Qdrant como banco vetorial padrão?

Qdrant é o único banco vetorial open-source com suporte nativo a filtragem por payload + busca vetorial em uma única query, API estável, cliente Python completo e imagem Docker oficial. ChromaDB e FAISS são alternativas válidas para protótipos locais.

### Por que LangGraph e não só LangChain?

LangChain resolve chains lineares. Agentes reais precisam de estado, ramificação, loops e retentativas — estruturas de grafos. LangGraph expõe esse grafo de forma explícita, o que facilita debugging e testes.

### Por que Pydantic v2 como base?

LangChain, FastAPI e praticamente todo ecossistema moderno Python usa Pydantic v2. Usá-lo no root garante que não há conflito de versão entre projetos e que o modelo de dados é compatível com todos os frameworks.

### Por que OpenTelemetry e não apenas logs?

Logs são suficientes para debugging local. Em sistemas distribuídos com múltiplos serviços, agentes e chamadas a LLMs, traces distribuídos são necessários para entender latência, falhas e comportamento agregado.

---

## 10. Roadmap

| Item | Status | Descrição |
|---|---|---|
| Workspace base | ✅ Concluído | uv workspace, pyproject.toml, pre-commit, .vscode |
| Template de projeto | ✅ Concluído | Scaffolding via `novo-projeto.ps1` |
| Projeto RAG (`rag-documentos`) | ✅ Iniciado | Scaffold criado; pipeline: ingestão → embedding → Qdrant → query |
| Projeto Agente | Planejado | Agente LangGraph com ferramentas e LangSmith |
| Servidor MCP | Planejado | MCP server Python expondo recursos do workspace |
| API de IA | Planejado | FastAPI wrapper com autenticação e OTel |
| CI/CD template | Planejado | GitHub Actions: lint + type check + testes |

---

*Eduardo Felizardo Cândido*
*Senior QA Automation Engineer | AI-driven Testing | Robot*
