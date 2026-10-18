# Enterprise Engineering Knowledge Book

An interactive, production-grade engineering knowledge base and curriculum modeled after interactive platforms like Educative.io. Built with first-principles mental models, visual control plane / data plane topologies, real-world Python and Kubernetes/OpenShift artifacts, and failure mode blast radius analysis.

---

## Curriculum Taxonomy

The knowledge book is structured across five foundational tracks comprising 20 production-grade modules:

```
+---------------------------------------------------------------------------------------------------+
|                              ENTERPRISE KNOWLEDGE BOOK TAXONOMY                                   |
+---------------------------------------------------------------------------------------------------+
|  Track 01: Cloud-Native Infrastructure & Platform Engineering                                     |
|  Track 02: AI Models, Serving, & Inference Engineering                                            |
|  Track 03: Modern Data Layers & Storage Systems                                                   |
|  Track 04: Agentic Workflows & Multi-Agent Architectures                                          |
|  Track 05: Unstructured Data Governance, Quality, & Compliance                                    |
+---------------------------------------------------------------------------------------------------+
```

### Curriculum Summary Matrix

| Track | Modules | Level | Focus & Technologies | Syllabus Directory |
| :--- | :---: | :---: | :--- | :--- |
| **Track 01: Cloud-Native Infrastructure & Platform Engineering** | 5 | L300 – L400 | Kubernetes, OpenShift SCC, KEDA, Envoy xDS, FastAPI, Redis, Kafka | [`tracks/01-cloud-native-infra/`](./tracks/01-cloud-native-infra/) |
| **Track 02: AI Models, Serving, & Inference Engineering** | 4 | L400 | Model Routing, MRL Embeddings, Parent-Child Chunking, Multimodal, ColPali | [`tracks/02-ai-models-inference/`](./tracks/02-ai-models-inference/) |
| **Track 03: Modern Data Layers & Storage Systems** | 3 | L400 | HNSW / IVF-PQ Vector Indexes, Apache Iceberg, Delta Lake, 4-Tier Memory | [`tracks/03-modern-data-layers/`](./tracks/03-modern-data-layers/) |
| **Track 04: Agentic Workflows & Multi-Agent Architectures** | 4 | L300 – L400 | LangGraph State Graphs, Prefect 3.0, Pydantic v2, Circuit Breakers, OTEL | [`tracks/04-agentic-workflows/`](./tracks/04-agentic-workflows/) |
| **Track 05: Unstructured Data Governance, Quality, & Compliance** | 4 | L300 | Shannon Entropy, MinHash LSH, Microsoft Presidio, OPA/Rego, GDPR Unlearning | [`tracks/05-unstructured-data-governance/`](./tracks/05-unstructured-data-governance/) |

---

## Track 01: Cloud-Native Infrastructure & Platform Engineering

Located in [`tracks/01-cloud-native-infra/`](./tracks/01-cloud-native-infra/):

1. **[`01-modern-system-design-microservices`](./tracks/01-cloud-native-infra/01-modern-system-design-microservices/)**: Scalability boundaries, Shared-Nothing architecture, idempotency in Python/FastAPI with Redis, and asynchronous event decoupling over Kafka.
   - *Key Artifact:* [`idempotent_ingress.py`](./tracks/01-cloud-native-infra/01-modern-system-design-microservices/artifacts/idempotent_ingress.py)
2. **[`02-python-architectural-patterns-control-loops`](./tracks/01-cloud-native-infra/02-python-architectural-patterns-control-loops/)**: Factory, Strategy (`typing.Protocol`), and Observer patterns alongside Kubernetes-style level-triggered reconciliation loops.
   - *Key Artifact:* [`reconciler_control_loop.py`](./tracks/01-cloud-native-infra/02-python-architectural-patterns-control-loops/artifacts/reconciler_control_loop.py)
3. **[`03-pods-clusters-openshift-security`](./tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/)**: Container cgroups v2/namespaces, container lifecycle hooks, OpenShift Security Context Constraints (`restricted-v2`), dynamic UID allocations, and edge routes.
   - *Key Artifacts:* [`openshift-deployment.yaml`](./tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/artifacts/openshift-deployment.yaml), [`openshift-route.yaml`](./tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/artifacts/openshift-route.yaml)
