"""Production multimodal document extraction and structured payload packager."""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class IngestModality(str, Enum):
    STRUCTURED_TABLE = "table_markdown"
    VISUAL_IMAGE = "visual_chart_summary"
    NARRATIVE_TEXT = "narrative_text"

class ExtractedContentNode(BaseModel):
    page_number: int = Field(ge=1)
    modality: IngestModality
    payload: str = Field(..., description="Markdown table, chart summary, or text")
    bounding_box: Optional[List[float]] = Field(default=None, description="[ymin, xmin, ymax, xmax]")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MultimodalDocumentPackager:
    """
    Data Plane transformation service unifying heterogeneous multimodal extractions
    (tables, diagrams, text blocks) into a linearized, layout-preserving payload.
    """
    def format_for_indexing(self, nodes: List[ExtractedContentNode], doc_name: str) -> str:
        """
        Unifies extracted heterogeneous multimodal blocks into a coherent semantic stream,
        explicitly preserving tabular relationships and visual image descriptions.
        """
        assembled_chunks: List[str] = []
        assembled_chunks.append(f"# Document Manifest: {doc_name}\n")
        
        for node in nodes:
            if node.modality == IngestModality.STRUCTURED_TABLE:
                header = f"\n[PAGE {node.page_number} - FINANCIAL DATA TABLE]\n"
                footer = "\n[/END TABLE]\n"
                assembled_chunks.append(f"{header}{node.payload}{footer}")
                
            elif node.modality == IngestModality.VISUAL_IMAGE:
                header = f"\n[PAGE {node.page_number} - VISUAL CHART DESCRIPTION]\n"
                footer = "\n[/END VISUAL]\n"
                assembled_chunks.append(f"{header}{node.payload}{footer}")
                
            else:
                assembled_chunks.append(f"\n[PAGE {node.page_number}]\n{node.payload}\n")
                
        return "".join(assembled_chunks)

if __name__ == "__main__":
    packager = MultimodalDocumentPackager()
    sample_nodes = [
        ExtractedContentNode(
            page_number=1,
            modality=IngestModality.NARRATIVE_TEXT,
            payload="Fiscal Year 2025 Comprehensive Operations and Financial Performance Overview."
        ),
        ExtractedContentNode(
            page_number=2,
            modality=IngestModality.STRUCTURED_TABLE,
            payload=(
                "| Metric | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
                "| Gross Revenue ($M) | $124.5 | $142.0 | $158.2 | $181.4 |\n"
                "| Operating Income ($M) | $18.2 | $22.4 | $29.1 | $34.8 |\n"
                "| Free Cash Flow ($M) | $11.4 | $15.8 | $21.2 | $26.5 |"
            )
        ),
        ExtractedContentNode(
            page_number=3,
            modality=IngestModality.VISUAL_IMAGE,
            payload="Bar chart illustrating quarter-over-quarter revenue acceleration from 14% to 22%."
        )
    ]
    manifest = packager.format_for_indexing(sample_nodes, "Enterprise_Q4_Financials.pdf")
    print(manifest)
