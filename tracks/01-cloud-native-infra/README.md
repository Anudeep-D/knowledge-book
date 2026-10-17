# Track 01: Cloud-Native Infrastructure & Platform Engineering

## Overview

Welcome to **Track 01: Cloud-Native Infrastructure & Platform Engineering**. This track is designed for senior and staff software engineers, site reliability engineers (SREs), and platform architects building, operating, and scaling mission-critical distributed systems on Kubernetes and hybrid cloud foundations.

Modeled after interactive engineering curricula, each module delivers first-principles mental models, visual control plane / data plane topologies, production-grade manifests, and battle-tested failure mode analysis.

---

## Pedagogical Philosophy

1. **The Why Before The How:** We dissect real-world production outages (etcd quorum loss, split-brain, metric lag storms, OOMKills) before writing a single configuration line.
2. **Control Plane vs. Data Plane Split:** Every architectural pattern cleanly delineates ingress, routing, reconcile loops, and execution workloads using Mermaid and ASCII diagrams.
3. **No Toy Examples:** All manifests include production requirements: strict resource quotas, CPU/memory limits, ephemeral storage allocations, graceful shutdown hooks, and non-root security contexts.
4. **Edge Cases & Failure Matrices:** We don't just explain when a tool shines; we document precisely when and how it collapses under load.

---

## Curriculum Roadmap

```
+---------------------------------------------------------------------------------------------------+
|                        CLOUD-NATIVE CURRICULUM ROADMAP (TRACK 01)                                 |
+---------------------------------------------------------------------------------------------------+
|  01. Modern System Design & Microservices                                                         |
|      (Scalability Boundaries, Shared-Nothing, Idempotency, Asynchronous Event Ingress)            |
|                                                                                                   |
|  02. Architectural Design Patterns & Control Loops in Python                                      |
|      (Strategy Protocol, Factory, Observer, Level-Triggered Reconciliation Loops)                 |
|                                                                                                   |
|  03. Pods, Clusters, & OpenShift Enterprise Security                                              |
|      (cgroups v2, Linux Namespaces, restricted-v2 SCC, PreStop Hooks, Ingress Route Sharding)     |
|                                                                                                   |
|  04. Event-Driven Scaling with KEDA                                                               |
|      (CRDs, External Metrics Adapter, Scale-to-Zero, Anti-Flapping Stabilization)                 |
|                                                                                                   |
|  05. Control Plane vs. Data Plane Separation                                                      |
|      (Decoupling Invariants, Envoy xDS Route Streaming, etcd Quorum Protection, Local Cache)      |
+---------------------------------------------------------------------------------------------------+
```

---

## Active Curriculum Modules

| Module Slug | Status | Focus Areas | Key Production Artifacts | Primary Failure Mode Analyzed |
| :--- | :--- | :--- | :--- | :--- |
| [`01-modern-system-design-microservices`](./01-modern-system-design-microservices/) | **Active** | Stateless ingress, idempotency locks, async event logs | `idempotent_ingress.py` (FastAPI + Redis) | Session stampede & database lock saturation |
| [`02-python-architectural-patterns-control-loops`](./02-python-architectural-patterns-control-loops/) | **Active** | Strategy pattern, reconcilers, self-healing control loops | `reconciler_control_loop.py` (Protocol + AsyncIO) | State bouncing & thundering herd API throttling |
| [`03-pods-clusters-openshift-security`](./03-pods-clusters-openshift-security/) | **Active** | Container lifecycles, OpenShift `restricted-v2` SCC | `openshift-deployment.yaml`, `openshift-route.yaml` | Connection drops on termination & UID violations |
| [`04-keda-event-driven-autoscaling`](./04-keda-event-driven-autoscaling/) | **Active** | Custom metrics, scale-to-zero, HPA integration | `ScaledObject`, `TriggerAuthentication`, Deployment | Downstream DB connection pool starvation |
| [`05-control-plane-data-plane-separation`](./05-control-plane-data-plane-separation/) | **Active** | CP/DP decoupling, Envoy xDS, local cache workers | `local_route_cache.py` (Fail-Open Router) | etcd Raft quorum collapse & data plane blackouts |

---

## Prerequisites & Tooling

- Working familiarity with containerization (Docker, OCI runtime specifications, cgroups, namespaces).
- Intermediate Kubernetes & OpenShift knowledge (`kubectl`, `oc`, Deployments, Services, Routes, SCCs).
- Modern Python 3.12+ literacy (type hints, `typing.Protocol`, Pydantic v2, `asyncio`).
- Basic distributed systems networking (TCP/IP, HTTP/2, gRPC, TLS termination handshakes).
- Installed tools for labs: `kubectl`, `oc`, `helm`, `k9s`, `redis-cli`, Python 3.12+.
