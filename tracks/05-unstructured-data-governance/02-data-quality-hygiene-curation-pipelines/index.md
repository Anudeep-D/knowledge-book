---
id: "02-udg-quality-hygiene-curation"
title: "Data Quality & Hygiene: Deduplication, Chunk Quality, & Multimodal Layout Preservation"
track: "05-unstructured-data-governance"
difficulty: "L300 (Intermediate)"
estimated_minutes: 50
tags:
  - "data-quality"
  - "deduplication"
  - "minhash"
  - "semdedup"
  - "multimodal-curation"
  - "ocr"
---

# Data Quality & Hygiene: Deduplication, Chunk Quality, & Multimodal Layout Preservation

> **Executive Summary:** High retrieval precision in semantic search and RAG systems depends strictly on input data hygiene. Ingesting repetitive legal boilerplates, near-identical document revisions, and flattened 2D tables contaminates vector neighborhoods, causing near-duplicate chunks to crowd out critical bespoke context in Top-$K$ retrieval. By executing two-tier deduplication (syntactic MinHash LSH followed by dense embedding SemDeDup) and enforcing multimodal layout fidelity (Laplacian blur thresholds and 2D bounding-box table preservation), platform teams preserve token window signal-to-noise ratios while reducing vector index memory footprints by up to 45%.

---

# 1. Interactive Concept Breakdown

## 1.1 The Production Crucible (The Why Before The How)

A global legal consulting firm built an AI search assistant indexing 3 million corporate contracts and vendor agreements. When senior partners queried:
*"Show indemnification clauses covering third-party software intellectual property infringement,"*
the top-10 retrieved chunks returned to the LLM were near-identical copies of a standardized boiler-plate indemnification paragraph extracted from master service agreements across hundreds of different clients.

The actual negotiated rider—which explicitly carved out critical exceptions for open-source AI models—was ranked at position #14 and completely excluded from the LLM prompt context window.

```
TOP-K CONTEXT HIJACKING (THE BOILERPLATE CROWDING EFFECT)
Query: "Indemnification for Third-Party IP Infringement"
Rank #01 ── [MSA Boilerplate v1] ── Cosine Sim: 0.942 ── "Standard indemnification clause..."
Rank #02 ── [MSA Boilerplate v2] ── Cosine Sim: 0.941 ── "Standard indemnification clause..."
Rank #03 ── [MSA Boilerplate v3] ── Cosine Sim: 0.940 ── "Standard indemnification clause..."
...
Rank #10 ── [MSA Boilerplate v10] ── Cosine Sim: 0.932 ── "Standard indemnification clause..."
--------------------------- [ CONTEXT WINDOW LIMIT (K=10) ] ----------------------------
Rank #14 ── [Custom Negotiated Rider] ── Cosine Sim: 0.915 ── [LOST IN TRANSIT]
```

### The Root-Cause Chain
1. **Semantic Density Sinks:** Ingesting 50,000 corporate contracts containing 95% identical boilerplate paragraphs creates high-density clusters in vector space. Because standard Approximate Nearest Neighbor (ANN) search retrieves strictly by cosine proximity, these near-identical chunks monopolize the entire retrieval budget ($K=10$).
2. **Table Flattening Disasters:** The ingestion worker stripped table layouts into flat 1D token streams. Columns containing loss payout numbers were concatenated with deductible numbers, generating hallucinated financial settlements.
3. **Semantic Drift:** Document revisions spanning 5 years diluted current terminology, causing outdated legacy policy definitions to outrank modern definitions.

To solve context hijacking, data pipelines must decouple **syntactic deduplication** (CPU-level) from **semantic deduplication** (embedding-level) and validate **multimodal layout integrity** before chunks enter vector storage.

---

## 1.2 First-Principles Mental Model: Syntactic MinHash vs. Semantic SemDeDup

Data hygiene requires a two-tiered deduplication pipeline:

### 1. Syntactic Deduplication: MinHash & Jaccard Distance
Syntactic similarity between two chunks $A$ and $B$ is measured by the Jaccard index of their $k$-shingles (token $n$-grams):

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

Evaluating pairwise Jaccard across millions of chunks is an $O(N^2)$ bottleneck. MinHash approximates Jaccard similarity by applying $K$ independent hash functions $h_1, \dots, h_K$ and evaluating the probability of hash collision:

$$\Pr[\min(h_i(A)) = \min(h_i(B))] = J(A, B)$$