4. **[`04-keda-event-driven-autoscaling`](./tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/)**: Event-driven horizontal autoscaling, external metric scalers, scale-to-zero, flapping stabilization, and downstream pool protection.
   - *Key Artifacts:* [`scaledobject-prometheus.yaml`](./tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/artifacts/scaledobject-prometheus.yaml), [`triggerauth.yaml`](./tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/artifacts/triggerauth.yaml), [`deployment.yaml`](./tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/artifacts/deployment.yaml)
5. **[`05-control-plane-data-plane-separation`](./tracks/01-cloud-native-infra/05-control-plane-data-plane-separation/)**: Architectural decoupling invariants, Envoy xDS dynamic route distribution, etcd Raft consensus preservation, and resilient local route cache workers.
   - *Key Artifact:* [`local_route_cache.py`](./tracks/01-cloud-native-infra/05-control-plane-data-plane-separation/artifacts/local_route_cache.py)

---

## Track 02: AI Models, Serving, & Inference Engineering

Located in [`tracks/02-ai-models-inference/`](./tracks/02-ai-models-inference/):

1. **[`01-model-taxonomy-selection`](./tracks/02-ai-models-inference/01-model-taxonomy-selection/)**: Foundation model taxonomy (Fast 8B vs Reasoning o-Series vs VLM vs LoRA), dynamic entropy routing, latency/cost SLAs, and fallback cascades.
   - *Key Artifacts:* [`router.py`](./tracks/02-ai-models-inference/01-model-taxonomy-selection/artifacts/router.py), [`model-router-policy.json`](./tracks/02-ai-models-inference/01-model-taxonomy-selection/artifacts/model-router-policy.json)
2. **[`02-embeddings-vector-space`](./tracks/02-ai-models-inference/02-embeddings-vector-space/)**: High-dimensional hypersphere geometry, Matryoshka Representation Learning (MRL) slicing (1536d $\to$ 512d), L2 normalization, SQ8 scalar quantization, and vector memory cliff mitigation.
   - *Key Artifacts:* [`embedding_pipeline.py`](./tracks/02-ai-models-inference/02-embeddings-vector-space/artifacts/embedding_pipeline.py), [`vector-index-config.json`](./tracks/02-ai-models-inference/02-embeddings-vector-space/artifacts/vector-index-config.json)
3. **[`03-context-windows-chunking`](./tracks/02-ai-models-inference/03-context-windows-chunking/)**: Token dynamics, context boundary rupture prevention, Small-to-Big hierarchical retrieval, parent-child chunk trees, and breadcrumb metadata injection.
   - *Key Artifacts:* [`contextual_chunker.py`](./tracks/02-ai-models-inference/03-context-windows-chunking/artifacts/contextual_chunker.py), [`chunking-rules.json`](./tracks/02-ai-models-inference/03-context-windows-chunking/artifacts/chunking-rules.json)
4. **[`04-multimodal-data-pipelines`](./tracks/02-ai-models-inference/04-multimodal-data-pipelines/)**: Heterogeneous mixed-input ingestion, 2D financial table preservation, text-first VLM decomposition, ColPali visual late-interaction embeddings, and multi-vector retrieval.
   - *Key Artifacts:* [`multimodal_pipeline.py`](./tracks/02-ai-models-inference/04-multimodal-data-pipelines/artifacts/multimodal_pipeline.py), [`multimodal-pipeline.json`](./tracks/02-ai-models-inference/04-multimodal-data-pipelines/artifacts/multimodal-pipeline.json)

---

## Track 03: Modern Data Layers & Storage Systems

Located in [`tracks/03-modern-data-layers/`](./tracks/03-modern-data-layers/):

1. **[`01-vector-databases-ann-search`](./tracks/03-modern-data-layers/01-vector-databases-ann-search/)**: Approximate Nearest Neighbor (ANN) search algorithms (HNSW, IVF-Flat, IVF-PQ), metric geometry (L2, Cosine, Inner Product), SQ8 scalar quantization, and distributed clustering.
   - *Key Artifacts:* [`vector_quantizer.py`](./tracks/03-modern-data-layers/01-vector-databases-ann-search/artifacts/vector_quantizer.py), [`hnsw_pgvector.sql`](./tracks/03-modern-data-layers/01-vector-databases-ann-search/artifacts/hnsw_pgvector.sql)
