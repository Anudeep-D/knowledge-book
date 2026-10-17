---
id: "03-cni-pods-clusters-openshift-security"
title: "Pods, Clusters, & OpenShift Enterprise Security"
track: "01-cloud-native-infra"
difficulty: "L300 (Intermediate)"
estimated_minutes: 45
prerequisites:
  - "Core Kubernetes Primitives (Pods, Deployments, Services)"
  - "Linux Fundamentals (UIDs, file permissions, signals)"
  - "Basic Networking (TCP/IP, Ingress, TLS termination)"
tags:
  - "kubernetes"
  - "openshift"
  - "security"
  - "scc"
  - "cgroups"
  - "linux-namespaces"
  - "containers"
last_updated: "2026-10-17"
---

# Pods, Clusters, & OpenShift Enterprise Security

> **Executive Summary:** Running containers in enterprise clusters requires abandoning the permissive assumptions of local development. Unlike vanilla Kubernetes, Red Hat OpenShift enforces strict Security Context Constraints (`restricted-v2` SCC) that reject hardcoded root users (`UID 0`), unprivileged ports ($<1024$), and writable root filesystems. By mastering Linux kernel isolation primitives (cgroups v2, namespaces) and pairing them with deterministic pod termination lifecycles and OpenShift Route sharding, platform engineers build tamper-proof, zero-downtime distributed workloads.

---

# 1. Interactive Concept Breakdown

## 1.1 The Production Crucible (The Why Before The How)

A software engineering team built a microservice for account verification. Locally on Docker Desktop and on a development Minikube cluster, the application deployed seamlessly. 

However, upon deploying the exact same Helm release to the company's multi-tenant Red Hat OpenShift production cluster, all worker pods instantly crashed with `CreateContainerConfigError` and remained locked in `CrashLoopBackOff`.

```
OPENSHIFT ADMISSION AUDIT LOG (PRODUCTION REJECTION)
Status: 403 Forbidden
Resource: pods "account-verify-7c94b79b9b-4k2x9"
Reason: "PodSecurityPolicy / SCC admission controller denied request"
Violations:
  - container "api": runAsUser=0 violates SCC 'restricted-v2' (MustRunAsRange)
  - container "api": privileged port 80 violates SCC 'restricted-v2' (net_bind_service capability required)
  - container "api": allowPrivilegeEscalation must be false
```

### The Root-Cause Chain
1. **Hardcoded Root Assumption:** The developer’s base image (`FROM python:3.12-slim`) defaulted to `USER root` (UID 0).
2. **Privileged Port Binding:** The application web server attempted to bind to privileged TCP port `80` ($<1024$), requiring the Linux capability `CAP_NET_BIND_SERVICE`.
3. **OpenShift Admission Gatekeeper:** OpenShift's default `restricted-v2` Security Context Constraint (SCC) automatically inspected the Pod admission request. Because the Pod did not specify `runAsNonRoot: true` and attempted to execute with root capabilities, the admission webhook rejected pod creation at the API server boundary before a single container process was scheduled.

In an enterprise cloud-native environment, **containers are never given root privileges**. Workloads must run as randomized, non-root high UIDs assigned dynamically by the platform.

---

## 1.2 First-Principles Mental Model: What is a Container?

A container is not a lightweight virtual machine. A container is simply a **standard Linux host process** wrapped in kernel isolation boundaries:

```
+-------------------------------------------------------------------------------+
|                       LINUX KERNEL ISOLATION BOUNDARIES                       |
+-------------------------------------------------------------------------------+
|                                                                               |
|   1. CONTROL GROUPS (cgroups v2)       2. KERNEL NAMESPACES                   |
|   (Resource Throttling)                (Visibility Walls)                     |
|                                                                               |
|   - cpu.max: Hard CPU quota (CFS)      - mnt: Isolated filesystem view        |
|   - memory.max: OOMKill trigger        - pid: Process tree (app sees PID 1)   |
|   - memory.high: Throttling floor      - net: Dedicated IP, ports, routing    |
|   - io.weight: Disk I/O prioritization - ipc: Inter-process memory isolation  |
|                                        - user: UID/GID virtualization         |
|                                                                               |
+-------------------------------------------------------------------------------+
```

