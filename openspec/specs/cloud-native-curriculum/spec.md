# cloud-native-curriculum Specification

## Purpose

Defines the architectural requirements, pedagogical milestones, module taxonomy, and companion artifacts for the 5-module curriculum in Track 1 (Cloud-Native Infrastructure & Platform Engineering).

## Requirements

### Requirement: Track 1 Five-Module Curriculum Structure
The curriculum SHALL organize Track 1 (`tracks/01-cloud-native-infra/`) into five sequentially ordered modules: `01-modern-system-design-microservices`, `02-python-architectural-patterns-control-loops`, `03-pods-clusters-openshift-security`, `04-keda-event-driven-autoscaling`, and `05-control-plane-data-plane-separation`.

#### Scenario: Sequential module layout verification
- **WHEN** the Track 1 directory structure is inspected
- **THEN** all five module directories exist with zero-padded prefixes from 01 to 05, each containing an `index.md` and companion asset subdirectories.

### Requirement: Microservices and Stateless Ingress Coverage
Module 01 SHALL provide conceptual mental models, visual request topologies, and production Python code demonstrating Shared-Nothing architecture, idempotency validation, and asynchronous event decoupling.

#### Scenario: Module 01 content validation
- **WHEN** Module 01 (`01-modern-system-design-microservices/index.md`) is reviewed
- **THEN** it contains first-principles scalability law analysis, an idempotency implementation with Redis and FastAPI, and asynchronous event publishing.

### Requirement: Python Architectural Patterns and Reconciler Loop
Module 02 SHALL demonstrate enterprise Python 3.12+ patterns (Factory, Strategy with `typing.Protocol`, Observer) and implement an idempotent reconciliation control loop modeled on Kubernetes controllers.

#### Scenario: Module 02 pattern and reconciler verification
- **WHEN** Module 02 artifacts are examined
- **THEN** runnable Python code implements structural subtyping via `typing.Protocol` and an active state reconciliation control loop detecting and remediating state drift.

### Requirement: Container Lifecycles and OpenShift Security Constraints
Module 03 SHALL teach container primitives (cgroups v2, Linux namespaces, pod termination lifecycle hooks) and provide production OpenShift manifests compliant with `restricted-v2` SecurityContextConstraints.

#### Scenario: OpenShift enterprise manifest verification
- **WHEN** Module 03 deployment manifests are audited
- **THEN** they specify non-root execution, dropped Linux capabilities, read-only root filesystems, resource boundaries, and OpenShift Route ingress definitions.

### Requirement: Event-Driven Autoscaling with KEDA
Module 04 SHALL refactor and renumber the reference KEDA implementation into position 04, detailing external queue metric scalers, HPA metric adapter mechanics, scale-to-zero activation, and downstream database connection protections.

#### Scenario: KEDA autoscaling progression
- **WHEN** Module 04 is validated
- **THEN** it resides in `tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling` and contains `ScaledObject` definitions with anti-flapping stabilization policies.

### Requirement: Control Plane and Data Plane Decoupling
Module 05 SHALL articulate the architectural boundaries between control plane orchestration and high-throughput data plane execution, including dynamic route distribution, etcd quorum protection, and resilient local cache workers.

#### Scenario: Control plane decoupling verification
- **WHEN** Module 05 is evaluated
- **THEN** it contains ASCII and Mermaid control/data plane split topologies and Python client implementations with out-of-band route updates and offline fallbacks.

### Requirement: Track Roadmap and Prerequisite Alignment
The Track 1 overview (`tracks/01-cloud-native-infra/README.md`) SHALL document the full 5-module curriculum roadmap, pedagogical philosophy, module status table, and technical prerequisites.

#### Scenario: Track README roadmap completeness
- **WHEN** `tracks/01-cloud-native-infra/README.md` is loaded
- **THEN** it lists all 5 modules with accurate slugs, difficulty ratings, key artifacts, and failure modes.
