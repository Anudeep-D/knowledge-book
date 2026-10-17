# module-contract Specification

## Purpose

Enforces the strict four-part pedagogical contract, visual diagramming standards, production-grade code requirements, and automated validation rules for all curriculum modules.

## Requirements

### Requirement: Four Mandatory Pedagogical Sections
Every module `index.md` SHALL contain exactly four top-level numbered sections: "1. Interactive Concept Breakdown", "2. Visual Architecture", "3. Real-World Code & Configuration", and "4. Edge Cases, Failure Modes & Trade-offs".

#### Scenario: Module section structure compliance
- **WHEN** a module is validated against the pedagogical contract
- **THEN** all four section headers are present in sequential order without omissions.

### Requirement: Concept Breakdown First-Principles Structure
The "Interactive Concept Breakdown" section SHALL explain "the why before the how", including a real-world production incident or bottleneck, first-principles intuition, and core invariants before presenting implementations.

#### Scenario: Production problem framing
- **WHEN** a reader reads Section 1 of any module
- **THEN** it explicitly states the production failure mode or scaling limit that motivated the architecture.

### Requirement: Visual Architecture Separation
The "Visual Architecture" section SHALL contain at least one embedded diagram explicitly visualizing the topology, separating control plane from data plane, and depicting labeled state or packet flows.

#### Scenario: Architecture diagram verification
- **WHEN** Section 2 is inspected
- **THEN** at least one ASCII or Mermaid diagram is present delineating control plane components from data plane execution.

### Requirement: Enterprise-Grade Code and Manifest Quality
The "Real-World Code & Configuration" section SHALL contain complete, production-ready manifests or code snippets that include enterprise safeguards such as resource limits, health probes, and security contexts.

#### Scenario: Production readiness checks in manifests
- **WHEN** Kubernetes manifests or code configurations are provided in Section 3
- **THEN** they specify explicit CPU/memory boundaries, probe definitions, and non-root security contexts without toy placeholders.

### Requirement: Trade-off Matrix and Operational Runbook
The "Edge Cases, Failure Modes & Trade-offs" section SHALL provide a comparative decision table comparing architectural options or deterministic versus stochastic patterns, alongside an operational triage runbook.

#### Scenario: Comparative decision table validation
- **WHEN** Section 4 is inspected
- **THEN** a markdown table exists specifying when to use the pattern, when it breaks down, and key triaging runbook indicators.

#### Scenario: Design pattern comparative matrix
- **WHEN** a module evaluates software or agentic design patterns
- **THEN** Section 4 includes a comparative analysis contrasting traditional deterministic implementations with non-deterministic LLM-driven architectures.

### Requirement: Automated Module Linter
The repository SHALL provide an automated CLI validation script that inspects module directories, checks frontmatter keys, verifies required section headers, and reports schema errors.

#### Scenario: Validation script execution
- **WHEN** `python3 shared/scripts/validate-module.py --path <module-dir>` is executed
- **THEN** the script outputs exit code 0 if the module satisfies the contract, or a non-zero exit code with specific missing section errors if invalid.