### 2. Semantic Deduplication: SemDeDup
Chunks may share zero identical words while being semantically redundant (e.g., paraphrased legal disclosures). **SemDeDup** clusters dense vector embeddings into $C$ partitions via $k$-means. Within each cluster, chunk pairs with cosine similarity exceeding threshold $\tau$ (e.g., $\tau \ge 0.92$) are pruned, retaining only the single highest-quality centroid representative.

```
THE TWO-TIER DEDUPLICATION FUNNEL
Raw Ingest Chunks (1,000,000)
    |
    v   [ Tier 1: MinHash LSH (Jaccard >= 0.85) ]  --> Prunes 40% exact/near-exact copies
Clean Chunks (600,000)
    |
    v   [ Tier 2: SemDeDup (Embedding Cosine >= 0.92) ] --> Prunes 25% paraphrased boilerplate
Curated Chunks (450,000) ---> Stored in Vector DB
```

---

# 2. Visual Architecture

## 2.1 End-to-End Data Hygiene & Quality Pipeline

```
+---------------------------------------------------------------------------------------------------+
|                        DATA QUALITY & HYGIENE PIPELINE TOPOLOGY                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ Ingested Document Chunks ]                                                                     |
|            |                                                                                      |
|            v                                                                                      |
|  +--------------------------------------------------------------------+                           |
|  | STEP 1: MULTIMODAL OCR & LAYOUT QUALITY GATE (Worker Data Plane)   |                           |
|  | - Image Laplacian Blur Variance (>= 100.0)                         |                           |
|  | - Mean OCR Confidence (>= 0.82)                                    |                           |
|  | - 2D Table Bounding-Box Grid Integrity (No Row/Col Collisions)     |                           |
|  +----------------------------------+---------------------------------+                           |
|                                     |                                                             |
|                                     v (Valid Structural Layout)                                   |
|  +--------------------------------------------------------------------+                           |
|  | STEP 2: SYNTACTIC HYGIENE GATE (CPU Data Plane)                    |                           |
|  | - SHA-256 Exact Content Hash Lookup                                |                           |
|  | - MinHash LSH Shingling (Jaccard Threshold >= 0.85)                |                           |
|  | - Low-Signal Boilerplate Removal                                   |                           |
|  +----------------------------------+---------------------------------+                           |
|                                     |                                                             |
|                                     v (Syntactically Unique Chunks)                               |
|  +--------------------------------------------------------------------+                           |
|  | STEP 3: SEMDEDUP EMBEDDING PRUNING (GPU Inference Plane)           |                           |
|  | - Compute Dense Vector Embeddings (512d Matryoshka)                |                           |
|  | - Intra-Cluster Cosine Similarity Matrix: dot(u, v)                |                           |
|  | - Prune Chunks where Cosine Sim >= 0.92 (Retain Canonical Node)    |                           |
|  +----------------------------------+---------------------------------+                           |
|                                     |                                                             |
|                                     v                                                             |
|                    [ Curated Vector Index (Milvus / Qdrant) ]                                     |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

# 3. Real-World Code & Configuration

The reference implementation provides a hybrid deduplication engine combining syntactic Jaccard pruning with SemDeDup cosine clustering, paired with a multimodal layout validator.

### 3.1 Hybrid Deduplication Engine (`artifacts/deduplication_engine.py`)

```python
import hashlib
import re
from typing import List, Set, Dict, Any
import numpy as np
from pydantic import BaseModel, Field

class Chunk(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float] = Field(default_factory=list)

