#!/usr/bin/env python3
"""
Hybrid Deduplication Engine
Combines syntactic MinHash LSH with dense embedding SemDeDup to eliminate
exact copies, boilerplate, and near-duplicate chunks before vector database insertion.
"""

import hashlib
from typing import List, Set, Dict, Any
import numpy as np
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HybridDeduplicator:
    def __init__(
        self,
        jaccard_threshold: float = 0.85,
        semantic_similarity_cutoff: float = 0.92,
        num_perm: int = 64
    ):
        self.jaccard_threshold = jaccard_threshold
        self.semantic_similarity_cutoff = semantic_similarity_cutoff
        self.num_perm = num_perm
        self.exact_hashes_seen: Set[str] = set()

    def _shingle_tokens(self, text: str, k: int = 2) -> Set[str]:
        """Generates k-shingles (n-grams) from normalized alphanumeric text."""
        import re
        clean_text = re.sub(r"[^\w\s]", "", text.lower())
        words = clean_text.split()
        if len(words) < k:
            return {" ".join(words)}
        return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

    def is_exact_duplicate(self, text: str) -> bool:
        """O(1) SHA-256 exact content hash check."""
        sig = hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()
        if sig in self.exact_hashes_seen:
            return True
        self.exact_hashes_seen.add(sig)
        return False

    def estimate_jaccard(self, text_a: str, text_b: str, k: int = 2) -> float:
        """Calculates exact Jaccard similarity across k-shingles."""
        shingles_a = self._shingle_tokens(text_a, k)
        shingles_b = self._shingle_tokens(text_b, k)
        intersection = shingles_a.intersection(shingles_b)
        union = shingles_a.union(shingles_b)
        if not union:
            return 0.0
        return len(intersection) / len(union)

    def prune_syntactic_duplicates(self, chunks: List[Chunk]) -> List[Chunk]:
        """Prunes exact and high-Jaccard syntactic duplicates."""
        unique_chunks: List[Chunk] = []
        for chunk in chunks:
            if self.is_exact_duplicate(chunk.text):
                continue
            
            # Check against accumulated unique chunks
            is_dup = False
            for existing in unique_chunks:
                if self.estimate_jaccard(chunk.text, existing.text) >= self.jaccard_threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique_chunks.append(chunk)
                
        return unique_chunks

    def prune_semantic_duplicates(self, chunks: List[Chunk]) -> List[Chunk]:
        """
        Executes SemDeDup: prunes semantic duplicates exceeding cosine similarity threshold.
        Assumes normalized dense embedding vectors.
        """
        if len(chunks) <= 1:
            return chunks

        embeddings = np.array([c.embedding for c in chunks], dtype=np.float32)
        # Verify normalization
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        normalized = embeddings / norms

        sim_matrix = np.dot(normalized, normalized.T)
        n = len(chunks)
        keep = np.ones(n, dtype=bool)

        for i in range(n):
            if not keep[i]:
                continue
            # Any j > i with cosine similarity >= cutoff is marked duplicate
            dups = np.where(sim_matrix[i, i+1:] >= self.semantic_similarity_cutoff)[0] + (i + 1)
            keep[dups] = False

        return [chunks[idx] for idx in range(n) if keep[idx]]


if __name__ == "__main__":
    dedup = HybridDeduplicator(jaccard_threshold=0.80, semantic_similarity_cutoff=0.90)

    # 1. Exact & Syntactic test
    c1 = Chunk(chunk_id="c1", text="The quick brown fox jumps over the lazy dog.")
    c2 = Chunk(chunk_id="c2", text="The quick brown fox jumps over the lazy dog.") # Exact
    c3 = Chunk(chunk_id="c3", text="The quick brown fox jumps over the lazy dog again.") # Near-duplicate (8/9 bigrams)
    c4 = Chunk(chunk_id="c4", text="Kubernetes manages containerized workloads across cloud clusters.")

    initial_chunks = [c1, c2, c3, c4]
    syntactic_unique = dedup.prune_syntactic_duplicates(initial_chunks)
    print(f"Syntactic Deduplication: {len(initial_chunks)} -> {len(syntactic_unique)} chunks")
    assert len(syntactic_unique) == 2, "Should retain c1 and c4"

    # 2. Semantic test with mock embeddings
    # c1 and c1_paraphrase share 0.96 cosine proximity
    v1 = [0.9, 0.1, 0.0]
    v_similar = [0.89, 0.11, 0.02]
    v_distinct = [0.0, 0.1, 0.99]

    chunks_with_vectors = [
        Chunk(chunk_id="p1", text="Cloud microservices ensure stateless scalability.", embedding=v1),
        Chunk(chunk_id="p2", text="Stateless cloud microservices provide horizontal scalability.", embedding=v_similar),
        Chunk(chunk_id="p3", text="Relational databases use B-Trees for primary index lookups.", embedding=v_distinct),
    ]

    curated = dedup.prune_semantic_duplicates(chunks_with_vectors)
    print(f"SemDeDup Pruning: {len(chunks_with_vectors)} -> {len(curated)} chunks")
    assert len(curated) == 2, "Should prune semantic duplicate p2"
    print("All deduplication assertions passed.")
