"""
supervisor_langgraph.py
Production Multi-Agent Supervisor-Worker Topology using Cyclic State Graphs.

Demonstrates:
1. Typed State with Immutable Reducers (operator.add) to prevent state overwrites.
2. Structured Supervisor Routing Schema (Pydantic v2).
3. Hard Recursion Guardrail to prevent infinite agentic token burn.
4. Cyclic Worker Handoff: Specialized workers always report back to Supervisor.
5. Asynchronous Graph Execution Engine.
"""

from __future__ import annotations

import asyncio
import logging
import operator
from dataclasses import dataclass
from typing import Annotated, Any, Callable, Dict, List, Literal, Sequence, TypedDict, Union
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("langgraph-supervisor")


# ============================================================================
# MESSAGE SCHEMAS & LANGGRAPH RUNTIME ENGINE
# ============================================================================

@dataclass
class Message:
    role: str
    content: str


class HumanMessage(Message):
    def __init__(self, content: str):
        super().__init__(role="human", content=content)


class AIMessage(Message):
    def __init__(self, content: str):
        super().__init__(role="ai", content=content)


class ToolMessage(Message):
    def __init__(self, content: str, tool_name: str = ""):
        super().__init__(role="tool", content=content)
        self.tool_name = tool_name


# ============================================================================
# 1. TYPED WORKFLOW STATE DEFINITION WITH REDUCERS
# ============================================================================

class AgentWorkflowState(TypedDict):
    """
    Immutable state passed across graph nodes.
    `messages` and `sql_records` use `operator.add` so nodes append rather than overwrite.
    """
    messages: Annotated[Sequence[Message], operator.add]
    next_step: str
    iteration_count: Annotated[int, operator.add]
    sql_records: Annotated[list[dict[str, Any]], operator.add]
    search_notes: Annotated[list[str], operator.add]
    is_complete: bool


# ============================================================================
# 2. STRUCTURED SUPERVISOR ROUTING SCHEMA (PYDANTIC V2)
# ============================================================================

class SupervisorRoutingDecision(BaseModel):
    """Deterministic routing schema enforced via structured LLM decoding."""
    next_worker: Literal["sql_worker", "search_worker", "synthesizer", "FINISH"] = Field(
        description="The next specialized agent node to execute, or FINISH when resolved."
    )
    instruction: str = Field(
        description="Specific instructions for the selected worker."
    )
    rationale: str = Field(
        description="Reasoning behind selecting this worker."
    )


# ============================================================================
# 3. SPECIALIZED WORKER NODES
# ============================================================================

async def supervisor_node(state: AgentWorkflowState) -> dict[str, Any]:
    """
    Supervisor router node that evaluates accumulated state and directs flow.
    Enforces a strict recursion limit.
    """
    current_iteration = state.get("iteration_count", 0)
    logger.info(f"[Supervisor Node] Evaluating iteration #{current_iteration}...")

    # Hard circuit breaker to prevent infinite loops
    if current_iteration >= 5:
        logger.warning("[Supervisor Node] Recursion ceiling (5) reached! Forcing FINISH.")
        return {
            "next_step": "FINISH",
            "iteration_count": 1,
            "is_complete": True,
            "messages": [AIMessage("[GUARDRAIL TRIGGERED]: Max recursion limit reached. Aborting.")],
        }

    # Deterministic simulation of structured LLM output (e.g. gpt-4o with_structured_output)
    if not state.get("sql_records"):
        decision = SupervisorRoutingDecision(
            next_worker="sql_worker",
            instruction="Extract Q3 enterprise revenue and margin metrics from database.",
            rationale="User requested quarterly financial performance data.",
        )
    elif not state.get("search_notes"):
        decision = SupervisorRoutingDecision(
            next_worker="search_worker",
            instruction="Query market analyst benchmarks for Q3 enterprise software sector.",
            rationale="Context needed to compare internal metrics with external benchmark.",
        )
    elif state.get("next_step") != "synthesizer":
        decision = SupervisorRoutingDecision(
            next_worker="synthesizer",
            instruction="Synthesize internal SQL metrics with external market benchmarks.",
            rationale="All necessary data collected.",
        )
    else:
        decision = SupervisorRoutingDecision(
            next_worker="FINISH",
            instruction="Return executive summary to client.",
            rationale="Synthesis verified.",
        )

    return {
        "next_step": decision.next_worker,
        "iteration_count": 1,
        "is_complete": (decision.next_worker == "FINISH"),
        "messages": [AIMessage(f"[Supervisor] Routing to '{decision.next_worker}': {decision.instruction}")],
    }


