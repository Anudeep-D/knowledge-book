# Tasks

## 1. Module 01: Modern System Design & Microservices

- [x] 1.1 Scaffold directory `tracks/01-cloud-native-infra/01-modern-system-design-microservices/` with `artifacts/` and `diagrams/` subdirectories and verify directory structure.
- [x] 1.2 Author Python artifact `artifacts/idempotent_ingress.py` implementing FastAPI stateless ingress, Redis idempotency locking, and asynchronous event publishing; verify syntax via `python3 -m py_compile`.
- [x] 1.3 Author `01-modern-system-design-microservices/index.md` fulfilling all 4 mandatory Educative.io sections (Incident Crucible, Amdahl/USL mental models, Control/Data plane ASCII & Mermaid diagrams, annotations, and failure modes).
- [x] 1.4 Validate Module 01 compliance by executing `python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/01-modern-system-design-microservices/index.md`.

## 2. Module 02: Architectural Design Patterns & Control Loops in Python

- [x] 2.1 Scaffold directory `tracks/01-cloud-native-infra/02-python-architectural-patterns-control-loops/` with `artifacts/` and `diagrams/` subdirectories and verify directory structure.
- [x] 2.2 Author Python artifact `artifacts/reconciler_control_loop.py` implementing Strategy via `typing.Protocol`, Factory, Observer, and a Kubernetes-style Reconciliation Engine; verify syntax via `python3 -m py_compile`.
- [x] 2.3 Author `02-python-architectural-patterns-control-loops/index.md` fulfilling all 4 mandatory Educative.io sections (Outage Crucible, Reconciliation mental model, ASCII & Mermaid control loop flows, annotations, and state drift failure modes).
- [x] 2.4 Validate Module 02 compliance by executing `python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/02-python-architectural-patterns-control-loops/index.md`.

## 3. Module 03: Pods, Clusters, & OpenShift Enterprise Security

- [x] 3.1 Scaffold directory `tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/` with `artifacts/` and `diagrams/` subdirectories and verify directory structure.
- [x] 3.2 Author production manifests `artifacts/openshift-deployment.yaml` (`restricted-v2` SCC compliance, non-root, read-only rootfs, probes, preStop lifecycle hook) and `artifacts/openshift-route.yaml` (TLS edge termination); verify YAML syntax.
- [x] 3.3 Author `03-pods-clusters-openshift-security/index.md` fulfilling all 4 mandatory Educative.io sections (Admission rejection crucible, cgroups v2/namespaces mental models, OpenShift SCC evaluation ASCII & Mermaid diagrams, annotations, and failure modes).
- [x] 3.4 Validate Module 03 compliance by executing `python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/03-pods-clusters-openshift-security/index.md`.

## 4. Module 04: Refactor Event-Driven Scaling with KEDA

- [x] 4.1 Relocate `tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/` to `tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/` and verify all manifests, diagrams, and files are preserved.
- [x] 4.2 Update frontmatter metadata `id: "04-cni-keda-autoscaling"` and internal links in `tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/index.md`.
- [x] 4.3 Validate Module 04 compliance by executing `python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/04-keda-event-driven-autoscaling/index.md`.

## 5. Module 05: Control Plane vs. Data Plane Separation

- [x] 5.1 Scaffold directory `tracks/01-cloud-native-infra/05-control-plane-data-plane-separation/` with `artifacts/` and `diagrams/` subdirectories and verify directory structure.
- [x] 5.2 Author Python artifact `artifacts/local_route_cache.py` implementing a resilient Data Plane client with out-of-band control plane synchronization and offline route cache fallbacks; verify syntax via `python3 -m py_compile`.
- [x] 5.3 Author `05-control-plane-data-plane-separation/index.md` fulfilling all 4 mandatory Educative.io sections (etcd quorum outage crucible, decoupling invariants, Envoy xDS ASCII & Mermaid diagrams, annotations, and quorum failure blast radius).
- [x] 5.4 Validate Module 05 compliance by executing `python3 shared/scripts/validate-module.py tracks/01-cloud-native-infra/05-control-plane-data-plane-separation/index.md`.

## 6. Track Integration & Final Validation

- [x] 6.1 Update `tracks/01-cloud-native-infra/README.md` to reflect the complete 5-module curriculum roadmap, module inventory table, and prerequisites.
- [x] 6.2 Update references across top-level `README.md` to maintain consistent cross-module links.
- [x] 6.3 Execute `shared/scripts/validate-module.py` across all modules in Track 1 to verify zero regressions.
