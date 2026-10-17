#!/usr/bin/env python3
"""
artifacts/agent_memory_manager.py
Enterprise Multi-Tier State Persistence & Memory Manager for Autonomous AI Agents.

Demonstrates:
1. Tier 1 & 2: Low-latency working scratchpad in Redis with TTLs and distributed locks.
2. Sub-agent concurrency arbitration: Atomic mutex leases preventing race conditions.
3. Sliding window eviction and asynchronous consolidation into Tier 3 persistent episodic memory.
"""

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import json
import time
from typing import Any, AsyncGenerator, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentStepEvent(BaseModel):
    step_id: int
    role: str
    action: str
    payload: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)


class AgentSessionState(BaseModel):
    session_id: str
    agent_id: str
    working_scratchpad: List[AgentStepEvent] = Field(default_factory=list)
    turn_count: int = 0
    updated_at: float = Field(default_factory=time.time)


@dataclass
class MockRedisClient:
    """In-memory Redis mock supporting async GET, SET (with NX/EX), and DEL."""
    store: Dict[str, str] = field(default_factory=dict)
    expiries: Dict[str, float] = field(default_factory=dict)

    async def get(self, key: str) -> Optional[str]:
        if key in self.expiries and time.time() > self.expiries[key]:
            del self.store[key]
            del self.expiries[key]
            return None
        return self.store.get(key)

    async def set(
        self, key: str, value: str, nx: bool = False, ex: Optional[int] = None
    ) -> bool:
        now = time.time()
        if nx and key in self.store:
            if key not in self.expiries or now <= self.expiries[key]:
                return False  # Key exists and not expired
        self.store[key] = value
        if ex:
            self.expiries[key] = now + ex
        return True

    async def delete(self, key: str) -> int:
        if key in self.store:
            del self.store[key]
            self.expiries.pop(key, None)
            return 1
        return 0


class TieredMemoryManager:
    """Orchestrates Tier 1 ephemeral working RAM, Tier 2 Redis, and Tier 3 long-term consolidation."""

    def __init__(self, redis_client: Any, max_scratchpad_steps: int = 5):
        self.redis = redis_client
        self.max_scratchpad_steps = max_scratchpad_steps
        self.session_ttl_seconds = 86400  # 24 Hours
        self.long_term_consolidated: List[Dict[str, Any]] = []

    @asynccontextmanager
    async def acquire_session_lock(
        self, session_id: str, timeout_sec: float = 3.0
    ) -> AsyncGenerator[None, None]:
        """Distributed lock (mutex lease) preventing race conditions across concurrent sub-agents."""
        lock_key = f"lock:agent:session:{session_id}"
        acquired = await self.redis.set(lock_key, "locked", nx=True, ex=int(timeout_sec))
        if not acquired:
            raise TimeoutError(f"Could not acquire session lock for {session_id} within timeout.")
        try:
            yield
        finally:
            await self.redis.delete(lock_key)

    async def get_or_create_session(self, session_id: str, agent_id: str) -> AgentSessionState:
        """Loads session from Redis buffer or initializes a fresh session state."""
        raw_state = await self.redis.get(f"session:agent:{session_id}")
        if raw_state:
            return AgentSessionState.model_validate_json(raw_state)
        return AgentSessionState(session_id=session_id, agent_id=agent_id)

    async def commit_agent_step(
        self, state: AgentSessionState, event: AgentStepEvent
    ) -> None:
        """Appends step payload, bounds scratchpad token window, and triggers async consolidation."""
        async with self.acquire_session_lock(state.session_id):
            state.working_scratchpad.append(event)
            state.turn_count += 1
            state.updated_at = time.time()

            # Bound Working Context: Evict older steps when exceeding buffer limit
            if len(state.working_scratchpad) > self.max_scratchpad_steps:
                overflow_count = len(state.working_scratchpad) - self.max_scratchpad_steps
                evicted_steps = state.working_scratchpad[:overflow_count]
                state.working_scratchpad = state.working_scratchpad[overflow_count:]
                
                # Asynchronously consolidate evicted steps into Tier 3 long-term memory
                asyncio.create_task(self._consolidate_to_long_term(state.agent_id, evicted_steps))

            # Commit updated state to Redis buffer with sliding TTL
            await self.redis.set(
                f"session:agent:{state.session_id}",
                state.model_dump_json(),
                ex=self.session_ttl_seconds
            )

    async def _consolidate_to_long_term(
        self, agent_id: str, evicted_steps: List[AgentStepEvent]
    ) -> None:
        """Background worker extracting episodic facts and writing to persistent storage."""
        await asyncio.sleep(0.01)  # Simulate LLM reflection and embedding generation
        for step in evicted_steps:
            record = {
                "agent_id": agent_id,
                "extracted_fact": f"Step {step.step_id} executed action '{step.action}' with payload: {step.payload}",
                "importance_weight": 8,
                "timestamp": step.timestamp
            }
            self.long_term_consolidated.append(record)
        print(f"[CONSOLIDATION] Consolidated {len(evicted_steps)} evicted step(s) into Tier 3 Long-Term Memory.")


async def simulate_multi_agent_execution():
    """Simulates two parallel sub-agents coordinating through the TieredMemoryManager."""
    print("\n================ MULTI-AGENT STATE PERSISTENCE SIMULATION ================")
    redis_mock = MockRedisClient()
    memory_manager = TieredMemoryManager(redis_client=redis_mock, max_scratchpad_steps=3)

    session_id = "sess-prod-892"
    agent_id = "agent-infra-orchestrator"

    # Step 1: Initialize session
    state = await memory_manager.get_or_create_session(session_id, agent_id)
    print(f"Initialized Session: {state.session_id} (Turn count: {state.turn_count})")

    # Step 2: Append steps triggering sliding window eviction
    for i in range(1, 6):
        event = AgentStepEvent(
            step_id=i,
            role="assistant",
            action=f"deploy_microservice_pod_{i}",
            payload={"cluster": "us-east-k8s", "replicas": i * 2}
        )
        await memory_manager.commit_agent_step(state, event)
        print(f"Step {i} committed. In-Memory Scratchpad Length: {len(state.working_scratchpad)}")

    # Allow async background consolidation to settle
    await asyncio.sleep(0.05)

    # Step 3: Verify consolidated long-term store
    print(f"\nFinal Active Working Scratchpad Length: {len(state.working_scratchpad)}")
    print(f"Total Tier 3 Consolidated Long-Term Memories: {len(memory_manager.long_term_consolidated)}")
    for mem in memory_manager.long_term_consolidated:
        print(f"  * {mem['extracted_fact']}")
    print("========================================================================\n")


if __name__ == "__main__":
    asyncio.run(simulate_multi_agent_execution())
