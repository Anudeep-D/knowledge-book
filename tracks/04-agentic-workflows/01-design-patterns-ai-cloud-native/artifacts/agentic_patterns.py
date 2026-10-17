"""AI & Agentic Design Patterns in Modern Python (3.11+).

Demonstrates:
1. Semantic Router Pattern (Intent routing with confidence thresholds).
2. Supervisor-Worker Pattern (Hierarchical task decomposition & aggregation).
3. Evaluator-Optimizer Pattern (Iterative self-correction feedback loop).
"""

from __future__ import annotations

import asyncio
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


# ============================================================================
# 1. SEMANTIC ROUTER PATTERN (Intent-Based Dynamic Dispatch)
# ============================================================================

class IntentRoute(str, Enum):
    DATABASE_QUERY = "DATABASE_QUERY"
    CODE_ANALYSIS = "CODE_ANALYSIS"
    GENERAL_KNOWLEDGE = "GENERAL_KNOWLEDGE"


class RouteDecision(BaseModel):
    query: str
    selected_route: IntentRoute
    confidence_score: float = Field(ge=0.0, le=1.0)
    routing_rationale: str


class SemanticRouter:
    """Classifies user intent and routes to specialized pipelines or prompts."""

    def __init__(self, fallback_route: IntentRoute = IntentRoute.GENERAL_KNOWLEDGE):
        self.fallback_route = fallback_route
        self._handlers: Dict[IntentRoute, Callable[[str], asyncio.Future]] = {}

    def register_route(self, route: IntentRoute, handler: Callable[[str], Any]):
        self._handlers[route] = handler

    async def classify_intent(self, query: str) -> RouteDecision:
        """Evaluates query semantics to choose the optimal specialized worker."""
        lowered = query.lower()
        if any(keyword in lowered for keyword in ("sql", "select", "table", "postgres", "database")):
            return RouteDecision(
                query=query,
                selected_route=IntentRoute.DATABASE_QUERY,
                confidence_score=0.94,
                routing_rationale="Detected relational database schema and SQL syntax keywords.",
            )
        elif any(keyword in lowered for keyword in ("def ", "class ", "function", "bug", "traceback")):
            return RouteDecision(
                query=query,
                selected_route=IntentRoute.CODE_ANALYSIS,
                confidence_score=0.91,
                routing_rationale="Detected code snippet and exception keywords.",
            )
        return RouteDecision(
            query=query,
            selected_route=self.fallback_route,
            confidence_score=0.65,
            routing_rationale="No specialized domain keywords matched; routing to general LLM.",
        )

    async def dispatch(self, query: str) -> Dict[str, Any]:
        decision = await self.classify_intent(query)
        handler = self._handlers.get(decision.selected_route)
        if not handler:
            raise ValueError(f"No handler registered for route: {decision.selected_route}")
        result = await handler(query)
        return {
            "decision": decision.model_dump(),
            "result": result,
        }


# ============================================================================
# 2. SUPERVISOR-WORKER PATTERN (Hierarchical Multi-Agent Topology)
# ============================================================================

class SubTask(BaseModel):
    task_id: str
    worker_type: str = Field(..., description="Target specialist: e.g., 'researcher', 'coder'")
    instruction: str


class WorkerOutput(BaseModel):
    task_id: str
    status: str
    payload: str


class AggregatedPlan(BaseModel):
    plan_title: str
    subtasks: List[SubTask]
    completed_results: List[WorkerOutput] = Field(default_factory=list)


