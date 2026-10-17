#!/usr/bin/env python3
"""
OpenLineage Provenance & GDPR Vector Unlearning Manager
Tracks data lineage from raw object store artifacts to vector index chunks,
and executes compliant two-tier vector unlearning (soft tombstoning and payload scrubbing)
for GDPR Article 17 Right-to-Erasure compliance.
"""

from datetime import datetime, timezone
import hashlib
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class LineageRecord(BaseModel):
    source_urn: str
    data_subject_id: str
    document_id: str
    chunk_ids: List[str]
    vector_collection: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MockVectorClient:
    """Mock in-memory vector store client simulating Milvus/Qdrant payloads."""
    def __init__(self):
        self.storage: Dict[str, Dict[str, Any]] = {}

    def insert(self, chunk_id: str, vector: List[float], payload: Dict[str, Any]):
        self.storage[chunk_id] = {
            "vector": vector,
            "payload": {**payload, "tombstone": False}
        }

    def update_payload(self, chunk_id: str, new_payload: Dict[str, Any]):
        if chunk_id in self.storage:
            self.storage[chunk_id]["payload"].update(new_payload)

    def get(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        return self.storage.get(chunk_id)


class VectorGDPRController:
    def __init__(self, vector_client: MockVectorClient):
        self.client = vector_client
        # Provenance index: data_subject_id -> List[LineageRecord]
        self.lineage_catalog: Dict[str, List[LineageRecord]] = {}
        # Append-only cryptographic audit ledger
        self.audit_ledger: List[Dict[str, Any]] = []

    def record_provenance(self, lineage: LineageRecord):
        """Records provenance linking user data to generated vector chunks."""
        if lineage.data_subject_id not in self.lineage_catalog:
            self.lineage_catalog[lineage.data_subject_id] = []
        self.lineage_catalog[lineage.data_subject_id].append(lineage)

    def execute_right_to_be_forgotten(self, data_subject_id: str) -> Dict[str, Any]:
        """
        Executes compliant two-tier vector unlearning:
        1. Resolves all chunk vectors belonging to the data subject.
        2. Sets tombstone flag and scrubs raw text payloads in vector store immediately.
        3. Generates cryptographic SHA-256 audit receipt.
        4. Removes subject from active catalog.
        """
        records = self.lineage_catalog.get(data_subject_id, [])
        if not records:
            return {"status": "NO_OP", "data_subject_id": data_subject_id, "chunks_affected": 0}

        all_chunk_ids = []
        for record in records:
            all_chunk_ids.extend(record.chunk_ids)

        # Step 1 & 2: Soft tombstone and wipe raw text payloads in vector database
        now_iso = datetime.now(timezone.utc).isoformat()
        for cid in all_chunk_ids:
            self.client.update_payload(
                chunk_id=cid,
                new_payload={
                    "tombstone": True,
                    "text_payload": "[ERASED_GDPR_ARTICLE_17]",
                    "erased_at": now_iso
                }
            )

        # Step 3: Compute cryptographic receipt
        receipt_payload = f"{data_subject_id}:{len(all_chunk_ids)}:{now_iso}"
        audit_hash = hashlib.sha256(receipt_payload.encode("utf-8")).hexdigest()

        audit_entry = {
            "data_subject_id": data_subject_id,
            "chunks_scrubbed": len(all_chunk_ids),
            "timestamp": now_iso,
            "audit_hash": audit_hash,
            "status": "COMPLIED_GDPR_ART_17"
        }
        self.audit_ledger.append(audit_entry)

        # Step 4: Invalidate active catalog reference
        del self.lineage_catalog[data_subject_id]

        return {"status": "COMPLETED", "audit_receipt": audit_entry}


if __name__ == "__main__":
    vector_db = MockVectorClient()
    controller = VectorGDPRController(vector_client=vector_db)

    # 1. Ingest document chunks for customer usr_9912
    c1_id = "chk-usr-9912-001"
    c2_id = "chk-usr-9912-002"
    vector_db.insert(c1_id, [0.12, 0.45, 0.88], {"tenant_id": "cust_acme", "text_payload": "Customer usr_9912 refund complaint"})
    vector_db.insert(c2_id, [0.15, 0.43, 0.85], {"tenant_id": "cust_acme", "text_payload": "Customer usr_9912 warranty terms"})

    # Record provenance
    controller.record_provenance(
        LineageRecord(
            source_urn="s3://enterprise-lake/tickets/usr_9912_claim.pdf",
            data_subject_id="usr_9912",
            document_id="doc-9912",
            chunk_ids=[c1_id, c2_id],
            vector_collection="legal-contracts"
        )
    )

    # Verify initial storage
    assert vector_db.get(c1_id)["payload"]["tombstone"] is False

    # 2. Execute GDPR Deletion Request
    result = controller.execute_right_to_be_forgotten("usr_9912")
    print("GDPR Erasure Result:", result)
    assert result["status"] == "COMPLETED"
    assert result["audit_receipt"]["chunks_scrubbed"] == 2

    # 3. Verify vector store payload scrubbing and tombstone flag
    chunk1_data = vector_db.get(c1_id)
    assert chunk1_data["payload"]["tombstone"] is True
    assert chunk1_data["payload"]["text_payload"] == "[ERASED_GDPR_ARTICLE_17]"
    print("All GDPR vector unlearning assertions passed successfully.")
