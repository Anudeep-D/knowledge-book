# Design: Track 05 Unstructured Data Governance, Quality, & Compliance

## Context

See `proposal.md` for motivation. Track 05 builds upon the foundation established in Tracks 01-04 (infrastructure, embedding geometry, data layers, and agent orchestration). Unstructured data governance requires bridging raw object storage (S3/lakehouses) with high-dimensional embedding spaces (vector DBs) while enforcing strict privacy, security, and quality invariants. All modules must adhere to the 4-part pedagogical contract defined in `openspec/specs/module-contract/spec.md`.

## Goals / Non-Goals

**Goals:**
- Provide a rigorous, four-module curriculum detailing the complete lifecycle of unstructured data governance for enterprise AI.
- Design real-world architectures showing control plane and data plane separation for discovery, quality hygiene, privacy sanitization, and vector unlearning.
- Deliver production-ready, runnable companion Python 3.12+ scripts, Pydantic V2 models, OPA/Rego gatekeeper policies, and OpenLineage emitters.
- Include operational runbooks, failure mode post-mortems, and trade-off matrices for each module.

**Non-Goals:**
- Implementing a production SaaS governance vendor product or proprietary data governance UI.
- Rewriting core vector database indexing engines (e.g., C++ HNSW implementations); we model and script against client interfaces (Milvus, Qdrant, OpenSearch).
- Replacing general NLP data cleaning libraries with proprietary algorithms; we leverage standard open-source tools (Presidio, MinHash, Tesseract, OpenLineage).

## Decisions

### Decision 1: Shannon Character Entropy as Ingestion Gatekeeper
- **Choice:** Evaluate character Shannon entropy ($3.0 \le H(X) \le 5.8$) and MIME sniffing before passing raw blobs to chunking or VLM parsing.
- **Rationale:** Processing corrupted scans or encrypted binaries through LLM/VLM chunkers wastes massive GPU compute. Entropy calculation is $O(N)$ over raw bytes and runs in sub-millisecond CPU time.
- **Alternatives Considered:** 
  - *LLM-based classification at ingress:* Prohibitive cost and latency ($>500$ms/doc at scale).
  - *File extension inspection only:* Trivial to spoof; misses polyglot files and corrupted OCR artifacts.

### Decision 2: Two-Tier Syntactic (MinHash) + Semantic (SemDeDup) Deduplication
- **Choice:** First pass with MinHash LSH ($Jaccard \ge 0.85$) to prune exact and near-exact document duplicates on CPU, followed by SemDeDup intra-cluster cosine pruning ($Cosine \ge 0.92$) on dense embeddings.
- **Rationale:** MinHash eliminates 40-60% of redundant boilerplates before calling expensive embedding models. SemDeDup prunes remaining paraphrased redundancies that hijack Top-$K$ retrieval.
- **Alternatives Considered:**
  - *Pairwise vector cosine over all chunks:* $O(N^2)$ distance computations explode memory and compute for millions of chunks.
  - *Exact SHA-256 deduplication only:* Misses minor formatting, whitespace, and scanned OCR noise variations.

### Decision 3: Entity-Counter Masking (`<PERSON_N>`) with FPE Vault over Generic Redaction
- **Choice:** Mask sensitive entities using positional class tokens (`<PERSON_1>`, `<SSN_1>`) combined with Format-Preserving Encryption (AES-256 SIV) in an isolated key vault.
- **Rationale:** Replacing sensitive terms with generic `<REDACTED>` strings destroys sentence syntax and causes unrelated chunks to collapse into identical vector spaces. Positional tokens preserve syntactic context for embedding models while eliminating raw PII.
- **Alternatives Considered:**
  - *Complete document drop:* Discards valuable domain context.
  - *In-database column encryption:* Ineffective for unstructured semantic search where embeddings must remain queryable.

### Decision 4: Two-Tier Vector Unlearning (Soft Tombstoning + Partition Compaction)
- **Choice:** Comply with GDPR Article 17 via immediate payload erasure and query-time bitset tombstoning (`tombstone == false`), paired with scheduled offline graph re-indexing / partition compaction.
- **Rationale:** Directly rewiring graph edges (HNSW) in real time fragments the graph index and causes $O(N \log N)$ compute spikes during peak hours. Tombstone bitsets enforce sub-millisecond exclusion with zero recall degradation.
- **Alternatives Considered:**
  - *Immediate graph deletion with edge rewiring:* Causes catastrophic query latency degradation during deletion bursts.
  - *Full index rebuild per deletion request:* Operationally impossible for high-volume deletion traffic.

### Decision 5: Layout-Aware OCR Validation & Indirect Prompt-Injection Filtering
- **Choice:** Enforce image Laplacian variance ($\ge 100$) and bounding-box 2D grid checks to prevent table flattening, coupled with regex/zero-width character stripping for indirect prompt injections.
- **Rationale:** 2D financial tables are routinely corrupted by naive 1D text chunkers, and ingested documents are an active attack vector for data poisoning and system prompt hijacking.

## Risks / Trade-offs

- **[Risk] High MinHash Shingling Memory Overhead** → *Mitigation:* Use 32-bit MurmurHash3 shingle representations and fixed-size 128-dimension MinHash signatures.
- **[Risk] False-Positive PII Masking on Technical Terms** → *Mitigation:* Provide customizable Presidio `PatternRecognizer` exemptions for domain-specific acronyms and entity IDs.
- **[Risk] Tombstone Accumulation Causing Memory Bloat in Vector RAM** → *Mitigation:* Implement automated threshold-based compaction jobs when tombstoned vectors exceed 5% of collection capacity.
- **[Risk] False Rejection of Technical Code by Entropy Gate** → *Mitigation:* Provide MIME-type bypass policies for structured code (`application/json`, `text/x-yaml`).

## Migration Plan

1. Update `shared/scripts/validate-module.py` to register `05-unstructured-data-governance` in `VALID_TRACKS`.
2. Scaffold `tracks/05-unstructured-data-governance/` with the syllabus `README.md`.
3. Sequentially author Modules 01, 02, 03, and 04 alongside companion Python scripts, OPA policies, and JSON schemas.
4. Run `python3 shared/scripts/validate-module.py --path tracks/05-unstructured-data-governance/<module-dir>` across all four modules to verify compliance with the module contract.
