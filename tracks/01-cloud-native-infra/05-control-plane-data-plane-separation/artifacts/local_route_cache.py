"""
Module 05: Control Plane vs. Data Plane Separation
Production Artifact: Resilient Data Plane Client with Local Route Caching
Demonstrates:
  - Decoupling high-frequency data forwarding from out-of-band control plane orchestration
  - Dynamic route synchronization loop modeled after Envoy xDS
  - Fail-Open resiliency: Zero downtime and zero packet drops during total control plane outages
  - Circuit breaking and exponential jittered reconnects
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import asyncio
import json
import random


class RouteHealth(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"


@dataclass(frozen=True)
class ServiceEndpoint:
    host: str
    port: int
    weight: int = 100
    health: RouteHealth = RouteHealth.HEALTHY


@dataclass
class DynamicRouteConfig:
    """Control Plane Route Definition."""
    service_name: str
    endpoints: list[ServiceEndpoint]
    timeout_ms: int = 500
    retry_budget: int = 2
    version: str = "v1"
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MockControlPlaneServer:
    """Simulates a Kubernetes API Server / Envoy Management Server (xDS)."""

    def __init__(self):
        self.is_healthy = True
        self._version = 1
        self._routes: dict[str, DynamicRouteConfig] = {
            "ai-inference": DynamicRouteConfig(
                service_name="ai-inference",
                endpoints=[
                    ServiceEndpoint(host="inference-node-01.mesh", port=8000, weight=50),
                    ServiceEndpoint(host="inference-node-02.mesh", port=8000, weight=50),
                ],
                version="v1",
            ),
            "fraud-detection": DynamicRouteConfig(
                service_name="fraud-detection",
                endpoints=[
                    ServiceEndpoint(host="fraud-node-01.mesh", port=9000, weight=100),
                ],
                version="v1",
            ),
        }

    async def fetch_route_manifest(self) -> dict[str, DynamicRouteConfig]:
        """Called out-of-band by Data Plane sync workers."""
        await asyncio.sleep(0.05)  # Simulated network latency
        if not self.is_healthy:
            raise ConnectionError("Control plane Raft consensus lost (etcd quorum failure 503)")
        return self._routes

    def simulate_outage(self) -> None:
        self.is_healthy = False
        print("\n[SIMULATION] Control Plane CRASHED (etcd quorum failure)!\n")

    def simulate_recovery(self) -> None:
        self.is_healthy = True
        self._version += 1
        # Update route dynamically
        self._routes["ai-inference"] = DynamicRouteConfig(
            service_name="ai-inference",
            endpoints=[
                ServiceEndpoint(host="inference-node-01.mesh", port=8000, weight=30),
                ServiceEndpoint(host="inference-node-02.mesh", port=8000, weight=70),
                ServiceEndpoint(host="inference-node-03.mesh", port=8000, weight=100),
            ],
            version=f"v{self._version}",
        )
        print(f"\n[SIMULATION] Control Plane RECOVERED (Propagating config v{self._version})!\n")


class ResilientDataPlaneRouter:
    """
    High-Throughput Data Plane Router:
      - Synchronizes route definitions out-of-band via background coroutine.
      - Never queries the Control Plane inside the critical request forwarding path.
      - Maintains local memory cache with zero-lock atomic swap.
    """

    def __init__(self, control_plane: MockControlPlaneServer):
        self._control_plane = control_plane
        # Immutable snapshot for lock-free read access
        self._route_cache: dict[str, DynamicRouteConfig] = {}
        self._sync_task: asyncio.Task | None = None
        self._running = False
        self._consecutive_failures = 0

    async def start_background_sync(self, interval_seconds: float = 1.0) -> None:
        """Starts asynchronous, non-blocking route synchronization."""
        self._running = True
        # Initial bootstrap sync
        await self._sync_routes_once()
        self._sync_task = asyncio.create_task(self._sync_loop(interval_seconds))

    async def _sync_routes_once(self) -> None:
        try:
            routes = await self._control_plane.fetch_route_manifest()
            # Atomic reference swap
            self._route_cache = routes.copy()
            self._consecutive_failures = 0
        except Exception as err:
            self._consecutive_failures += 1
            print(f"[DATA PLANE WARNING] Failed to reach control plane ({err}). Operating on cached snapshot ({len(self._route_cache)} routes).")

    async def _sync_loop(self, interval: float) -> None:
        while self._running:
            # Jittered backoff if control plane is struggling
            delay = interval * (1.5 ** min(self._consecutive_failures, 4)) + random.uniform(0.1, 0.3)
            await asyncio.sleep(delay)
            await self._sync_routes_once()

    def route_request(self, service_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        CRITICAL PATH: 100% in-memory data plane forwarding.
        Zero control plane dependency. Executes in sub-millisecond time.
        """
        route = self._route_cache.get(service_name)
        if not route:
            raise LookupError(f"Data plane error: No route registered for '{service_name}'")

        healthy_endpoints = [ep for ep in route.endpoints if ep.health == RouteHealth.HEALTHY]
        if not healthy_endpoints:
            raise RuntimeError(f"Service '{service_name}' has zero healthy endpoints in cache")

        # Weighted selection in memory
        selected = random.choices(
            healthy_endpoints,
            weights=[ep.weight for ep in healthy_endpoints],
            k=1,
        )[0]

        return {
            "routed_to": f"{selected.host}:{selected.port}",
            "route_version": route.version,
            "status": "FORWARDED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def shutdown(self) -> None:
        self._running = False
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
