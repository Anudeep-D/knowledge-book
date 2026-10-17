"""
evals_otel_harness.py
Enterprise LLMOps Evaluation Suite and OpenTelemetry GenAI Tracing Instrumentation.

Demonstrates:
1. OpenTelemetry GenAI Semantic Conventions (Hierarchical Span Trees & Token Accounting).
2. The RAG Triad Automated Evaluation Scorer (Context Groundedness, Query Relevance).
3. Automated CI/CD Assertion Gates for Stochastic Agent Outputs.
4. Egress Hallucination Detection & Diagnostic Logging.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("evals-otel-harness")


# ============================================================================
# 1. OPENTELEMETRY GENAI SEMANTIC SPAN TRACER
# ============================================================================

@dataclass
class GenAISpanRecord:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    system: str = "openai"
    request_model: str = "gpt-4o"
    temperature: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    duration_ms: float = 0.0
    status: str = "OK"
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class OpenTelemetryAgentTracer:
    """
    Traces multi-agent workflows using OpenTelemetry GenAI semantic conventions.
    Captures hierarchical spans: root agent -> worker tools -> LLM completions.
    """

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans: list[GenAISpanRecord] = []

    def start_span(
        self,
        name: str,
        parent_span_id: Optional[str] = None,
        model: str = "gpt-4o",
        attributes: Optional[dict[str, Any]] = None,
    ) -> str:
        span_id = f"span-{len(self.spans) + 1:04d}"
        span = GenAISpanRecord(
            trace_id=self.trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            request_model=model,
            attributes=attributes or {},
        )
        self.spans.append(span)
        logger.info(f"[OTel Tracer] Started span '{name}' ({span_id}) | Parent: {parent_span_id}")
        return span_id

    def end_span(
        self,
        span_id: str,
        status: str = "OK",
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        duration_ms: float = 0.0,
    ) -> None:
        for span in self.spans:
            if span.span_id == span_id:
                span.status = status
                span.prompt_tokens = prompt_tokens
                span.completion_tokens = completion_tokens
                span.duration_ms = duration_ms
                logger.info(
                    f"[OTel EXPORT] Span '{span.name}' ({span.span_id}) closed | "
                    f"Status: {status} | Duration: {duration_ms:.1f}ms | Tokens: {span.total_tokens}"
                )
                return
        raise KeyError(f"Span ID '{span_id}' not found.")

    def export_summary(self) -> dict[str, Any]:
        """Calculates aggregated trace telemetry."""
        total_tokens = sum(s.total_tokens for s in self.spans)
        total_duration = sum(s.duration_ms for s in self.spans)
        return {
            "trace_id": self.trace_id,
            "total_spans": len(self.spans),
            "total_tokens_consumed": total_tokens,
            "cumulative_duration_ms": round(total_duration, 2),
            "root_spans": [s.span_id for s in self.spans if s.parent_span_id is None],
        }


# ============================================================================
# 2. AUTOMATED EVALUATION HARNESS (THE RAG TRIAD & FAITHFULNESS)
# ============================================================================

class EvaluationResult(BaseModel):
    groundedness_score: float = Field(ge=0.0, le=1.0, description="Faithfulness to source context.")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance to user query keywords.")
    passed_sla: bool
    diagnostic: str


class EnterpriseAgentEvaluator:
    """
    Evaluates agent outputs against strict ground-truth and semantic SLAs.
    Can be run inline as an egress guardrail or inside CI/CD test runs.
    """

    def __init__(self, min_groundedness: float = 0.75, min_relevance: float = 0.50):
        self.min_groundedness = min_groundedness
        self.min_relevance = min_relevance

    def evaluate_response(
        self,
        user_prompt: str,
        retrieved_contexts: list[str],
        generated_answer: str,
    ) -> EvaluationResult:
        """
        Calculates context groundedness (hallucination check) and query relevance.
        """
        clean_context = " ".join(retrieved_contexts).lower()
        clean_answer = generated_answer.lower()
        clean_query = user_prompt.lower()

        answer_tokens = set(re_tokenize(clean_answer))
        context_tokens = set(re_tokenize(clean_context))
        query_tokens = set(re_tokenize(clean_query))

        # 1. Groundedness / Faithfulness: % of generated content supported by retrieved context
        supported_tokens = answer_tokens.intersection(context_tokens)
        groundedness = round(len(supported_tokens) / max(len(answer_tokens), 1), 2)

        # 2. Query Relevance: % of query keywords addressed in candidate answer
        addressed_tokens = query_tokens.intersection(answer_tokens)
        relevance = round(len(addressed_tokens) / max(len(query_tokens), 1), 2)

        passed = (groundedness >= self.min_groundedness) and (relevance >= self.min_relevance)

        diag = (
            f"Groundedness: {groundedness:.2f} (SLA >= {self.min_groundedness}) | "
            f"Relevance: {relevance:.2f} (SLA >= {self.min_relevance}) | "
            f"Verdict: {'PASS' if passed else 'FAIL'}"
        )

        return EvaluationResult(
            groundedness_score=groundedness,
            relevance_score=relevance,
            passed_sla=passed,
            diagnostic=diag,
        )


def re_tokenize(text: str) -> list[str]:
    """Helper token splitter filtering punctuation and basic stopwords."""
    stopwords = {"the", "a", "an", "is", "for", "and", "in", "to", "of", "with", "on", "at", "by", "this", "that"}
    words = [w.strip(".,;:?!'\"()[]{}") for w in text.split()]
    return [w for w in words if len(w) > 2 and w not in stopwords]


# ============================================================================
# 3. CI/CD TEST HARNESS & DEMONSTRATION RUNNER
# ============================================================================

def run_ci_eval_suite():
    tracer = OpenTelemetryAgentTracer(trace_id="trace-prod-ci-00892")
    evaluator = EnterpriseAgentEvaluator(min_groundedness=0.70, min_relevance=0.50)

    print("\n--- Phase 1: Recording OpenTelemetry GenAI Span Hierarchy ---")
    # 1. Root Agent Span
    root_span_id = tracer.start_span(
        name="agent.research_supervisor",
        parent_span_id=None,
        model="supervisor-graph-v2",
        attributes={"tenant_id": "enterprise-compliance", "environment": "production"},
    )

    # 2. Child Tool Span
    tool_span_id = tracer.start_span(
        name="tool.vector_search",
        parent_span_id=root_span_id,
        model="bge-large-en-v1.5",
        attributes={"top_k": 3, "index": "sec_filings_2025"},
    )
    tracer.end_span(tool_span_id, status="OK", duration_ms=48.2)

    # 3. Child LLM Completion Span
    llm_span_id = tracer.start_span(
        name="gen_ai.llm.completion",
        parent_span_id=root_span_id,
        model="gpt-4o-2024-08-06",
        attributes={"gen_ai.request.temperature": 0.0},
    )
    tracer.end_span(
        llm_span_id,
        status="OK",
        prompt_tokens=520,
        completion_tokens=94,
        duration_ms=412.8,
    )

    # Close Root Span
    tracer.end_span(root_span_id, status="OK", duration_ms=475.0)

    trace_metrics = tracer.export_summary()
    print("\nExported Trace Summary:")
    print(f"  Trace ID: {trace_metrics['trace_id']}")
    print(f"  Total Spans: {trace_metrics['total_spans']}")
    print(f"  Total Token Consumption: {trace_metrics['total_tokens_consumed']}")
    print(f"  Total Pipeline Latency: {trace_metrics['cumulative_duration_ms']}ms")

    print("\n--- Phase 2: Testing RAG Triad Evaluation Assertions ---")
    query = "What is the penalty for late regulatory tax filing in Oregon?"
    source_context = [
        "Oregon Revised Statute ORS-314 dictates that corporate late tax filings incur a monthly penalty of 5%.",
        "The cumulative maximum penalty under ORS-314 cannot exceed 25% of the total tax liability.",
    ]

    # Test Case A: Compliant, Grounded Response
    valid_answer = (
        "Under Oregon Statute ORS-314, corporate late tax filings incur a 5% monthly penalty, "
        "capped at a maximum of 25% of the total liability."
    )
    result_valid = evaluator.evaluate_response(query, source_context, valid_answer)
    print(f"\n[Test Case A - Grounded Response]:\n  {result_valid.diagnostic}")
    assert result_valid.passed_sla is True, f"Failed SLA: {result_valid.diagnostic}"

    # Test Case B: Hallucinated / Contradictory Response
    hallucinated_answer = (
        "Oregon law imposes an automatic flat fine of $25,000 and revokes the corporate charter immediately."
    )
    result_hallucinated = evaluator.evaluate_response(query, source_context, hallucinated_answer)
    print(f"\n[Test Case B - Hallucinated Response]:\n  {result_hallucinated.diagnostic}")
    assert result_hallucinated.passed_sla is False, "Evaluator failed to catch severe hallucination!"

    print("\nSUCCESS: evals_otel_harness.py verified with OTel GenAI tracing and assertion gates!")


if __name__ == "__main__":
    run_ci_eval_suite()