class HybridDeduplicator:
    def __init__(self, jaccard_threshold: float = 0.85, semantic_similarity_cutoff: float = 0.92):
        self.jaccard_threshold = jaccard_threshold
        self.semantic_similarity_cutoff = semantic_similarity_cutoff
        self.exact_hashes_seen: Set[str] = set()

    def _shingle_tokens(self, text: str, k: int = 2) -> Set[str]:
        clean_text = re.sub(r"[^\w\s]", "", text.lower())
        words = clean_text.split()
        if len(words) < k:
            return {" ".join(words)}
        return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

    def is_exact_duplicate(self, text: str) -> bool:
        sig = hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()
        if sig in self.exact_hashes_seen:
            return True
        self.exact_hashes_seen.add(sig)
        return False

    def estimate_jaccard(self, text_a: str, text_b: str, k: int = 2) -> float:
        s_a = self._shingle_tokens(text_a, k)
        s_b = self._shingle_tokens(text_b, k)
        union = s_a.union(s_b)
        return len(s_a.intersection(s_b)) / len(union) if union else 0.0

    def prune_syntactic_duplicates(self, chunks: List[Chunk]) -> List[Chunk]:
        unique = []
        for chunk in chunks:
            if self.is_exact_duplicate(chunk.text):
                continue
            if not any(self.estimate_jaccard(chunk.text, u.text) >= self.jaccard_threshold for u in unique):
                unique.append(chunk)
        return unique

    def prune_semantic_duplicates(self, chunks: List[Chunk]) -> List[Chunk]:
        if len(chunks) <= 1:
            return chunks
        embeddings = np.array([c.embedding for c in chunks], dtype=np.float32)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        normalized = embeddings / norms

        sim_matrix = np.dot(normalized, normalized.T)
        n = len(chunks)
        keep = np.ones(n, dtype=bool)

        for i in range(n):
            if not keep[i]:
                continue
            dups = np.where(sim_matrix[i, i+1:] >= self.semantic_similarity_cutoff)[0] + (i + 1)
            keep[dups] = False
        return [chunks[idx] for idx in range(n) if keep[idx]]
```

### 3.2 Multimodal Layout Quality Gate (`artifacts/multimodal_quality_gate.py`)

```python
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class TableCell(BaseModel):
    row_idx: int
    col_idx: int
    text: str
    bbox: BoundingBox

class MultimodalChunkPayload(BaseModel):
    chunk_id: str
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    image_laplacian_variance: float = Field(ge=0.0)
    table_cells: Optional[List[TableCell]] = None

    def validate_quality_gate(self) -> Tuple[bool, str]:
        if self.image_laplacian_variance < 100.0:
            return False, f"REJECTED_BLURRY_IMAGE: Variance {self.image_laplacian_variance:.1f} < 100.0"
        if self.ocr_confidence < 0.82:
            return False, f"REJECTED_LOW_OCR_CONFIDENCE: Confidence {self.ocr_confidence:.2f} < 0.82"
        if self.table_cells:
            coords = set()
            for cell in self.table_cells:
                c = (cell.row_idx, cell.col_idx)
                if c in coords:
                    return False, f"REJECTED_TABLE_COLLISION: Cell collision at {c}"
                coords.add(c)
        return True, "PASSED_QUALITY_GATE"
```

---

# 4. Edge Cases, Failure Modes & Trade-offs

## 4.1 Comparative Architectural Decision Matrix

| Strategy | When to Use | When It Breaks Down | Triage Runbook Indicator |
| :--- | :--- | :--- | :--- |
| **Exact Content Hash (SHA-256)** | Instant $O(1)$ duplicate rejection at ingress | Single whitespace or punctuation change invalidates hash | High frequency of near-identical text surviving into vector DB |
| **MinHash LSH** | Large corpus syntactic dedup across millions of documents | Fails to detect semantic paraphrasing or translated content | Partner reports: "Bot retrieves repetitive legal boilerplates" |
| **SemDeDup (Vector Cosine)** | Eliminating paraphrased redundancy before storage | High memory footprint if comparing vectors without clustering | GPU inference backpressure during batch indexing |

## 4.2 Operational Triage Runbook

```
+---------------------------------------------------------------------------------------------------+
|                        OPERATIONAL TRIAGE RUNBOOK: DATA QUALITY PIPELINE                          |
+---------------------------------------------------------------------------------------------------+
| SYMPTOM: Users report AI assistant quotes redundant contracts or hallucinates table figures      |
|                                                                                                   |
| STEP 1: Verify Table Layout Preservation                                                          |
|   Inspect raw chunk payloads for collapsed 2D cells:                                              |
|   jq '.table_cells' /var/log/ai-chunks/latest.json                                                |
|   - If table cells are missing bounding box coordinates, activate VLM late-interaction parsing    |
|                                                                                                   |
| STEP 2: Check SemDeDup Pruning Rate                                                               |
|   - Normal curation pruning rate: 15% to 35%                                                      |
|   - If pruning rate < 5%: Threshold (0.92) is too strict; tune to 0.88                            |
|   - If pruning rate > 60%: Threshold is too aggressive; critical domain nuances are being dropped |
|                                                                                                   |
| STEP 3: Monitor Semantic Embedding Drift                                                          |
|   - Calculate daily Fréchet Distance across newly generated embedding batches                    |
|   - If drift score > 0.15: Alert data engineering to inspect upstream source corpus updates       |
+---------------------------------------------------------------------------------------------------+
```
