# Proposal

## Why

Track 1 (`tracks/01-cloud-native-infra`) currently contains an isolated pilot module for KEDA autoscaling, but lacks a complete, cohesive curriculum teaching enterprise distributed systems from first principles. Platform engineers, SREs, and distributed systems architects require a structured, hands-on learning progression spanning stateless microservice design, modern Python architectural patterns and control loops, container lifecycles and OpenShift security boundaries, event-driven scaling, and control plane vs. data plane separation. 

Formalizing this 5-module curriculum ensures Track 1 delivers comprehensive, production-grade mental models, visual topologies, Python 3.12+ reference implementations, and hardened Kubernetes/OpenShift manifests strictly compliant with our Educative.io pedagogical contract.

## What Changes

- Establish the complete 5-module curriculum for Track 1 (`tracks/01-cloud-native-infra`):
  - **Module 01: Modern System Design & Microservices (`01-modern-system-design-microservices`)**: Scalability boundaries, Shared-Nothing architecture, idempotency in Python/FastAPI with Redis, and asynchronous decoupling over Kafka.
  - **Module 02: Architectural Design Patterns & Control Loops in Python (`02-python-architectural-patterns-control-loops`)**: Factory, Strategy (`typing.Protocol`), and Observer patterns alongside cloud-native reconciliation loops (Kubernetes controller pattern).
  - **Module 03: Pods, Clusters, & OpenShift Enterprise Security (`03-pods-clusters-openshift-security`)**: Container cgroups/namespaces, lifecycle hooks, OpenShift Security Context Constraints (`restricted-v2`), dynamic UID allocations, and edge routes.
  - **Module 04: Event-Driven Scaling with KEDA (`04-keda-event-driven-autoscaling`)**: Deepening and renumbering the reference KEDA implementation, detailing external metric scalers (RabbitMQ/Kafka/Prometheus), scale-to-zero, flapping stabilization, and downstream pool protection.
  - **Module 05: Control Plane vs. Data Plane Separation (`05-control-plane-data-plane-separation`)**: Architectural decoupling, Envoy xDS dynamic configuration vs. data forwarding, etcd Raft consensus preservation, and resilient local route cache workers.
- Refactor and renumber existing `01-keda-autoscaling-patterns` to `04-keda-event-driven-autoscaling` to maintain strict sequential progression.
- Update `tracks/01-cloud-native-infra/README.md` to reflect the complete 5-module roadmap and prerequisite chain.
- Validate all newly authored and refactored modules against `shared/scripts/validate-module.py` to guarantee compliance with `module-contract`.

## Capabilities

### New Capabilities
- `cloud-native-curriculum`: Defines the architectural requirements, learning outcomes, required artifacts, and pedagogical progression across the 5 core modules of Track 1 (`tracks/01-cloud-native-infra`).

### Modified Capabilities
None (existing capabilities `curriculum-taxonomy` and `module-contract` remain unchanged and fully enforced).

## Impact

- **Filesystem & Codebase Layout**: Adds four new module directories under `tracks/01-cloud-native-infra/` with co-located `artifacts/` and `diagrams/` folders; renames/refactors `01-keda-autoscaling-patterns` to `04-keda-event-driven-autoscaling`.
- **Manifests & Code**: Introduces production-ready Python implementations (FastAPI idempotency, Strategy/Reconciler engines, local route caches) and hardened Kubernetes/OpenShift manifests (restricted SCC deployments, OpenShift Routes, KEDA ScaledObjects).
- **Validation**: Every module's `index.md` must pass automated structural validation via `validate-module.py`.
