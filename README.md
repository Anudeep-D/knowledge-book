# Enterprise Engineering Knowledge Book

An interactive, production-grade engineering knowledge base and curriculum modeled after interactive platforms like Educative.io. Built with first-principles mental models, visual control plane / data plane topologies, real-world Python and Kubernetes/OpenShift artifacts, and failure mode blast radius analysis.

---

## Curriculum Taxonomy

The knowledge book is structured across four foundational tracks:

```
+---------------------------------------------------------------------------------------------------+
|                              ENTERPRISE KNOWLEDGE BOOK TAXONOMY                                   |
+---------------------------------------------------------------------------------------------------+
|  Track 01: Cloud-Native Infrastructure & Platform Engineering                                     |
|  Track 02: AI Models, Serving, & Distributed Inference                                           |
|  Track 03: Modern Data Layers & Streaming Architectures                                           |
|  Track 04: Agentic Workflows & Multi-Agent Orchestration                                          |
+---------------------------------------------------------------------------------------------------+
```

---

## Track 01: Cloud-Native Infrastructure & Platform Engineering

Located in [`tracks/01-cloud-native-infra/`](./tracks/01-cloud-native-infra/):

1. **[`01-modern-system-design-microservices`](./tracks/01-cloud-native-infra/01-modern-system-design-microservices/)**: Scalability boundaries, Shared-Nothing architecture, idempotency in Python/FastAPI with Redis, and asynchronous decoupling over Kafka.
2. **[`02-python-architectural-patterns-control-loops`](./tracks/01-cloud-native-infra/02-python-architectural-patterns-control-loops/)**: Factory, Strategy (`typing.Protocol`), and Observer patterns alongside Kubernetes-style reconciliation loops.
3. **[`03-pods-clusters-openshift-security`](./tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/)**: Container cgroups v2/namespaces, lifecycle hooks, OpenShift Security Context Constraints (`restricted-v2`), dynamic UID allocations, and edge routes.
4. **[`04-keda-event-driven-autoscaling`](./tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/)**: Event-driven horizontal autoscaling, external metric scalers, scale-to-zero, flapping stabilization, and downstream pool protection.
5. **[`05-control-plane-data-plane-separation`](./tracks/01-cloud-native-infra/05-control-plane-data-plane-separation/)**: Architectural decoupling, Envoy xDS dynamic route distribution, etcd Raft consensus preservation, and resilient local route cache workers.

---

## Pedagogical Standard & Contract

Every module implements our mandatory 4-part structure:
1. **Interactive Concept Breakdown:** The production crucible ("why before how"), first-principles mental models, and non-negotiable invariants.
2. **Visual Architecture:** Terminal-safe plain ASCII diagrams and interactive Mermaid flowcharts with explicit Control Plane vs. Data Plane splits.
3. **Real-World Code & Configuration:** Production-grade Python 3.12+ reference code and hardened Kubernetes/OpenShift YAML manifests.
4. **Edge Cases, Failure Modes & Trade-offs:** Comparative architectural decision matrices, failure blast radius analysis, and emergency SRE triage runbooks.

Modules are automatically linted and validated via:
```bash
python3 shared/scripts/validate-module.py --all
```