class SupervisorAgent:
    """Orchestrates work decomposition, concurrent worker dispatch, and aggregation."""

    def __init__(self):
        self.workers = {
            "researcher": self._researcher_worker,
            "coder": self._coder_worker,
        }

    async def _researcher_worker(self, task: SubTask) -> WorkerOutput:
        await asyncio.sleep(0.05)  # Simulate search retrieval
        return WorkerOutput(
            task_id=task.task_id,
            status="SUCCESS",
            payload=f"Research synthesis: {task.instruction} verified against docs.",
        )

    async def _coder_worker(self, task: SubTask) -> WorkerOutput:
        await asyncio.sleep(0.08)  # Simulate code generation
        return WorkerOutput(
            task_id=task.task_id,
            status="SUCCESS",
            payload=f"Implementation: generated clean Python code for '{task.instruction}'.",
        )

    async def decompose_goal(self, goal: str) -> List[SubTask]:
        """Breaks a high-level user goal into disjoint worker tasks."""
        return [
            SubTask(task_id="task-1", worker_type="researcher", instruction=f"Gather specifications for {goal}"),
            SubTask(task_id="task-2", worker_type="coder", instruction=f"Write test harness for {goal}"),
        ]

    async def run(self, goal: str) -> AggregatedPlan:
        subtasks = await self.decompose_goal(goal)
        print(f"[SUPERVISOR] Decomposed goal into {len(subtasks)} subtasks. Dispatching in parallel...")

        # Concurrently dispatch subtasks to assigned worker functions
        tasks_to_run = [self.workers[st.worker_type](st) for st in subtasks]
        results = await asyncio.gather(*tasks_to_run)

        print("[SUPERVISOR] All worker results received. Synthesizing final response...")
        return AggregatedPlan(
            plan_title=f"Execution Plan: {goal}",
            subtasks=subtasks,
            completed_results=list(results),
        )


# ============================================================================
# 3. EVALUATOR-OPTIMIZER PATTERN (Iterative Refinement Loop)
# ============================================================================

class EvaluationResult(BaseModel):
    score: int = Field(ge=0, le=100, description="Quality score from 0-100")
    passed: bool
    critique: str
    remediation_suggestions: List[str]


class EvaluatorOptimizerEngine:
    """Iterative generator-critic loop with termination guardrails."""

    def __init__(self, passing_score: int = 85, max_iterations: int = 3):
        self.passing_score = passing_score
        self.max_iterations = max_iterations

    async def _generator(self, prompt: str, feedback: Optional[str] = None) -> str:
        """Simulates LLM producing content, incorporating previous feedback."""
        await asyncio.sleep(0.04)
        if not feedback:
            return f"Draft output addressing '{prompt}' (Initial Attempt: missing edge cases)"
        return f"Refined output addressing '{prompt}' (Incorporated critique: {feedback})"

    async def _evaluator(self, output: str, iteration: int) -> EvaluationResult:
        """Evaluator judge checking against quality rubrics."""
        await asyncio.sleep(0.03)
        # Simulate convergence over iterations
        if iteration == 1:
            return EvaluationResult(
                score=65,
                passed=False,
                critique="Draft lacks explicit error handling and bounds checking.",
                remediation_suggestions=["Add input validation with Pydantic", "Enforce timeout constraints"],
            )
        return EvaluationResult(
            score=92,
            passed=True,
            critique="Output satisfies all resilience criteria and type safety guarantees.",
            remediation_suggestions=[],
        )

    async def execute(self, prompt: str) -> Dict[str, Any]:
        iteration = 1
        current_feedback = None
        history = []

        while iteration <= self.max_iterations:
            print(f"[LOOP] Starting iteration {iteration}/{self.max_iterations}...")
            draft = await self._generator(prompt, feedback=current_feedback)
            evaluation = await self._evaluator(draft, iteration=iteration)

            history.append({
                "iteration": iteration,
                "draft": draft,
                "evaluation": evaluation.model_dump(),
            })

            if evaluation.passed or evaluation.score >= self.passing_score:
                print(f"[LOOP] Convergence reached at iteration {iteration} (Score: {evaluation.score}/100)!")
                return {
                    "status": "CONVERGED",
                    "final_output": draft,
                    "iterations_used": iteration,
                    "history": history,
                }

            current_feedback = f"{evaluation.critique} Suggestions: {', '.join(evaluation.remediation_suggestions)}"
            iteration += 1

        print(f"[LOOP] Warning: Maximum iterations ({self.max_iterations}) exceeded without passing score.")
        return {
            "status": "MAX_ITERATIONS_EXCEEDED",
            "final_output": draft,
            "iterations_used": self.max_iterations,
            "history": history,
        }
