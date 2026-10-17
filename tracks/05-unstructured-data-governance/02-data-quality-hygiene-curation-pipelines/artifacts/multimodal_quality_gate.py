#!/usr/bin/env python3
"""
Multimodal Quality Gate & Layout Preservation Validator
Validates image sharpness (Laplacian variance), OCR confidence, and prevents
destructive 2D table flattening in document chunks before vectorization.
"""

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x_min: float = Field(..., ge=0.0)
    y_min: float = Field(..., ge=0.0)
    x_max: float = Field(..., ge=0.0)
    y_max: float = Field(..., ge=0.0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class TableCell(BaseModel):
    row_idx: int = Field(..., ge=0)
    col_idx: int = Field(..., ge=0)
    text: str
    bbox: BoundingBox


class MultimodalChunkPayload(BaseModel):
    chunk_id: str
    page_number: int = Field(default=1, ge=1)
    raw_text: str
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    image_laplacian_variance: float = Field(ge=0.0)  # >100 indicates sharp image
    table_cells: Optional[List[TableCell]] = None

    def validate_quality_gate(self) -> Tuple[bool, str]:
        """
        Validates quality invariants:
        1. Sharpness: Image Laplacian variance >= 100.0 (reject blurry scans)
        2. OCR Confidence: Mean confidence >= 0.82 (reject degraded OCR)
        3. Table Topological Integrity: No row/column collisions or collapsed 2D grids
        """
        if self.image_laplacian_variance < 100.0:
            return False, f"REJECTED_BLURRY_IMAGE: Laplacian variance {self.image_laplacian_variance:.1f} < 100.0"

        if self.ocr_confidence < 0.82:
            return False, f"REJECTED_LOW_OCR_CONFIDENCE: Mean confidence {self.ocr_confidence:.2f} < 0.82"

        if self.table_cells:
            # Check for grid flattening collisions (two distinct cells assigned same coordinate)
            seen_coordinates = set()
            for cell in self.table_cells:
                coord = (cell.row_idx, cell.col_idx)
                if coord in seen_coordinates:
                    return False, f"REJECTED_TABLE_COLLISION: Flattened collision at row {cell.row_idx}, col {cell.col_idx}"
                seen_coordinates.add(coord)

        return True, "PASSED_QUALITY_GATE"


if __name__ == "__main__":
    # 1. Valid sharp document chunk with structured table
    valid_cells = [
        TableCell(row_idx=0, col_idx=0, text="Claim Item", bbox=BoundingBox(x_min=10, y_min=10, x_max=50, y_max=30)),
        TableCell(row_idx=0, col_idx=1, text="Approved ($)", bbox=BoundingBox(x_min=55, y_min=10, x_max=90, y_max=30)),
        TableCell(row_idx=1, col_idx=0, text="Roof Repairs", bbox=BoundingBox(x_min=10, y_min=35, x_max=50, y_max=55)),
        TableCell(row_idx=1, col_idx=1, text="12000", bbox=BoundingBox(x_min=55, y_min=35, x_max=90, y_max=55)),
    ]
    good_chunk = MultimodalChunkPayload(
        chunk_id="chk-valid-01",
        raw_text="Claim Item: Roof Repairs | Approved ($): 12000",
        ocr_confidence=0.94,
        image_laplacian_variance=245.0,
        table_cells=valid_cells
    )
    is_ok, reason = good_chunk.validate_quality_gate()
    assert is_ok, f"Expected pass, got: {reason}"

    # 2. Corrupted blurry scan
    blurry_chunk = MultimodalChunkPayload(
        chunk_id="chk-blur-02",
        raw_text="Unreadable blurred text",
        ocr_confidence=0.85,
        image_laplacian_variance=42.0
    )
    is_ok, reason = blurry_chunk.validate_quality_gate()
    assert not is_ok and "REJECTED_BLURRY_IMAGE" in reason

    # 3. Flattened table with row/col collision
    flattened_cells = [
        TableCell(row_idx=0, col_idx=0, text="Cell A", bbox=BoundingBox(x_min=10, y_min=10, x_max=50, y_max=30)),
        TableCell(row_idx=0, col_idx=0, text="Cell B (Overlapping)", bbox=BoundingBox(x_min=15, y_min=12, x_max=52, y_max=32)),
    ]
    flattened_chunk = MultimodalChunkPayload(
        chunk_id="chk-table-03",
        raw_text="Cell A Cell B",
        ocr_confidence=0.91,
        image_laplacian_variance=180.0,
        table_cells=flattened_cells
    )
    is_ok, reason = flattened_chunk.validate_quality_gate()
    assert not is_ok and "REJECTED_TABLE_COLLISION" in reason
    print("All multimodal quality gate assertions passed successfully.")
