"""
hitl_checkpoint_agent.py
Enterprise Human-in-the-Loop (HITL) Agent with State Checkpointing & Time-Travel.

Demonstrates:
1. Thread-Scoped State Checkpointing (Snapshot Persistence).
2. Human-in-the-Loop Interruption Gate (interrupt_before).
3. State Inspection, Human Review, and State Mutation (update_state).
4. Safe Resumption from Saved Checkpoint.
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("hitl-agent")


# ============================================================================
# 1. TRANSACTION PAYLOAD & DOMAIN MODELS
# ============================================================================

class RefundActionPayload(BaseModel):
    """Strict schema for financial transaction tool execution."""
    account_id: str = Field(pattern=r"^ACC-\d{5}$", description="Customer account ID.")
    amount_usd: float = Field(gt=0, le=10000, description="Refund amount in USD.")
    approval_ticket: str = Field(min_length=5, description="Audited ticketing reference.")


class AgentState(BaseModel):
    """Workflow state with tracking flags and transaction parameters."""
    query: str
    target_account: str = ""
    proposed_amount: float = 0.0
    is_authorized: bool = False
    transaction_id: Optional[str] = None
    audit_log: list[str] = Field(default_factory=list)


# ============================================================================
# 2. CHECKPOINTER ENGINE (PERSISTENCE & SNAPSHOT STORE)
# ============================================================================

@dataclass
class StateSnapshot:
    thread_id: str
    step: int
    next_node: Optional[str]
    values: dict[str, Any]


class InMemoryCheckpointer:
    """Thread-safe state snapshot store for state graph persistence."""

    def __init__(self):
        self._threads: Dict[str, List[StateSnapshot]] = {}

    def save_checkpoint(self, thread_id: str, next_node: Optional[str], state_values: dict[str, Any]) -> StateSnapshot:
        if thread_id not in self._threads:
            self._threads[thread_id] = []
        
        step = len(self._threads[thread_id]) + 1
        snapshot = StateSnapshot(
            thread_id=thread_id,
            step=step,
            next_node=next_node,
            values=copy.deepcopy(state_values),
        )
        self._threads[thread_id].append(snapshot)
        logger.info(f"[Checkpointer] Saved checkpoint step #{step} for thread '{thread_id}'. Next: {next_node}")
        return snapshot

    def get_latest(self, thread_id: str) -> Optional[StateSnapshot]:
        history = self._threads.get(thread_id, [])
        return history[-1] if history else None

    def update_state(self, thread_id: str, new_values: dict[str, Any]) -> StateSnapshot:
        latest = self.get_latest(thread_id)
        if not latest:
            raise KeyError(f"Thread '{thread_id}' not found in checkpointer.")
        
        merged_values = dict(latest.values)
        merged_values.update(new_values)
        return self.save_checkpoint(thread_id, latest.next_node, merged_values)


# ============================================================================
# 3. GRAPH NODES & HIGH-PRIVILEGE TOOL
# ============================================================================

def supervisor_planner_node(state: dict[str, Any]) -> dict[str, Any]:
    """Interprets customer query and drafts refund parameters."""
    logger.info("[Planner Node] Drafting proposed refund transaction...")
    return {
        "target_account": "ACC-54321",
        "proposed_amount": 3200.00,
        "is_authorized": False,
        "audit_log": state.get("audit_log", []) + ["Supervisor: Proposed refund of $3,200.00 for ACC-54321."],
    }


def execute_refund_tool(payload: RefundActionPayload) -> dict[str, Any]:
    """External transactional banking API."""
    logger.info(f"[Banking API] DISPATCHING REFUND: ${payload.amount_usd} to {payload.account_id}")
    return {
        "status": "SETTLED",
        "tx_id": f"TX-BANK-{hash(payload.account_id + str(payload.amount_usd)) % 1000000:06d}",
        "settled_amount": payload.amount_usd,
    }


def execute_transaction_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    High-privilege node. MUST only execute after human operator authorization.
    """
    logger.info("[Transaction Node] Checking authorization before calling banking API...")
    if not state.get("is_authorized", False):
        raise PermissionError("SECURITY ALERT: Transaction attempted without human operator authorization flag!")

    payload = RefundActionPayload(
        account_id=state["target_account"],
        amount_usd=state["proposed_amount"],
        approval_ticket="JIRA-SEC-8921",
    )
    result = execute_refund_tool(payload)

    return {
        "transaction_id": result["tx_id"],
        "audit_log": state.get("audit_log", []) + [f"System: Settled refund TX {result['tx_id']} for ${payload.amount_usd}."],
    }