### OpenShift Security Context Constraints (SCC) vs. Vanilla Kubernetes PSS
In vanilla Kubernetes, Pod Security Standards (Privileged, Baseline, Restricted) are configured via namespace labels. 

OpenShift enforces **Security Context Constraints (SCCs)** through a dedicated admission controller. When a project namespace is created in OpenShift, the control plane allocates a unique, non-overlapping UID range annotation:

```yaml
openshift.io/sa.scc.uid-range: 1000670000/10000
openshift.io/sa.scc.supplemental-groups: 1000670000/10000
```

Any container running in this namespace must run with a UID in the range `1000670000` to `1000679999`. Hardcoding `USER 1001` or `USER 0` in your Dockerfile violates this range and results in instant admission failure.

---

## 1.3 Pod Termination Lifecycle Invariants

To achieve true zero-downtime rolling deployments, services must coordinate with the Kubernetes ingress routing layer. The termination sequence follows a deterministic 5-stage pipeline:

```
[Kube-API: Delete Pod]
       |
       +---> 1. Pod marked Terminating; Kube-Proxy / Ingress Router begins removing Pod IP
       |
       +---> 2. Kubelet executes preStop hook: ["/bin/sh", "-c", "sleep 15"]
       |        (Crucial: Router needs ~5-10s to update HAProxy/Envoy route tables!)
       |
       +---> 3. Kubelet sends SIGTERM (PID 1) -> Application finishes in-flight requests
       |
       +---> 4. Kubelet waits up to terminationGracePeriodSeconds (e.g. 45s)
       |
       +---> 5. If process still alive after deadline -> Kubelet sends SIGKILL (Hard Termination)
```

---

# 2. Visual Architecture

## 2.1 OpenShift SCC Admission & Security Evaluation Topology

```
+-----------------------------------------------------------------------------------------------+
|                      OPENSHIFT ENTERPRISE SCC ADMISSION PIPELINE                              |
+-----------------------------------------------------------------------------------------------+
|                                                                                               |
|   Developer Manifest (Deployment / Pod)                                                       |
|   spec.template.spec.securityContext: runAsNonRoot: true                                      |
|               |                                                                               |
|               v                                                                               |
|   +---------------------------------------------------------------------------------------+   |
|   | OpenShift API Server Admission Chain                                                  |   |
|   | 1. Mutating Webhooks                                                                  |   |
|   | 2. SCC Admission Controller                                                           |   |
|   |    - Evaluates ServiceAccount against available SCCs                                  |   |
|   |    - Selects 'restricted-v2' (Least Privilege)                                       |   |
|   +---------------------------------------------------------------------------------------+   |
|               |                                                   |                           |
|        [Passes Criteria]                                   [Fails Criteria]                   |
|               |                                                   |                           |
|               v                                                   v                           |
|   +---------------------------------------+       +---------------------------------------+   |
|   | Inject Dynamic Assigned UID           |       | 403 Forbidden                         |   |
|   | e.g., UID = 1000670014                |       | "violates SCC restricted-v2"          |   |
|   +---------------------------------------+       +---------------------------------------+   |
|               |                                                                               |
|               v                                                                               |
|   +---------------------------------------------------------------------------------------+   |
|   | Node Kubelet / CRI-O Container Engine                                                 |   |
|   | - Linux User Namespace: UID 1000670014                                                |   |
|   | - Linux Capabilities: Drop ALL (no CAP_NET_RAW, no CAP_SYS_ADMIN)                     |   |
|   | - Mounts: Root filesystem mounted READ-ONLY (ro)                                      |   |
|   | - Seccomp: RuntimeDefault filter active                                               |   |
|   +---------------------------------------------------------------------------------------+   |
|                                                                                               |
+-----------------------------------------------------------------------------------------------+
```

## 2.2 Pod Termination & Ingress Route Deregistration Flow

