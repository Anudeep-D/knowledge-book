#!/usr/bin/env python3
"""
Query Enforcement & Tombstone Filter Builder
Injects non-bypassable metadata filters into vector search requests to guarantee
that soft-deleted (tombstoned) chunks are strictly excluded from nearest neighbor results.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class CompliantVectorQuery(BaseModel):
    collection_name: str
    query_vector: List[float]
    top_k: int = Field(default=10, ge=1, le=100)
    tenant_id: str
    include_tombstones: bool = False  # Strictly False by default

    def build_qdrant_filter(self) -> Dict[str, Any]:
        """Generates Qdrant compliant boolean filter."""
        return {
            "must": [
                {"key": "tenant_id", "match": {"value": self.tenant_id}},
                {"key": "tombstone", "match": {"value": False}}
            ]
        }

    def build_milvus_expr(self) -> str:
        """Generates Milvus boolean filter expression."""
        return f'(tenant_id == "{self.tenant_id}") and (tombstone == false)'


if __name__ == "__main__":
    query = CompliantVectorQuery(
        collection_name="enterprise-docs",
        query_vector=[0.1, 0.2, 0.3],
        top_k=5,
        tenant_id="tenant_acme"
    )

    qdrant_filter = query.build_qdrant_filter()
    milvus_filter = query.build_milvus_expr()

    print("Qdrant Filter:", qdrant_filter)
    print("Milvus Filter:", milvus_filter)

    assert any(
        f.get("key") == "tombstone" and f.get("match", {}).get("value") is False
        for f in qdrant_filter["must"]
    ), "Qdrant filter must enforce tombstone == False"
    assert "tombstone == false" in milvus_filter, "Milvus filter must enforce tombstone == false"
    print("All query enforcement filter assertions passed successfully.")
