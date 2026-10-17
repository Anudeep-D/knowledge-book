#!/usr/bin/env python3
"""
Production Vector Quantizer & Asymmetric Distance Computation Engine.

Demonstrates:
1. L2 Unit Hypersphere Normalization (Cosine -> Maximum Inner Product Search).
2. Symmetric 8-Bit Scalar Quantization (SQ8) with zero-point offset elimination.
3. Asymmetric Distance Computation (ADC): FP32 Query vs Int8 Quantized Storage.
"""

from dataclasses import dataclass
import time
from typing import Tuple
import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class QuantizedVectorSegment:
    """Immutable memory layout for 8-bit quantized high-dimensional vectors."""
    quantized_matrix: npt.NDArray[np.int8]    # Shape: (N, D) in [-128, 127]
    scale_factors: npt.NDArray[np.float32]     # Shape: (N,) per-vector scale multiplier
    dimension: int
    vector_count: int

    @property
    def memory_bytes(self) -> int:
        return self.quantized_matrix.nbytes + self.scale_factors.nbytes


class SymmetricScalarQuantizer:
    """
    Symmetric 8-Bit Scalar Quantizer for normalized embedding manifolds.
    
    Compresses 32-bit floating-point dense representations by 75%
    (from 4 bytes/dim down to 1 byte/dim + float32 scale per vector).
    """

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    def normalize_l2(self, vectors: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
        """Projects vectors onto the unit hypersphere: ||v||_2 = 1.0."""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        # Numerical guard against divide-by-zero
        return vectors / np.maximum(norms, 1e-12)

    def quantize(self, vectors: npt.NDArray[np.float32]) -> QuantizedVectorSegment:
        """
        Quantizes an (N, D) float32 matrix to signed int8.
        
        Symmetric quantization maps [-max_val, +max_val] -> [-128, 127],
        ensuring 0.0 maps directly to 0 integer with no zero-point shift.
        """
        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(f"Expected shape (N, {self.dimension}), got {vectors.shape}")

        # Invariant 1: Ensure strict unit normalization
        normalized = self.normalize_l2(vectors.astype(np.float32))

        # Invariant 2: Per-vector dynamic absolute range scaling
        # For unit vectors, max_val is <= 1.0, but per-coordinate distribution varies
        max_abs = np.max(np.abs(normalized), axis=1, keepdims=True)
        scales = (max_abs / 127.0).astype(np.float32)

        # Scale and symmetrically clamp to int8 bounds
        quantized = np.clip(np.round(normalized / scales), -128, 127).astype(np.int8)

        return QuantizedVectorSegment(
            quantized_matrix=quantized,
            scale_factors=scales.squeeze(axis=1),
            dimension=self.dimension,
            vector_count=vectors.shape[0]
        )

    def search_top_k(
        self,
        query: npt.NDArray[np.float32],
        segment: QuantizedVectorSegment,
        k: int = 10
    ) -> Tuple[npt.NDArray[np.int64], npt.NDArray[np.float32]]:
        """
        Asymmetric Distance Computation (ADC):
        Computes dot product between unquantized FP32 query and int8 quantized base.
        """
        if query.ndim == 1:
            query = query.reshape(1, -1)

        # Normalize query vector to preserve MIPS cosine equivalence
        norm_query = self.normalize_l2(query.astype(np.float32)).squeeze(axis=0)

        # Vectorized SIMD Dot Product: (N, D) int8 @ (D,) float32 -> (N,) float32
        # Convert int8 to float32 accumulator during BLAS matrix-vector product
        raw_dot = np.dot(segment.quantized_matrix.astype(np.float32), norm_query)

        # Re-scale back to [-1.0, 1.0] cosine similarity range
        similarity_scores = raw_dot * segment.scale_factors

        # Efficient top-k partition
        top_k_indices = np.argpartition(-similarity_scores, kth=min(k, segment.vector_count - 1))[:k]
        sorted_top_k = top_k_indices[np.argsort(-similarity_scores[top_k_indices])]

        return sorted_top_k, similarity_scores[sorted_top_k]


def benchmark_quantization(num_vectors: int = 50_000, dimension: int = 1536):
    """Executes a comparative benchmark between FP32 exact scan and SQ8 ADC."""
    print(f"\n================ VECTOR QUANTIZATION BENCHMARK ================")
    print(f"Generating {num_vectors:,} random embeddings (d={dimension})...")
    np.random.seed(42)
    raw_data = np.random.randn(num_vectors, dimension).astype(np.float32)
    query = np.random.randn(dimension).astype(np.float32)

    quantizer = SymmetricScalarQuantizer(dimension=dimension)

    # 1. Measure Exact FP32 Baseline
    t0 = time.perf_counter()
    norm_data = quantizer.normalize_l2(raw_data)
    norm_query = quantizer.normalize_l2(query.reshape(1, -1)).squeeze(axis=0)
    fp32_scores = np.dot(norm_data, norm_query)
    fp32_top10 = np.argsort(-fp32_scores)[:10]
    fp32_latency_ms = (time.perf_counter() - t0) * 1000
    fp32_ram_mb = norm_data.nbytes / (1024 * 1024)

    # 2. Measure SQ8 Quantization & Search
    t1 = time.perf_counter()
    segment = quantizer.quantize(raw_data)
    build_latency_ms = (time.perf_counter() - t1) * 1000

    t2 = time.perf_counter()
    sq8_top10, sq8_scores = quantizer.search_top_k(query, segment, k=10)
    sq8_latency_ms = (time.perf_counter() - t2) * 1000
    sq8_ram_mb = segment.memory_bytes / (1024 * 1024)

    # Calculate Recall@10
    overlap = len(set(fp32_top10).intersection(set(sq8_top10)))
    recall_at_10 = overlap / 10.0

    print(f"FP32 Raw RAM Footprint:    {fp32_ram_mb:.2f} MB")
    print(f"SQ8 Quantized RAM:         {sq8_ram_mb:.2f} MB ({100 - (sq8_ram_mb/fp32_ram_mb*100):.1f}% reduction)")
    print(f"Quantization Build Time:   {build_latency_ms:.2f} ms")
    print(f"FP32 Search Latency:       {fp32_latency_ms:.2f} ms")
    print(f"SQ8 Search Latency:        {sq8_latency_ms:.2f} ms")
    print(f"Recall@10 Precision:       {recall_at_10 * 100:.1f}%")
    print(f"===============================================================\n")


if __name__ == "__main__":
    benchmark_quantization()
