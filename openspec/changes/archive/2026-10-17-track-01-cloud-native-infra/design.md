# Design

## Context

See `proposal.md` for the motivation and high-level curriculum scope, and `specs/cloud-native-curriculum/spec.md` for formal requirement contracts.

The repository currently maintains a single pilot module in `tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/` alongside automated structural validation in `shared/scripts/validate-module.py`. To fulfill the complete curriculum vision, we must build a unified, 5-stage platform engineering trajectory that covers distributed microservices architecture, Python control loops, OpenShift security boundaries, autoscaling mechanics, and control/data plane topology.

## Goals / Non-Goals

**Goals:**
- Implement all 5 curriculum modules in `tracks/01-cloud-native-infra/` adhering strictly to `module-contract` (4 mandatory sections: Interactive Concept Breakdown, Visual Architecture, Real-World Code & Configuration, Edge Cases & Trade-offs).
- Refactor and renumber existing `01-keda-autoscaling-patterns` to `04-keda-event-driven-autoscaling` without dropping existing manifest/diagram assets.
- Provide production-grade, typed Python 3.12+ reference code (FastAPI, Redis, Pydantic v2, `typing.Protocol`, async reconcilers) in co-located `artifacts/` directories.
- Provide hardened Kubernetes and OpenShift manifests (`restricted-v2` SCC, non-root, readOnlyRootFilesystem, OpenShift Routes, KEDA ScaledObjects with anti-flapping).
- Delineate Control Plane vs. Data Plane responsibilities using both plain ASCII diagrams and Mermaid flowcharts across every module.
- Update `tracks/01-cloud-native-infra/README.md` to provide the unified roadmap and prerequisite matrix.

**Non-Goals:**
- Creating live cloud infrastructure provisioning scripts (Terraform/Ansible) or deploying actual OpenShift clusters.
- Replacing or modifying Track 2 (`02-ai-models-inference`), Track 3 (`03-modern-data-layers`), or Track 4 (`04-agentic-workflows`).
- Modifying the core linting logic of `shared/scripts/validate-module.py`.

## Decisions

### 1. Module Sequencing & Naming
- **Decision:** Sequence the 5 modules as:
  1. `01-modern-system-design-microservices`
  2. `02-python-architectural-patterns-control-loops`
  3. `03-pods-clusters-openshift-security`
  4. `04-keda-event-driven-autoscaling` (renumbered from `01-keda-autoscaling-patterns`)
  5. `05-control-plane-data-plane-separation`
- **Rationale:** Builds from application architecture and language patterns up to operating system primitives, cluster orchestrators, dynamic event scaling, and finally cross-system distributed control plane topology.
- **Alternatives Considered:** Keeping `01-keda-...` at index 01 and placing foundational microservice architecture at later indices. Rejected because autoscaling assumes deep prior comprehension of container lifecycle hooks, pods, and statelessness.

### 2. Python Implementation Patterns
- **Decision:** Use modern Python 3.12+ with structural subtyping (`typing.Protocol`), Pydantic v2 data models, and `asyncio` structured concurrency across all code artifacts.
- **Rationale:** Demonstrates how clean, modern Python powers real-world cloud-native platforms, microservice controllers, and ingress layers without heavy external framework bloat.
- **Alternatives Considered:** Classical inheritance (`abc.ABCMeta`) or untyped dictionaries. Rejected as obsolete and unaligned with modern enterprise Python standards.

### 3. OpenShift Manifest Strategy (`restricted-v2` SCC)
- **Decision:** Author OpenShift deployment manifests strictly enforcing `runAsNonRoot: true`, `drop: ["ALL"]`, `readOnlyRootFilesystem: true`, and memory-backed ephemeral storage.
- **Rationale:** Red Hat OpenShift 4.12+ defaults to `restricted-v2` SCC which rejects hardcoded root UIDs (`0`) and unconstrained capabilities. Demonstrating enterprise compliance avoids common "works on Minikube, fails on OpenShift" pitfalls.
- **Alternatives Considered:** Targeting vanilla Kubernetes `PodSecurityStandards` only. Rejected because OpenShift represents a major enterprise platform standard with unique SCC and Route abstractions.

### 4. Diagram Standard
- **Decision:** Include both plain ASCII diagrams (using only `+`, `-`, `|`, `-->`, `<--`, `^`, `v`) and Mermaid diagrams in every module.
- **Rationale:** Plain ASCII diagrams render identically across all terminals, IDE previewers, and command-line viewers without font or Unicode alignment drift, while Mermaid diagrams provide interactive rendering in modern web viewers.

## Risks / Trade-offs

- **[Risk: Renumbering `01-keda-autoscaling-patterns` breaks existing links]** → Mitigated by updating all references in `tracks/01-cloud-native-infra/README.md`, top-level `README.md`, and preserving all companion manifests and diagrams under `04-keda-event-driven-autoscaling/`.
- **[Risk: Volume of content across 5 modules causing superficial coverage]** → Mitigated by following the strict 4-part `module-contract` template for each module, complete with production-grade artifacts and failure matrices.
- **[Risk: Linter failures on section numbering]** → Mitigated by running `python3 shared/scripts/validate-module.py` on every module `index.md` before finalizing tasks.

## Migration Plan

1. Create module directories and author modules 01, 02, 03, and 05.
2. Relocate `tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/` to `tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/`.
3. Update metadata frontmatter (`id: 04-cni-keda-autoscaling`) and internal artifact links in `04-keda-event-driven-autoscaling/index.md`.
4. Update `tracks/01-cloud-native-infra/README.md` curriculum roadmap and module inventory table.
5. Execute `validate-module.py` across all 5 modules to guarantee zero syntax or schema regressions.
