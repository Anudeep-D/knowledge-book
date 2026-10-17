"""Classic Microservices Resilience & Structural Patterns in Modern Python (3.11+).

Demonstrates:
1. Circuit Breaker Pattern using `tenacity`, `httpx`, and stateful sliding window.
2. Strategy Pattern using `typing.Protocol` and Pydantic v2.
3. Repository Pattern abstracting conversational state and vector embeddings.
"""

from __future__ import annotations

import asyncio
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

import httpx
from pydantic import BaseModel, Field
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


# ============================================================================
# 1. CIRCUIT BREAKER PATTERN (Resilience for Unstable External APIs)
# ============================================================================

class CircuitState(str, Enum):
    CLOSED = "CLOSED"       # Normal operation; calls proceed.
    OPEN = "OPEN"           # Trips after threshold failures; calls fail-fast.
    HALF_OPEN = "HALF_OPEN" # Canary probe testing downstream health.


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected immediately because breaker is OPEN."""
    pass


class CircuitBreaker:
    """Production stateful Circuit Breaker for HTTP endpoints (LLM APIs, microservices)."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.consecutive_successes = 0
        self.last_state_change = time.monotonic()
        self._lock = asyncio.Lock()

    async def can_execute(self) -> bool:
        async with self._lock:
            now = time.monotonic()
            if self.state == CircuitState.OPEN:
                if now - self.last_state_change >= self.recovery_timeout:
                    print("[CIRCUIT BREAKER] Recovery timeout elapsed. Transitioning OPEN -> HALF-OPEN.")
                    self.state = CircuitState.HALF_OPEN
                    self.consecutive_successes = 0
                    self.last_state_change = now
                    return True
                return False
            return True

    async def record_success(self):
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.consecutive_successes += 1
                if self.consecutive_successes >= self.half_open_success_threshold:
                    print("[CIRCUIT BREAKER] Canary probes succeeded. Transitioning HALF-OPEN -> CLOSED.")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    async def record_failure(self):
        async with self._lock:
            self.failure_count += 1
            now = time.monotonic()
            if self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
                if self.failure_count >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
                    print(f"[CIRCUIT BREAKER] Threshold breached ({self.failure_count} failures). Transitioning to OPEN.")
                    self.state = CircuitState.OPEN
                    self.last_state_change = now


class ResilientHTTPClient:
    """Combines Tenacity exponential backoff with stateful Circuit Breaker protection."""

    def __init__(self, breaker: Optional[CircuitBreaker] = None):
        self.breaker = breaker or CircuitBreaker()
        self.client = httpx.AsyncClient(timeout=10.0)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
        reraise=True,
    )
    async def _execute_with_retry(self, url: str) -> Dict[str, Any]:
        resp = await self.client.get(url)
        resp.raise_for_status()
        return resp.json()

    async def call(self, url: str, fallback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not await self.breaker.can_execute():
            if fallback_data is not None:
                print(f"[FALLBACK] Circuit OPEN for {url}. Serving degraded cache.")
                return fallback_data
            raise CircuitBreakerOpenException(f"Circuit Breaker is OPEN for endpoint {url}")

        try:
            result = await self._execute_with_retry(url)
            await self.breaker.record_success()
            return result
        except Exception as exc:
            await self.breaker.record_failure()
            if fallback_data is not None:
                print(f"[FALLBACK] Request failed ({exc}). Serving fallback response.")
                return fallback_data
            raise


# ============================================================================
# 2. STRATEGY PATTERN (Pluggable Model Inference Strategies)
# ============================================================================

class InferencePayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    generated_text: str
    tokens_used: int
    provider: str
    latency_ms: float


@runtime_checkable
class LLMInferenceStrategy(Protocol):
    """Protocol establishing the structural contract for model providers."""
    async def generate(self, payload: InferencePayload) -> InferenceResponse:
        ...


class VLLMLocalStrategy:
    """Strategy for self-hosted local vLLM inference engine."""
    def __init__(self, endpoint: str = "http://localhost:8000/v1"):
        self.endpoint = endpoint

    async def generate(self, payload: InferencePayload) -> InferenceResponse:
        t0 = time.monotonic()
        await asyncio.sleep(0.05)  # Simulate local GPU tensor forward pass
        latency = (time.monotonic() - t0) * 1000
        return InferenceResponse(
            generated_text=f"[vLLM Local Output for: '{payload.prompt[:20]}...']",
            tokens_used=128,
            provider="vLLM-Local-H100",
            latency_ms=round(latency, 2),
        )


class CloudAnthropicStrategy:
    """Strategy for Claude API fallback invocation."""
    def __init__(self, api_key: str = "mock-key"):
        self.api_key = api_key

    async def generate(self, payload: InferencePayload) -> InferenceResponse:
        t0 = time.monotonic()
        await asyncio.sleep(0.12)  # Simulate WAN network hop + API processing
        latency = (time.monotonic() - t0) * 1000
        return InferenceResponse(
            generated_text=f"[Claude 3.5 Sonnet Output for: '{payload.prompt[:20]}...']",
            tokens_used=135,
            provider="Anthropic-Claude-3.5",
            latency_ms=round(latency, 2),
        )


class ModelInferenceContext:
    """Runtime context executing the configured inference strategy."""
    def __init__(self, strategy: LLMInferenceStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: LLMInferenceStrategy):
        self._strategy = strategy

    async def execute(self, payload: InferencePayload) -> InferenceResponse:
        return await self._strategy.generate(payload)


# ============================================================================
# 3. REPOSITORY PATTERN (Abstracting Conversational State & Memory)
# ============================================================================

class ConversationMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str
    timestamp: float = Field(default_factory=time.time)


@runtime_checkable
class ConversationRepository(Protocol):
    """Abstract Repository for session state and history persistence."""
    async def save_message(self, session_id: str, message: ConversationMessage) -> None:
        ...

    async def get_history(self, session_id: str, limit: int = 10) -> List[ConversationMessage]:
        ...


class InMemoryConversationRepository:
    """Thread-safe in-memory repository implementation with sliding-window support."""
    def __init__(self):
        self._store: Dict[str, List[ConversationMessage]] = {}
        self._lock = asyncio.Lock()

    async def save_message(self, session_id: str, message: ConversationMessage) -> None:
        async with self._lock:
            if session_id not in self._store:
                self._store[session_id] = []
            self._store[session_id].append(message)

    async def get_history(self, session_id: str, limit: int = 10) -> List[ConversationMessage]:
        async with self._lock:
            messages = self._store.get(session_id, [])
            return messages[-limit:]
