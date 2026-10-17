# Tasks: Track 04 Orchestration & Agent Workflows Implementation

## 1. Syllabus Roadmap Alignment

- [x] 1.1 Update `tracks/04-agentic-workflows/README.md` to reflect the 4-module curriculum roadmap and verify frontmatter and markdown links.

## 2. Module 02: Data & Workflow Orchestration with Prefect

- [x] 2.1 Scaffold `tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect/` directory with `diagrams/` and `artifacts/`.
- [x] 2.2 Implement `artifacts/prefect_rag_pipeline.py` with dynamic task mapping (`.map()`), content-hash task caching, and exponential jitter backoff, and verify script runs.
- [x] 2.3 Create `artifacts/prefect_job_template.yaml` for Kubernetes work pools with resource limits, GPU affinities, and non-root security contexts.
- [x] 2.4 Author `02-data-workflow-orchestration-prefect/index.md` satisfying the 4-part module contract, and verify with `python3 shared/scripts/validate-module.py --path tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect`.

## 3. Module 03: Agentic Topologies & Cyclic State Machines (LangGraph)

- [x] 3.1 Scaffold `tracks/04-agentic-workflows/03-agentic-topologies-state-machines/` directory with `diagrams/` and `artifacts/`.
- [x] 3.2 Implement `artifacts/supervisor_langgraph.py` with typed state reducers, structured router schema, and recursion guards, and verify execution.
- [x] 3.3 Implement `artifacts/hitl_checkpoint_agent.py` demonstrating `MemorySaver` persistence, `interrupt_before`, and state mutation, and verify execution.
- [x] 3.4 Author `03-agentic-topologies-state-machines/index.md` satisfying the 4-part module contract, and verify with `python3 shared/scripts/validate-module.py --path tracks/04-agentic-workflows/03-agentic-topologies-state-machines`.

## 4. Module 04: Production Guardrails & Evals

- [x] 4.1 Scaffold `tracks/04-agentic-workflows/04-production-guardrails-evals/` directory with `diagrams/` and `artifacts/`.
- [x] 4.2 Implement `artifacts/guarded_schema_repair.py` featuring Pydantic v2 strict models, SQL injection regex validators, and LLM self-correction repair loops, and verify execution.
- [x] 4.3 Implement `artifacts/evals_otel_harness.py` with OpenTelemetry GenAI semantic tracing spans and the RAG Triad assertion test suite, and verify execution.
- [x] 4.4 Author `04-production-guardrails-evals/index.md` satisfying the 4-part module contract, and verify with `python3 shared/scripts/validate-module.py --path tracks/04-agentic-workflows/04-production-guardrails-evals`.

## 5. Track-Wide Validation & Consistency

- [x] 5.1 Run repository-wide module validator `python3 shared/scripts/validate-module.py --all` and verify all modules in Track 04 pass with zero errors.