```mermaid
sequenceDiagram
    autonumber
    participant Client as External Traffic
    participant Router as OpenShift Ingress (HAProxy)
    participant K8s as OpenShift Control Plane
    participant Kubelet as Worker Node Kubelet
    participant Pod as Banking API Pod (PID 1)

    Client->>Router: HTTPS Ingress Traffic
    Router->>Pod: Proxy request to Pod IP:8443
    Note over K8s: Rolling Update Triggered
    K8s->>Router: Asynchronously remove Pod IP from Endpoints
    K8s->>Kubelet: Initiate Pod Termination
    Kubelet->>Pod: Execute preStop hook (sleep 15s)
    Note over Pod: Pod continues servicing active connections!
    Note over Router: Router drains existing connections & flushes table
    Kubelet->>Pod: Send SIGTERM to PID 1
    Pod->>Pod: Stop accepting new TCP connections; drain in-flight jobs
    Pod-->>Kubelet: Process exits with code 0
    Kubelet-->>K8s: Container stopped cleanly
    Note over Client,Router: Zero dropped connections observed!
```

---

# 3. Real-World Code & Configuration

Companion manifests for this module are co-located in [`artifacts/openshift-deployment.yaml`](./artifacts/openshift-deployment.yaml) and [`artifacts/openshift-route.yaml`](./artifacts/openshift-route.yaml).

## 3.1 Hardened OpenShift Deployment (`artifacts/openshift-deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-banking-api
  namespace: prod-banking-core
  labels:
    app.kubernetes.io/name: secure-banking-api
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: secure-banking-api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: secure-banking-api
    spec:
      serviceAccountName: secure-banking-sa
      terminationGracePeriodSeconds: 45
      # OpenShift Pod-Level Security Context
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          image: image-registry.openshift-image-registry.svc:5000/prod-banking-core/secure-banking-api:v2.1.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8443
              name: https
              protocol: TCP
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
              ephemeral-storage: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
              ephemeral-storage: "1Gi"
          # Container-Level Hardening satisfying restricted-v2 SCC
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          livenessProbe:
            httpGet:
              path: /healthz/liveness
              port: 8443
              scheme: HTTPS
            initialDelaySeconds: 15
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /healthz/readiness
              port: 8443
              scheme: HTTPS
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 2
            failureThreshold: 2
          lifecycle:
            preStop:
              exec:
                # Invariant: Allow Ingress router to unregister endpoint before SIGTERM
                command: ["/bin/sh", "-c", "sleep 15"]
          volumeMounts:
            - name: ephemeral-scratch
              mountPath: /tmp
            - name: tls-certs
              mountPath: /etc/tls/certs
              readOnly: true
      volumes:
        - name: ephemeral-scratch
          emptyDir:
            medium: Memory
            sizeLimit: 128Mi
        - name: tls-certs
          secret:
            secretName: banking-api-tls
            defaultMode: 0400