async def sql_worker_node(state: AgentWorkflowState) -> dict[str, Any]:
    """Specialized database worker executing read-only parameter-bound SQL queries."""
    logger.info("[SQL Worker] Executing parameterized query...")
    await asyncio.sleep(0.02)
    # Simulated query execution
    records = [{"quarter": "Q3-2025", "revenue_usd": 14_850_000, "ebitda_margin": 0.228}]
    return {
        "sql_records": records,
        "messages": [ToolMessage(content="Extracted SQL: Q3 Revenue=$14.85M, EBITDA=22.8%", tool_name="sql_query")],
    }


async def search_worker_node(state: AgentWorkflowState) -> dict[str, Any]:
    """Specialized RAG worker executing semantic document retrieval."""
    logger.info("[Search Worker] Performing vector semantic search...")
    await asyncio.sleep(0.02)
    benchmark_note = "Industry average software SaaS operating margin in Q3 was 19.4%."
    return {
        "search_notes": [benchmark_note],
        "messages": [ToolMessage(content=f"Retrieved benchmark: '{benchmark_note}'", tool_name="rag_search")],
    }


async def synthesizer_node(state: AgentWorkflowState) -> dict[str, Any]:
    """Aggregates multi-source evidence into a structured answer."""
    logger.info("[Synthesizer] Merging SQL records with market benchmarks...")
    sql = state["sql_records"][0] if state.get("sql_records") else {}
    notes = "; ".join(state.get("search_notes", []))

    summary = (
        f"Executive Performance Briefing: Enterprise generated ${sql.get('revenue_usd', 0):,} "
        f"in Q3 with a {sql.get('ebitda_margin', 0)*100:.1f}% EBITDA margin. "
        f"This outperforms the industry benchmark ({notes})."
    )
    return {
        "next_step": "FINISH",
        "is_complete": True,
        "messages": [AIMessage(f"[Final Briefing]: {summary}")],
    }


# ============================================================================
# 4. GRAPH ENGINE & CYCLIC DISPATCHER
# ============================================================================

class CyclicStateGraphRunner:
    """
    Executes a cyclic actor-model state machine honoring LangGraph semantics.
    Workers report back to the supervisor until `FINISH` is achieved.
    """

    def __init__(self):
        self.nodes: Dict[str, Callable[[AgentWorkflowState], Coroutine[Any, Any, dict[str, Any]]]] = {
            "supervisor": supervisor_node,
            "sql_worker": sql_worker_node,
            "search_worker": search_worker_node,
            "synthesizer": synthesizer_node,
        }

    async def invoke(self, initial_state: AgentWorkflowState) -> AgentWorkflowState:
        state = dict(initial_state)

        while not state.get("is_complete", False):
            # 1. Supervisor evaluates current state
            sup_update = await self.nodes["supervisor"](state)
            self._apply_update(state, sup_update)

            target = state.get("next_step")
            if target == "FINISH" or state.get("is_complete", False):
                break

            # 2. Dispatch to designated worker
            if target in self.nodes:
                worker_update = await self.nodes[target](state)
                self._apply_update(state, worker_update)
            else:
                raise ValueError(f"Unknown node target: {target}")

        return state

    @staticmethod
    def _apply_update(state: dict[str, Any], update: dict[str, Any]) -> None:
        """Applies state updates using appropriate field reducers."""
        for k, v in update.items():
            if k in ("messages", "sql_records", "search_notes"):
                existing = state.get(k, [])
                state[k] = list(existing) + list(v)
            elif k == "iteration_count":
                state[k] = state.get(k, 0) + v
            else:
                state[k] = v


# ============================================================================
# VERIFICATION HARNESS
# ============================================================================

if __name__ == "__main__":
    runner = CyclicStateGraphRunner()

    initial_input: AgentWorkflowState = {
        "messages": [HumanMessage("Prepare Q3 financial performance review against market benchmarks.")],
        "next_step": "supervisor",
        "iteration_count": 0,
        "sql_records": [],
        "search_notes": [],
        "is_complete": False,
    }

    final_state = asyncio.run(runner.invoke(initial_input))

    print("\n--- Execution Completed Successfully ---")
    print(f"Total Iterations: {final_state['iteration_count']}")
    print(f"SQL Records Extracted: {len(final_state['sql_records'])}")
    print(f"Search Benchmarks Retrieved: {len(final_state['search_notes'])}")
    print(f"Total Messages Logged: {len(final_state['messages'])}")

    print("\nState Message History:")
    for m in final_state["messages"]:
        print(f"  [{m.role.upper()}]: {m.content}")

    assert final_state["is_complete"] is True
    assert len(final_state["sql_records"]) == 1
    assert len(final_state["search_notes"]) == 1
    print("\nSUCCESS: supervisor_langgraph.py verified with cyclic state handoffs!")
