"""Production embedding engine with Matryoshka prefix slicing, L2 re-normalization, and SQ8 quantization."""
import numpy as np
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

class EmbeddingRequest(BaseModel):
    texts: List[str] = Field(min_length=1, description="Batch of text strings to embed")
    target_dim: int = Field(default=512, ge=64, le=1536, description="Target Matryoshka dimension")

class EmbeddingStats(BaseModel):
    original_dimension: int
    truncated_dimension: int
    raw_fp32_bytes: int
    quantized_int8_bytes: int
    compression_ratio: float

class MatryoshkaEmbeddingService:
    """
    Data Plane transformation service managing dimensionality reduction,
    vector manifold normalization, and 8-bit scalar quantization.
    """
    def __init__(self, default_target_dim: int = 512):
        self.default_target_dim = default_target_dim

    def process_and_slice(self, raw_embeddings: np.ndarray, target_dim: int = None) -> np.ndarray:
        """
        Slices high-dimensional embeddings to target MRL prefix and applies L2 re-normalization.
        
        CRITICAL MATHEMATICAL INVARIANT:
        When a unit vector in R^N is truncated to R^K (K < N), its L2 norm drops below 1.0:
        ||v[:K]||_2 < 1.0. If not re-normalized, dot products no longer equal cosine similarities!
        """
        dim = target_dim or self.default_target_dim
        
        if raw_embeddings.shape[1] < dim:
            raise ValueError(f"Cannot slice to {dim} dimensions from native {raw_embeddings.shape[1]}")

        # Step 1: Matryoshka prefix truncation
        sliced = raw_embeddings[:, :dim]

        # Step 2: Re-project onto the unit hypersphere via L2 re-normalization
        norms = np.linalg.norm(sliced, axis=1, keepdims=True)
        # Numerical guard against division by zero
        normalized = sliced / np.clip(norms, a_min=1e-12, a_max=None)

        return normalized

    def quantize_to_sq8(self, normalized_vectors: np.ndarray) -> np.ndarray:
        """
        Symmetric 8-bit scalar quantization for 4x memory compression.
        Since vectors are L2-normalized on [-1.0, 1.0], symmetric scaling by 127 is optimal.
        """
        quantized = np.clip(np.round(normalized_vectors * 127.0), -128, 127).astype(np.int8)
        return quantized

    def dequantize_from_sq8(self, quantized_vectors: np.ndarray) -> np.ndarray:
        """Restores float32 approximation from 8-bit integer vectors."""
        return quantized_vectors.astype(np.float32) / 127.0

    def compute_stats(self, num_vectors: int, native_dim: int, target_dim: int) -> EmbeddingStats:
        raw_bytes = num_vectors * native_dim * 4  # FP32 = 4 bytes
        sq8_bytes = num_vectors * target_dim * 1   # INT8 = 1 byte
        return EmbeddingStats(
            original_dimension=native_dim,
            truncated_dimension=target_dim,
            raw_fp32_bytes=raw_bytes,
            quantized_int8_bytes=sq8_bytes,
            compression_ratio=raw_bytes / max(1, sq8_bytes)
        )

if __name__ == "__main__":
    service = MatryoshkaEmbeddingService(target_dim=512)
    # Simulate a batch of 100 random 1536-dimensional embedding vectors
    simulated_raw = np.random.randn(100, 1536).astype(np.float32)
    # L2 normalize initial raw vectors
    simulated_raw /= np.linalg.norm(simulated_raw, axis=1, keepdims=True)
    
    sliced = service.process_and_slice(simulated_raw, target_dim=512)
    quantized = service.quantize_to_sq8(sliced)
    
    stats = service.compute_stats(100, 1536, 512)
    print(f"Original shape: {simulated_raw.shape} ({stats.raw_fp32_bytes} bytes)")
    print(f"Quantized shape: {quantized.shape} ({stats.quantized_int8_bytes} bytes)")
    print(f"Total compression factor: {stats.compression_ratio:.2f}x reduction")