```

## 3.2 OpenShift Edge Route with TLS Termination (`artifacts/openshift-route.yaml`)

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: secure-banking-route
  namespace: prod-banking-core
  labels:
    app.kubernetes.io/name: secure-banking-api
    router.openshift.io/shard: external-dmz
  annotations:
    haproxy.router.openshift.io/timeout: 30s
    haproxy.router.openshift.io/balance: roundrobin
spec:
  host: api.banking.enterprise.internal
  to:
    kind: Service
    name: secure-banking-api
    weight: 100
  port:
    targetPort: https
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

## 3.3 Line-by-Line "Under the Hood" Annotations

- **`openshift-deployment.yaml` Lines 25–29 (`runAsNonRoot: true` & `seccompProfile`):** Guarantees the container engine refuses to launch the container if the image tries to execute as UID 0. Enables the Linux kernel default syscall restriction profile.
- **`openshift-deployment.yaml` Lines 45–50 (`allowPrivilegeEscalation: false` & `drop: ["ALL"]`):** Sets the Linux process bit `no_new_privs`, preventing setuid binaries (like `sudo` or `ping`) from gaining elevated privileges. Drops all kernel capabilities.
- **`openshift-deployment.yaml` Line 46 (`readOnlyRootFilesystem: true`):** Protects against rootkits and remote code execution (RCE) exploitation. Attackers cannot modify `/bin`, `/usr`, or write executable scripts to disk.
- **`openshift-deployment.yaml` Lines 72–75 (`preStop: sleep 15`):** Solves the Kubernetes termination race condition. Ensures the pod continues running its HTTP server for 15 seconds while OpenShift's HAProxy routers drain existing keep-alive TCP connections.
- **`openshift-deployment.yaml` Lines 85–89 (`emptyDir: medium: Memory`):** Because the root filesystem is read-only, applications needing temporary scratch space (e.g., Python temp files or pid locks) are provided a RAM-backed, quota-constrained `/tmp` directory.

---

# 4. Edge Cases, Failure Modes & Trade-offs

## 4.1 Comparative Architectural Decision Matrix: OpenShift SCC Profiles

| Security Context Constraint (SCC) | UID Allocation Mode | Allowed Capabilities | Host Access Allowed | Target Workload Profile |
| :--- | :--- | :--- | :--- | :--- |
| **`restricted-v2` (Default)** | MustRunAsRange (Allocated high UID) | Drops ALL | None (Strictly Isolated) | 99% of business microservices and web APIs |
| **`nonroot-v2`** | MustRunAsNonRoot (User defines >0) | Drops ALL | None | Third-party OCI images requiring fixed UIDs (e.g., UID 1001) |
| **`anyuid`** | RunAsAny (Allows UID 0) | Standard default capabilities | None | Legacy container images that cannot run without root |
| **`privileged`** | RunAsAny | ALL Capabilities | Full Host Access (PID, Net, IPC) | CNI plugins (Cilium), storage drivers, OpenShift node daemons |

---

## 4.2 Failure Mode & Blast Radius Analysis

### Failure Scenario 1: Dropped Client TCP Connections During Rolling Updates
- **The Trigger:** A new deployment is applied. Kubernetes sends `SIGTERM` immediately without a `preStop` hook. The container terminates active sockets.
- **The Blast Radius:** OpenShift Ingress (HAProxy) takes 3 to 6 seconds to propagate endpoint removal across router pods. During this window, incoming client HTTPS requests are routed to the terminated container, resulting in `502 Bad Gateway` errors for active customers.
- **Mitigation & Guardrail:** Always inject `lifecycle.preStop.exec.command: ["/bin/sh", "-c", "sleep 15"]` in every Deployment and set `terminationGracePeriodSeconds >= 45`.

### Failure Scenario 2: Read-Only Root Filesystem Application Crash
- **The Trigger:** A Python microservice is deployed with `readOnlyRootFilesystem: true`. The Python runtime attempts to write `.pyc` bytecode caches or SQLite temp files to `/app` or `/tmp`.
- **The Blast Radius:** Python crashes on startup with `OSError: [Errno 30] Read-only file system`, throwing the container into `CrashLoopBackOff`.
- **Mitigation & Guardrail:** Set environment variables `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`, and explicitly mount a memory-backed `emptyDir` volume at `/tmp`.

---

## 4.3 Operational Triage & SRE Runbook

### Emergency Inspection Commands

```bash
# 1. Identify which SCC was assigned to a crashing pod
oc get pod secure-banking-api-7c94b79b9b-4k2x9 -n prod-banking-core \
  -o jsonpath='{.metadata.annotations.openshift\.io/scc}'

# 2. Inspect allocated UID range for the namespace
oc get project prod-banking-core -o yaml | grep -A 2 "sa.scc.uid-range"

# 3. Audit whether a ServiceAccount is permitted to use an SCC
oc adm policy who-can use scc restricted-v2 -n prod-banking-core

# 4. Debug container startup failure under read-only rootfs
oc logs secure-banking-api-7c94b79b9b-4k2x9 -n prod-banking-core --previous
```

### Emergency 3-Step SRE Triage Checklist
1. **Step 1: Verify SCC Authorization**
   If a pod fails with `Forbidden: unable to validate against any security context constraint`, inspect `spec.serviceAccountName` and verify the ServiceAccount has rolebindings in the namespace.
2. **Step 2: Inspect Container UID via CRI-O**
   Verify the image does not have hardcoded `USER 0` in its container manifest. Run `oc debug deployment/secure-banking-api` to inspect the effective user `id -u`.
3. **Step 3: Check Temporary Directory Quotas**
   If an application running with read-only root filesystem throws `No space left on device` during file generation, check if the memory-backed `emptyDir` size limit (128Mi) is exhausted.