2. **[`02-lakehouse-iceberg-delta-lake`](./tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/)**: ACID lakehouses on cloud object storage, hierarchical metadata trees vs. Delta transaction logs, Optimistic Concurrency Control (OCC), Merge-on-Read, and snapshot time travel.
   - *Key Artifacts:* [`iceberg_ops.py`](./tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/artifacts/iceberg_ops.py), [`iceberg_schema.sql`](./tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/artifacts/iceberg_schema.sql)
3. **[`03-agent-state-persistence-memory`](./tracks/03-modern-data-layers/03-agent-state-persistence-memory/)**: 4-tier memory pyramid (scratchpad, working, episodic, semantic), Redis distributed mutex leases, PostgreSQL `pgvector` episodic decay scoring, and semantic caching.
   - *Key Artifacts:* [`agent_memory_manager.py`](./tracks/03-modern-data-layers/03-agent-state-persistence-memory/artifacts/agent_memory_manager.py), [`episodic_memory.sql`](./tracks/03-modern-data-layers/03-agent-state-persistence-memory/artifacts/episodic_memory.sql)

---

## Track 04: Agentic Workflows & Multi-Agent Architectures

Located in [`tracks/04-agentic-workflows/`](./tracks/04-agentic-workflows/):

1. **[`01-design-patterns-ai-cloud-native`](./tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/)**: Classic microservice resilience patterns (Circuit Breaker, Strategy, Repository) bridged with agentic coordination patterns (Supervisor-Worker, Evaluator-Optimizer) in Python 3.12+ with Pydantic v2.
   - *Key Artifacts:* [`classic_resilience.py`](./tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/artifacts/classic_resilience.py), [`agentic_patterns.py`](./tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/artifacts/agentic_patterns.py)
2. **[`02-data-workflow-orchestration-prefect`](./tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect/)**: Distributed data orchestration with Prefect 3.0, dynamic task mapping (`.map()`), content-hash caching, Kubernetes work pools, and token concurrency governance.
   - *Key Artifacts:* [`prefect_rag_pipeline.py`](./tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect/artifacts/prefect_rag_pipeline.py), [`prefect_job_template.yaml`](./tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect/artifacts/prefect_job_template.yaml)
3. **[`03-agentic-topologies-state-machines`](./tracks/04-agentic-workflows/03-agentic-topologies-state-machines/)**: Cyclic state graphs with LangGraph, supervisor-worker fan-out/fan-in, actor-model state reducers, checkpoint persistence (PostgreSQL/in-memory), and Human-in-the-Loop (HITL) interrupt approval gates.
   - *Key Artifacts:* [`supervisor_langgraph.py`](./tracks/04-agentic-workflows/03-agentic-topologies-state-machines/artifacts/supervisor_langgraph.py), [`hitl_checkpoint_agent.py`](./tracks/04-agentic-workflows/03-agentic-topologies-state-machines/artifacts/hitl_checkpoint_agent.py)
4. **[`04-production-guardrails-evals`](./tracks/04-agentic-workflows/04-production-guardrails-evals/)**: Pydantic v2 strict schema enforcement, automated LLM self-correction loops, OpenTelemetry GenAI semantic spans, and RAG Triad automated evaluation harnesses.
   - *Key Artifacts:* [`guarded_schema_repair.py`](./tracks/04-agentic-workflows/04-production-guardrails-evals/artifacts/guarded_schema_repair.py), [`evals_otel_harness.py`](./tracks/04-agentic-workflows/04-production-guardrails-evals/artifacts/evals_otel_harness.py)

---

## Track 05: Unstructured Data Governance, Quality, & Compliance

Located in [`tracks/05-unstructured-data-governance/`](./tracks/05-unstructured-data-governance/):

1. **[`01-unstructured-taxonomy-dark-data-discovery`](./tracks/05-unstructured-data-governance/01-unstructured-taxonomy-dark-data-discovery/)**: Unclassified dark data discovery across enterprise cloud storage, character-level Shannon entropy profiling ($3.0 \le H(X) \le 5.8$), MIME sniffing, and Open Policy Agent (OPA/Rego) ingestion gates.
   - *Key Artifacts:* [`taxonomy_router.py`](./tracks/05-unstructured-data-governance/01-unstructured-taxonomy-dark-data-discovery/artifacts/taxonomy_router.py), [`gatekeeper.rego`](./tracks/05-unstructured-data-governance/01-unstructured-taxonomy-dark-data-discovery/artifacts/gatekeeper.rego)
