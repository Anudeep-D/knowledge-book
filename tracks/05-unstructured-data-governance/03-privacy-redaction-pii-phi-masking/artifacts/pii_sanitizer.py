#!/usr/bin/env python3
"""
Enterprise PII/PHI Sanitizer & Tokenization Vault
Identifies sensitive entities (SSN, Email, Phone, Internal IDs) and substitutes them
with deterministic entity-counter tokens (<PERSON_1>, <SSN_1>) or format-preserving
encryption tokens to preserve linguistic context without leaking raw identifiers.
"""

import re
from typing import Dict, List, Tuple
from pydantic import BaseModel, Field

try:
    from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
    from presidio_anonymizer import AnonymizerEngine
    from presidio_anonymizer.entities import OperatorConfig
    HAS_PRESIDIO = True
except ImportError:
    HAS_PRESIDIO = False


class SanitizationResult(BaseModel):
    sanitized_text: str
    detected_entities: List[str] = Field(default_factory=list)
    entity_counts: Dict[str, int] = Field(default_factory=dict)
    has_pii: bool = False


class EnterprisePIISanitizer:
    def __init__(self):
        self.has_presidio = HAS_PRESIDIO
        if self.has_presidio:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            self._register_presidio_patterns()
        else:
            self._compile_fallback_regexes()

    def _register_presidio_patterns(self):
        emp_pattern = Pattern(name="emp_pattern", regex=r"\bEMP-[0-9]{6}\b", score=0.95)
        self.analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="INTERNAL_EMP_ID", patterns=[emp_pattern]))

    def _compile_fallback_regexes(self):
        self.regex_map = {
            "US_SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "EMAIL_ADDRESS": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "PHONE_NUMBER": re.compile(r"\b(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b"),
            "INTERNAL_EMP_ID": re.compile(r"\bEMP-[0-9]{6}\b"),
            "CREDIT_CARD": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b"),
        }

    def sanitize(self, raw_text: str) -> SanitizationResult:
        """
        Substitutes raw PII with typed positional tokens:
        'Alice (EMP-123456) with SSN 123-45-6789' -> 'Alice (<INTERNAL_EMP_ID_1>) with SSN <US_SSN_1>'
        """
        detected: List[str] = []
        counts: Dict[str, int] = {}
        sanitized = raw_text

        if self.has_presidio:
            results = self.analyzer.analyze(
                text=raw_text,
                language="en",
                entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SSN", "INTERNAL_EMP_ID"]
            )
            anonymized = self.anonymizer.anonymize(
                text=raw_text,
                analyzer_results=results,
                operators={
                    "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"}),
                    "PERSON": OperatorConfig("entity_counter", {"template": "<PERSON_{}>"}),
                    "US_SSN": OperatorConfig("entity_counter", {"template": "<US_SSN_{}>"}),
                    "INTERNAL_EMP_ID": OperatorConfig("entity_counter", {"template": "<INTERNAL_EMP_ID_{}>"}),
                    "EMAIL_ADDRESS": OperatorConfig("entity_counter", {"template": "<EMAIL_{}>"}),
                }
            )
            for r in results:
                detected.append(r.entity_type)
                counts[r.entity_type] = counts.get(r.entity_type, 0) + 1
            return SanitizationResult(
                sanitized_text=anonymized.text,
                detected_entities=list(set(detected)),
                entity_counts=counts,
                has_pii=len(results) > 0
            )

        # Standalone deterministic regex fallback
        for entity_type, pattern in self.regex_map.items():
            matches = pattern.findall(sanitized)
            if matches:
                detected.append(entity_type)
                counts[entity_type] = len(matches)
                for i, match in enumerate(matches, 1):
                    sanitized = sanitized.replace(match, f"<{entity_type}_{i}>", 1)

        return SanitizationResult(
            sanitized_text=sanitized,
            detected_entities=detected,
            entity_counts=counts,
            has_pii=len(detected) > 0
        )


if __name__ == "__main__":
    sanitizer = EnterprisePIISanitizer()
    sample = (
        "Employee Alice Smith (EMP-991234) submitted health ticket with SSN 000-12-3456 "
        "and contact email alice.smith@enterprise.org."
    )
    result = sanitizer.sanitize(sample)
    print("Raw Input:", sample)
    print("Sanitized:", result.sanitized_text)
    print("Detected:", result.detected_entities)
    print("Counts:", result.entity_counts)

    assert "<INTERNAL_EMP_ID_1>" in result.sanitized_text or "<INTERNAL_EMP_ID" in result.sanitized_text
    assert "<US_SSN_1>" in result.sanitized_text or "<US_SSN" in result.sanitized_text
    assert "<EMAIL_1>" in result.sanitized_text or "<EMAIL" in result.sanitized_text
    assert result.has_pii is True
    print("All PII sanitization assertions passed successfully.")
