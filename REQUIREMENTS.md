# Requirements

Catálogo completo de dependências do **Workspace AI-Engineering**.

As dependências do root (`pyproject.toml` raiz) são instaladas em todos os projetos.
As demais são **opcionais** e devem ser adicionadas apenas ao projeto que as utiliza.

---

## Dependências base (root)

Instaladas via `uv sync` na raiz do workspace. Disponíveis em todos os projetos.

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `pydantic` | `>=2.0` | Modelagem e validação de dados com type hints |
| `python-dotenv` | `>=1.0` | Carregamento de variáveis de ambiente a partir de `.env` |
| `httpx` | `>=0.28` | Cliente HTTP assíncrono e síncrono |
| `rich` | `>=13.0` | Output formatado no terminal (tabelas, progresso, logs) |
| `loguru` | `>=0.7` | Logging estruturado com sink configurável |
| `typer` | `>=0.15` | CLIs com type hints; baseado em Click |
| `pytest` | `>=8.0` | Framework de testes |
| `pytest-cov` | `>=6.0` | Cobertura de código integrada ao pytest |

---

## LLM Providers

Instalar somente o provider utilizado no projeto.

| Pacote | Versão mínima | Provider |
|---|---|---|
| `openai` | `>=1.0` | OpenAI (GPT-4o, o3, embeddings) |
| `anthropic` | `>=0.50` | Anthropic (Claude 3.5/4) |
| `google-genai` | `>=1.0` | Google (Gemini) |
| `groq` | `>=0.11` | Groq (Llama 3, Mixtral — inferência rápida) |
| `mistralai` | `>=1.0` | Mistral AI |

```bash
uv add openai --package <nome-projeto>
```

---

## Orquestração

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `langchain` | `>=0.3` | Abstrações para chains, retrievers e tool use |
| `langgraph` | `>=0.2` | Agentes stateful baseados em grafos de estado |
| `langsmith` | `>=0.2` | Observabilidade e rastreamento de chains LangChain |

```bash
uv add langchain langgraph langsmith --package <nome-projeto>
```

---

## Model Context Protocol (MCP)

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `mcp` | `>=1.0` | SDK oficial para servidores e clientes MCP em Python |

```bash
uv add mcp --package <nome-projeto>
```

---

## Embeddings

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `sentence-transformers` | `>=3.0` | Modelos de embedding de texto (local) |
| `transformers` | `>=4.45` | Acesso a modelos HuggingFace |
| `accelerate` | `>=1.0` | Aceleração de inferência (GPU/CPU otimizado) |

```bash
uv add sentence-transformers transformers accelerate --package <nome-projeto>
```

---

## Banco Vetorial

| Pacote | Versão mínima | Backend | Observação |
|---|---|---|---|
| `qdrant-client` | `>=1.12` | Qdrant | Recomendado para produção; suporte a Docker |
| `chromadb` | `>=0.5` | ChromaDB | Simples, bom para protótipos locais |
| `faiss-cpu` | `>=1.9` | FAISS (Meta) | Busca vetorial em memória; sem persistência nativa |

```bash
uv add qdrant-client --package <nome-projeto>
```

---

## Banco de Grafos

| Pacote | Versão mínima | Backend |
|---|---|---|
| `neo4j` | `>=5.0` | Neo4j (GraphRAG, Knowledge Graph) |

```bash
uv add neo4j --package <nome-projeto>
```

---

## Banco de Dados Relacional / NoSQL

Instalar somente os drivers utilizados.

| Pacote | Versão mínima | Backend |
|---|---|---|
| `sqlalchemy` | `>=2.0` | ORM e query builder (suporte a múltiplos bancos) |
| `psycopg[binary]` | `>=3.0` | Driver PostgreSQL assíncrono (psycopg3) |
| `oracledb` | `>=2.0` | Driver Oracle Database |
| `pymongo` | `>=4.0` | Driver MongoDB |
| `redis` | `>=5.0` | Cliente Redis (cache, pub/sub, filas) |

```bash
uv add sqlalchemy psycopg --package <nome-projeto>
```

---

## API

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `fastapi` | `>=0.115` | Framework de API assíncrona com validação automática |
| `uvicorn[standard]` | `>=0.32` | Servidor ASGI para FastAPI |

```bash
uv add fastapi "uvicorn[standard]" --package <nome-projeto>
```

---

## Observabilidade

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `opentelemetry-api` | `>=1.28` | API padrão de instrumentação (traces, métricas, logs) |
| `opentelemetry-sdk` | `>=1.28` | Implementação do SDK OpenTelemetry |

```bash
uv add opentelemetry-api opentelemetry-sdk --package <nome-projeto>
```

---

## Processamento de Documentos

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `pypdf` | `>=5.0` | Leitura e extração de texto de PDFs |
| `pymupdf` | `>=1.24` | Extração avançada de PDFs (texto, imagens, tabelas) |
| `unstructured` | `>=0.15` | Ingestão de documentos de múltiplos formatos (Word, PPT, HTML…) |
| `beautifulsoup4` | `>=4.12` | Parsing de HTML/XML |
| `lxml` | `>=5.0` | Parser de alto desempenho para HTML/XML |

```bash
uv add pymupdf beautifulsoup4 --package <nome-projeto>
```

---

## Dados

| Pacote | Versão mínima | Finalidade |
|---|---|---|
| `pandas` | `>=2.2` | Manipulação tabular de dados |
| `numpy` | `>=2.0` | Operações numéricas e vetoriais |

```bash
uv add pandas numpy --package <nome-projeto>
```

---

## Ferramentas globais (uv tool)

Instaladas globalmente na máquina, não no venv do workspace.

| Ferramenta | Finalidade |
|---|---|
| `ruff` | Linter + formatter Python (substitui flake8, isort, black) |
| `basedpyright` | Type checker estático (fork do Pyright com modo strict aprimorado) |
| `pre-commit` | Orquestrador de hooks de pré-commit |

```bash
uv tool install ruff
uv tool install basedpyright
uv tool install pre-commit
```

---

*Eduardo Felizardo Cândido*
*Senior QA Automation Engineer | AI-driven Testing | Robot*