# ============================================================================
# 4. HITL STATE MACHINE ENGINE
# ============================================================================

class HITLStateMachine:
    """State graph orchestrator with interrupt_before gate and checkpointing."""

    def __init__(self, checkpointer: InMemoryCheckpointer, interrupt_before: list[str]):
        self.checkpointer = checkpointer
        self.interrupt_before = set(interrupt_before)

    def stream(self, thread_id: str, initial_state: Optional[dict[str, Any]] = None):
        """
        Runs graph until an interrupt gate is reached or graph completes.
        """
        # Determine starting state
        latest_snapshot = self.checkpointer.get_latest(thread_id)
        if latest_snapshot is None:
            if initial_state is None:
                raise ValueError("Must provide initial_state for a new thread.")
            current_values = dict(initial_state)
            current_node = "planner"
        else:
            current_values = dict(latest_snapshot.values)
            current_node = latest_snapshot.next_node

        while current_node:
            # Check for human interruption gate
            if current_node in self.interrupt_before and not current_values.get("is_authorized", False):
                logger.warning(f"INTERRUPT GATE REACHED at node '{current_node}'. Halting execution for human review.")
                self.checkpointer.save_checkpoint(thread_id, next_node=current_node, state_values=current_values)
                yield {"event": "INTERRUPT", "node": current_node, "thread_id": thread_id}
                return

            logger.info(f"[State Machine] Executing node: '{current_node}'")
            if current_node == "planner":
                update = supervisor_planner_node(current_values)
                current_values.update(update)
                current_node = "execute_transaction"
                self.checkpointer.save_checkpoint(thread_id, next_node=current_node, state_values=current_values)
                yield {"event": "STEP_COMPLETE", "node": "planner", "state": current_values}

            elif current_node == "execute_transaction":
                update = execute_transaction_node(current_values)
                current_values.update(update)
                current_node = None  # Graph END
                self.checkpointer.save_checkpoint(thread_id, next_node=None, state_values=current_values)
                yield {"event": "STEP_COMPLETE", "node": "execute_transaction", "state": current_values}


# ============================================================================
# RUNNABLE VERIFICATION HARNESS
# ============================================================================

if __name__ == "__main__":
    checkpointer = InMemoryCheckpointer()
    app = HITLStateMachine(checkpointer=checkpointer, interrupt_before=["execute_transaction"])
    thread_id = "refund-session-tx-99"

    print("\n--- Phase 1: Invocation (Running until interrupt gate) ---")
    initial_input = {
        "query": "Customer requested full refund for breached SLA on account ACC-54321",
        "audit_log": ["Client: Inbound refund request received."],
    }

    events = list(app.stream(thread_id=thread_id, initial_state=initial_input))
    for ev in events:
        print(f"  Event: {ev['event']} (Node: {ev.get('node')})")

    # Inspect paused state snapshot
    snapshot = checkpointer.get_latest(thread_id)
    print("\n--- Phase 2: Inspecting Paused State Snapshot ---")
    print(f"Suspended Thread: {snapshot.thread_id}")
    print(f"Blocked Node: {snapshot.next_node}")
    print(f"Proposed Target Account: {snapshot.values['target_account']}")
    print(f"Proposed Amount: ${snapshot.values['proposed_amount']}")
    print(f"Authorized Flag: {snapshot.values['is_authorized']}")

    # Operator Review: Modify state (adjust amount from $3,200 to $2,800 and authorize)
    print("\n--- Phase 3: Operator Authorizes & Adjusts Amount (State Mutation) ---")
    checkpointer.update_state(
        thread_id=thread_id,
        new_values={
            "is_authorized": True,
            "proposed_amount": 2800.00,  # Adjusted by operator
            "audit_log": snapshot.values["audit_log"] + ["Human Operator: Approved adjusted amount $2,800.00."],
        },
    )

    # Resume graph execution
    print("\n--- Phase 4: Resuming Execution Post-Approval ---")
    resume_events = list(app.stream(thread_id=thread_id))
    for ev in resume_events:
        print(f"  Resumed Event: {ev['event']} (Node: {ev.get('node')})")

    final_snapshot = checkpointer.get_latest(thread_id)
    print("\n--- Final Settled Workflow State ---")
    print(f"Transaction ID: {final_snapshot.values['transaction_id']}")
    print("Full Audit History:")
    for log in final_snapshot.values["audit_log"]:
        print(f"  • {log}")

    assert final_snapshot.values["transaction_id"] is not None
    assert final_snapshot.values["proposed_amount"] == 2800.00
    print("\nSUCCESS: hitl_checkpoint_agent.py verified with checkpointing and state mutation!")