2. **[`02-data-quality-hygiene-curation-pipelines`](./tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines/)**: Two-tier data hygiene, MinHash LSH Jaccard deduplication, SemDeDup semantic centroid pruning, 2D table layout preservation, and OCR blur rejection.
   - *Key Artifacts:* [`deduplication_engine.py`](./tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines/artifacts/deduplication_engine.py), [`multimodal_quality_gate.py`](./tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines/artifacts/multimodal_quality_gate.py), [`chunk-hygiene-rules.json`](./tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines/artifacts/chunk-hygiene-rules.json)
3. **[`03-privacy-redaction-pii-phi-masking`](./tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking/)**: Contextual entity masking (`<PERSON_N>`), Microsoft Presidio integration, Format-Preserving Encryption (FPE) vaults, and adversarial prompt-injection defenses (zero-width character stripping, system prompt override filtering).
   - *Key Artifacts:* [`pii_sanitizer.py`](./tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking/artifacts/pii_sanitizer.py), [`prompt_injection_guard.py`](./tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking/artifacts/prompt_injection_guard.py), [`pii_policy.rego`](./tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking/artifacts/pii_policy.rego)
4. **[`04-compliance-lineage-gdpr-vector-unlearning`](./tracks/05-unstructured-data-governance/04-compliance-lineage-gdpr-vector-unlearning/)**: Regulatory compliance (GDPR/CCPA "Right to be Forgotten"), OpenLineage source-to-vector DAG provenance tracking, soft tombstoning, and HNSW graph compaction for deterministic vector unlearning.
   - *Key Artifacts:* [`lineage_gdpr_manager.py`](./tracks/05-unstructured-data-governance/04-compliance-lineage-gdpr-vector-unlearning/artifacts/lineage_gdpr_manager.py), [`query_enforcement.py`](./tracks/05-unstructured-data-governance/04-compliance-lineage-gdpr-vector-unlearning/artifacts/query_enforcement.py)

---

## Pedagogical Standard & Contract

Every module implements our mandatory 4-part structure:
1. **Interactive Concept Breakdown:** The production crucible ("why before how"), first-principles mental models, and non-negotiable architectural invariants.
2. **Visual Architecture:** Terminal-safe plain ASCII diagrams and interactive Mermaid flowcharts with explicit Control Plane vs. Data Plane splits.
3. **Real-World Code & Configuration:** Production-grade Python 3.12+ reference implementations and hardened Kubernetes, OpenShift, SQL DDL, and Rego policy artifacts.
4. **Edge Cases, Failure Modes & Trade-offs:** Comparative architectural decision matrices, failure blast radius analysis, and emergency SRE triage runbooks.

---

## Repository Structure

```
knowledge-book/
├── README.md                               # Curriculum overview and index (this file)
├── requirements.txt                        # Core Python dependencies
├── shared/
│   └── scripts/
│       └── validate-module.py              # Automated 4-part contract and schema linter
├── templates/
│   └── module-template.md                  # Standard module scaffolding template
├── openspec/                               # OpenSpec change management and specifications
│   ├── config.yaml
│   ├── specs/                              # Formal track and curriculum specifications
│   └── changes/archive/                    # Implemented and archived change proposals
└── tracks/
    ├── 01-cloud-native-infra/              # Track 01 (5 modules + manifests)
    ├── 02-ai-models-inference/             # Track 02 (4 modules + routers & pipelines)
    ├── 03-modern-data-layers/              # Track 03 (3 modules + SQL & storage engines)
    ├── 04-agentic-workflows/               # Track 04 (4 modules + LangGraph & Prefect)
    └── 05-unstructured-data-governance/    # Track 05 (4 modules + Presidio & OPA/Rego)
```

---

## Development & Validation

All modules are strictly validated against the pedagogical contract, frontmatter schema, and asset conventions:

```bash
# Validate all 20 modules across all tracks
python3 shared/scripts/validate-module.py --all

# Validate a specific track
python3 shared/scripts/validate-module.py --track 04-agentic-workflows

# Validate a specific module
python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/01-modern-system-design-microservices
```

### Installation

```bash
uv sync
```
