"""Production hierarchical Parent-Child recursive chunker with contextual breadcrumbs."""
import uuid
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

class ChunkNode(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: str
    text_content: str
    token_count: int
    metadata: Dict[str, Any]

class DocumentSection(BaseModel):
    doc_title: str
    section_path: str
    raw_text: str

class HierarchicalContextChunker:
    """
    Data Plane chunking engine executing structural recursive splitting with
    parent-child context preservation and breadcrumb header injection.
    """
    def __init__(
        self, 
        child_size: int = 256, 
        child_overlap: int = 32,
        parent_size: int = 1024
    ):
        self.child_size = child_size
        self.child_overlap = child_overlap
        self.parent_size = parent_size

    def estimate_tokens(self, text: str) -> int:
        """Lightweight token estimator: approx 4 characters per token."""
        return max(1, len(text) // 4)

    def chunk_parent_block(
        self, 
        parent_text: str, 
        parent_id: str, 
        doc_title: str, 
        section_path: str
    ) -> List[ChunkNode]:
        """
        Splits parent text into overlapping child chunks and injects
        contextual breadcrumb headers to guarantee semantic anchoring in vector space.
        """
        words = parent_text.split()
        if not words:
            return []

        # Convert word array chunks preserving approx child token window
        words_per_chunk = max(10, self.child_size * 3 // 4)
        words_overlap = max(2, self.child_overlap * 3 // 4)
        step = max(1, words_per_chunk - words_overlap)

        nodes: List[ChunkNode] = []
        breadcrumb = f"Document: {doc_title} | Section: {section_path}\n---\n"
        breadcrumb_tokens = self.estimate_tokens(breadcrumb)

        for i in range(0, len(words), step):
            window = words[i:i + words_per_chunk]
            raw_child = " ".join(window)
            
            # Non-negotiable invariant: Anchor vector position with contextual breadcrumbs
            enriched_content = f"{breadcrumb}{raw_child}"
            token_count = self.estimate_tokens(raw_child) + breadcrumb_tokens

            nodes.append(ChunkNode(
                parent_id=parent_id,
                text_content=enriched_content,
                token_count=token_count,
                metadata={
                    "doc_title": doc_title,
                    "section_path": section_path,
                    "word_offset_start": i,
                    "word_offset_end": i + len(window),
                    "is_child": True
                }
            ))
            
            if i + words_per_chunk >= len(words):
                break

        return nodes

if __name__ == "__main__":
    chunker = HierarchicalContextChunker(child_size=128, child_overlap=16)
    sample_text = (
        "Underwriter agrees to fully reimburse all casualty loss events described in Section 4.1 "
        "subject to the covenants and warranties defined herein. "
        "Provided always that Supplier shall have no liability for indirect, incidental, or consequential damages. "
        "Except where damage results from intentional non-compliance with regional building codes, "
        "in which event the aggregate liability cap of Section 9.2 shall be deemed completely null and void."
    )
    parent_uid = str(uuid.uuid4())
    chunks = chunker.chunk_parent_block(
        parent_text=sample_text,
        parent_id=parent_uid,
        doc_title="Master Services Agreement 2026",
        section_path="Section 4.2 > Indemnification Exceptions"
    )
    print(f"Generated {len(chunks)} contextual children from parent {parent_uid[:8]}:")
    for idx, c in enumerate(chunks):
        print(f"--- Child {idx} ({c.token_count} tokens) ---")
        print(c.text_content[:140] + "...")
