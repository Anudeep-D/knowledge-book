"""
Module 02: Architectural Design Patterns & Control Loops in Python
Production Artifact: Enterprise Reconciler Control Loop
Demonstrates:
  - Strategy Pattern via typing.Protocol & structural subtyping
  - Dynamic Factory Pattern with registration registry
  - Observer Pattern with async event subscriber dispatch
  - Kubernetes-style Reconciliation Loop (Observed vs. Desired State convergence)
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Coroutine, Protocol, runtime_checkable
import asyncio
import random


class ProvisioningStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    TERMINATING = "TERMINATING"


@dataclass(frozen=True)
class ClusterSpec:
    """The Declarative Target State (Desired State)."""
    cluster_id: str
    target_replicas: int
    region: str
    version: str


@dataclass
class ClusterStatus:
    """The Current Telemetry State (Observed State)."""
    cluster_id: str
    active_replicas: int
    status: ProvisioningStatus
    last_reconciled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class ReconciliationEvent:
    cluster_id: str
    desired_replicas: int
    observed_replicas: int
    delta: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# --- 1. STRATEGY PATTERN (typing.Protocol) ---

@runtime_checkable
class InfrastructureStrategy(Protocol):
    """Behavioral Strategy contract adhering to the Open/Closed Principle."""

    async def get_observed_status(self, cluster_id: str) -> ClusterStatus:
        """Polls current live infrastructure state."""
        ...

    async def scale_replicas(self, cluster_id: str, count: int) -> None:
        """Applies mutation to align active replicas with target."""
        ...


class OpenShiftStrategy:
    """Concrete Strategy for OpenShift MachineSets."""

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        self._current_nodes = 2  # Simulated live state

    async def get_observed_status(self, cluster_id: str) -> ClusterStatus:
        await asyncio.sleep(0.02)
        return ClusterStatus(
            cluster_id=cluster_id,
            active_replicas=self._current_nodes,
            status=ProvisioningStatus.READY,
        )

    async def scale_replicas(self, cluster_id: str, count: int) -> None:
        await asyncio.sleep(0.05)
        self._current_nodes = count
        print(f"[OpenShift API] Patched MachineSet {cluster_id}. Active replicas: {count}")


class AWSKarpenterStrategy:
    """Concrete Strategy for AWS EKS NodePools via Karpenter."""

    def __init__(self, region: str):
        self.region = region
        self._current_nodes = 3

    async def get_observed_status(self, cluster_id: str) -> ClusterStatus:
        await asyncio.sleep(0.02)
        return ClusterStatus(
            cluster_id=cluster_id,
            active_replicas=self._current_nodes,
            status=ProvisioningStatus.READY,
        )

    async def scale_replicas(self, cluster_id: str, count: int) -> None:
        await asyncio.sleep(0.05)
        self._current_nodes = count
        print(f"[AWS Karpenter] Provisioned NodePool for {cluster_id} in {self.region} -> {count} nodes")


# --- 2. FACTORY PATTERN ---

class StrategyFactory:
    """Extensible Factory registry for infrastructure provisioners."""

    _registry: dict[str, Callable[..., InfrastructureStrategy]] = {}

    @classmethod
    def register(cls, provider: str, builder: Callable[..., InfrastructureStrategy]) -> None:
        cls._registry[provider.lower()] = builder

    @classmethod
    def create(cls, provider: str, **kwargs) -> InfrastructureStrategy:
        builder = cls._registry.get(provider.lower())
        if not builder:
            raise ValueError(f"Unknown infrastructure provider: '{provider}'. Registered: {list(cls._registry.keys())}")
        return builder(**kwargs)


# Register initial strategies
StrategyFactory.register("openshift", lambda **kwargs: OpenShiftStrategy(api_endpoint=kwargs.get("api_endpoint", "https://api.ocp.local:6443")))
StrategyFactory.register("aws", lambda **kwargs: AWSKarpenterStrategy(region=kwargs.get("region", "us-east-1")))


# --- 3. OBSERVER PATTERN ---

EventListener = Callable[[ReconciliationEvent], Coroutine[None, None, None]]


class ReconciliationEventDispatcher:
    """Asynchronous Observer event dispatcher for metrics and alerting."""

    def __init__(self):
        self._subscribers: list[EventListener] = []

    def subscribe(self, listener: EventListener) -> None:
        self._subscribers.append(listener)

    async def notify(self, event: ReconciliationEvent) -> None:
        if not self._subscribers:
            return
        await asyncio.gather(*(listener(event) for listener in self._subscribers), return_exceptions=True)


# --- 4. RECONCILIATION CONTROL LOOP ENGINE ---

class CloudNativeReconciliationEngine:
    """
    Kubernetes Controller Pattern:
      1. Observe (Read live cluster status)
      2. Analyze (Diff target spec vs actual status)
      3. Act (Mutate cluster via Strategy)
      4. Emit Telemetry (Notify Observers)
    """

    def __init__(
        self,
        strategy: InfrastructureStrategy,
        dispatcher: ReconciliationEventDispatcher,
    ):
        self._strategy = strategy
        self._dispatcher = dispatcher
        self._running = False

    async def reconcile_step(self, spec: ClusterSpec) -> None:
        """Executes a single idempotent reconciliation pass."""
        observed = await self._strategy.get_observed_status(spec.cluster_id)
        delta = spec.target_replicas - observed.active_replicas

        if delta == 0:
            print(f"[RECONCILER] In Sync: Cluster {spec.cluster_id} active={observed.active_replicas}, target={spec.target_replicas}")
            return

        print(f"[RECONCILER] State Drift Detected: Cluster {spec.cluster_id} observed={observed.active_replicas}, desired={spec.target_replicas} (Delta={delta:+d})")

        # Idempotently converge target
        await self._strategy.scale_replicas(spec.cluster_id, spec.target_replicas)

        # Notify asynchronous telemetry observers
        event = ReconciliationEvent(
            cluster_id=spec.cluster_id,
            desired_replicas=spec.target_replicas,
            observed_replicas=observed.active_replicas,
            delta=delta,
        )
        await self._dispatcher.notify(event)

    async def start(self, spec: ClusterSpec, sync_interval_seconds: float = 2.0, max_iterations: int | None = None) -> None:
        self._running = True
        iterations = 0
        print(f"[RECONCILER] Starting active control loop for cluster '{spec.cluster_id}'...")

        while self._running:
            try:
                await self.reconcile_step(spec)
            except Exception as err:
                # Invariant: Controller never crashes on transient infrastructure failures
                print(f"[RECONCILER ERROR] Failed reconciliation pass: {err}. Backing off...")
                await asyncio.sleep(sync_interval_seconds * 1.5)

            iterations += 1
            if max_iterations is not None and iterations >= max_iterations:
                break

            # Add jittered sleep to prevent thundering herd across parallel controllers
            jitter = random.uniform(0.9, 1.1)
            await asyncio.sleep(sync_interval_seconds * jitter)

    def stop(self) -> None:
        self._running = False
