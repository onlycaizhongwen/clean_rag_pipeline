# clean_rag_pipeline

面向企业知识库的 **数据清洗与 RAG 检索服务**。项目覆盖文档上传、异步清洗、分块、Embedding、向量入库、混合检索、权限过滤、rerank、诊断观测和演示控制台，适合作为 RAG pipeline、data cleaning service、knowledge base search、document ingestion、hybrid retrieval 的 PoC 或工程化参考。

## 关键词

RAG, Retrieval-Augmented Generation, data cleaning, document ingestion, knowledge base, semantic search, keyword search, hybrid search, vector database, Qdrant, FastAPI, RabbitMQ, MinIO, PostgreSQL, BGE embedding, BGE reranker, DashScope embedding, Vue console, enterprise search, permission filtering, audit trail, diagnostics.

## 核心能力

- 文档入库：支持文件上传、对象存储、清洗任务创建、异步 Worker 消费。
- 文档处理：解析、基础清洗、段落分块、Embedding 生成、Qdrant 向量写入。
- RAG 检索：支持 `semantic`、`keyword`、`hybrid` 三种检索模式，包含召回、预排序、去重、打散和 top-k 输出。
- Rerank：支持 `disabled`、`mock`、`external` provider，可接入本地 BGE reranker 服务。
- 权限与租户：支持 tenant、knowledge base、permission tags 和可信 Header 上下文。
- 文档生命周期：支持删除、更新、重建、批处理、任务重试、操作锁和审计事件。
- 诊断观测：提供 API 指标、搜索诊断事件、任务状态概览和本地验证脚本。
- 演示控制台：Vue 3 + Vite 前端，用于演示上传、清洗、检索、rerank 切换和诊断摘要。

## 架构组件

| 路径 | 说明 |
| --- | --- |
| `services/api` | FastAPI 控制面，提供上传、文档、任务、检索、诊断、指标和运行时配置 API。 |
| `services/worker` | Python 清洗 Worker，消费 RabbitMQ 任务并写入 PostgreSQL、MinIO、Qdrant。 |
| `services/reranker` | 可选本地 BGE reranker 服务，兼容 API 的 external rerank contract。 |
| `services/console` | Vue 演示控制台。 |
| `infra` | Docker Compose 本地基础设施与数据库初始化脚本。 |
| `scripts` | smoke、demo、权限、rerank、诊断、负载和模型评估脚本。 |
| `samples` | 示例文档和检索评估 query。 |
| `docs/codex/v1` | 需求、设计、计划、trace 报告和运维资料。 |

## 技术栈

- API: Python 3.12, FastAPI, SQLAlchemy, Alembic, httpx
- Worker: Python 3.12, pika, MinIO SDK, Qdrant client, pypdf, pandas, python-docx
- Reranker: FastAPI, sentence-transformers, `BAAI/bge-reranker-base`
- Frontend: Vue 3, Vite, TypeScript
- Infrastructure: PostgreSQL, RabbitMQ, MinIO, Qdrant, Docker Compose
- Embedding providers: deterministic mock, DashScope, local BGE through Ollama-compatible endpoint

## 快速启动

本地默认使用 Docker Compose 启动 API、Worker 和基础设施。Windows PowerShell 示例：

```powershell
Copy-Item .env.local.example .env
docker compose -f infra/docker-compose.yml build api worker
docker compose -f infra/docker-compose.yml up -d
.\scripts\db-migrate.ps1
.\scripts\smoke-test.ps1
```

常用本地地址：

- API health: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- RabbitMQ console: `http://localhost:15672`
- MinIO console: `http://localhost:9001`
- Qdrant dashboard: `http://localhost:6333/dashboard`

## 启动演示控制台

```powershell
cd services\console
npm install
npm run dev
```

打开：

```text
http://localhost:5173
```

控制台默认代理 `/health` 和 `/api/*` 到 `http://localhost:8000`。

## 常用验证脚本

```powershell
.\scripts\smoke-test.ps1
.\scripts\demo-eval.ps1
.\scripts\phase2-eval.ps1
.\scripts\permission-test.ps1
.\scripts\diagnostics-test.ps1
.\scripts\bge-rerank-test.ps1
.\scripts\model-eval.ps1
.\scripts\search-load-test.ps1
```

更多基础设施、Embedding provider 和 BGE reranker 配置见 `infra/README.md`。

## API 入口

主要接口前缀：

- `/api/v1/ingestions`：文档上传与入库
- `/api/v1/documents`：文档删除、更新、重建、审计
- `/api/v1/document-batches`：批处理
- `/api/v1/jobs`：清洗任务查询与重试
- `/api/v1/rag/search`：RAG 检索
- `/api/v1/diagnostics`：诊断概览
- `/api/v1/metrics`：API 指标
- `/api/v1/runtime-config`：演示环境运行时配置

检索请求支持的关键参数包括 `query`、`tenant_id`、`knowledge_base_ids`、`permission_context`、`search_mode`、`top_k`、`recall_size`、`pre_rank_size`、`rerank_enabled` 和 `rerank_size`。

## 配置文件

- `.env.example`：基础本地配置模板。
- `.env.local.example`：本地 PoC 推荐配置，默认使用 local BGE embedding + mock rerank。
- `.env.test.example`：测试环境模板。
- `.env.prod.example`：生产环境模板。

生产或客户环境应重点确认数据库、对象存储、消息队列、向量库、Embedding provider、rerank provider、认证模式和权限策略配置。

## 文档索引

- API 契约：`docs/codex/v1/plans/data-cleaning-rag-api-contract.md`
- 架构设计：`docs/codex/v1/designs/data-cleaning-rag-architecture-design.md`
- 部署运维：`docs/codex/v1/plans/数据清洗与RAG服务部署运维说明.md`
- 问题排查：`docs/codex/v1/plans/数据清洗与RAG服务问题排查手册.md`
- 发布检查：`docs/codex/v1/plans/数据清洗与RAG服务发布检查清单.md`
- 演示控制台：`services/console/README.md`
- 本地基础设施：`infra/README.md`

## 当前定位

该仓库当前定位为数据清洗与 RAG 服务的工程化 MVP / PoC 基线，已覆盖端到端入库检索、生产可控性增强、权限上下文、rerank 容量验证和演示控制台。后续可继续扩展客户真实语料评测、隔离恢复演练、CI/CD 发布流水线和更完整的生产权限体系。
