# AGENTS.md

This file provides guidance to agents when working with code in this repository.

This is a documentation-first curriculum (not an application): 5 tracks × modules under `tracks/`, each module = `index.md` + `artifacts/` + `diagrams/`. There is no pytest suite, no ruff config, and no build step.

## Commands
- Setup: `uv sync` (deps declared in `pyproject.toml`, locked in `uv.lock`; `package = false`). Run scripts with `uv run ...`.
- `requirements.txt` is GENERATED, do not hand-edit: after changing `pyproject.toml` run `uv pip compile pyproject.toml --group dev -o requirements.txt --python-version 3.12`.
- Optional heavy deps (langgraph, prefect, presidio, pyspark) are not installed; artifacts guard those imports.
- Validate all modules: `uv run python shared/scripts/validate-module.py --all`
- Validate a single module: `uv run python shared/scripts/validate-module.py --path tracks/01-cloud-native-infra/01-modern-system-design-microservices`
- README documents `--track <name>` and a positional module path; the script supports ONLY `--path` and `--all`. Use those.
- "Single test" = run one artifact directly: `python3 tracks/<track>/<module>/artifacts/<file>.py` (each has an `if __name__ == "__main__":` demo; no `test_*` files exist).
- Lint (if needed): `ruff check <file>` with default settings; no repo config.

## Module contract (enforced by `shared/scripts/validate-module.py`)
- `index.md` must have frontmatter with `id, title, track, difficulty, estimated_minutes (int > 0), tags`. `track` must exactly match one of the 5 directory names (hard-coded `VALID_TRACKS` in the script — update it when adding a track).
- The frontmatter parser is hand-rolled (no PyYAML): lists must be `- item` lines; inline `[a, b]` lists are not parsed.
- Sections must be H1 (`# 1. Interactive Concept Breakdown`, `# 2. Visual Architecture`, `# 3. Real-World Code & Configuration`, `# 4. Edge Cases, Failure Modes & Trade-offs`) — H1, not H2. The module title is also an H1.
- Needs ≥1 Mermaid block or ASCII diagram (`+---`, `|---`, `===>`, `<---`) and ≥1 markdown table with a `| :--- |` separator row.
- Both `diagrams/` and `artifacts/` directories must exist (use `.gitkeep` if empty).
- Start new modules from `templates/module-template.md`; also register them in the root `README.md` and the track `README.md`.
- Spec source of truth: `openspec/specs/module-contract/spec.md`. Changes are managed via OpenSpec (`openspec/changes/`, workflows in `.agents/workflows/opsx-*.md`).

## Code style (artifacts, Python 3.12+)
- Production-grade, typed, self-contained scripts: module docstring listing what it "Demonstrates", `from __future__ import annotations` in Pydantic/async-heavy files, `@dataclass(frozen=True)` for configs, Pydantic v2 `BaseModel`/`Field` for validated models, `typing.Protocol` for Strategy interfaces.
- Heavy optional deps (e.g. `pyspark`) are imported inside try/except within methods and fall back to printing config, so artifacts run without them. Keep that pattern.
- Each artifact ends with an `if __name__ == "__main__":` runnable demo.
- Config/manifests: Kubernetes/OpenShift YAML must include resource requests/limits, probes, and non-root `securityContext` (`runAsNonRoot`, `readOnlyRootFilesystem`, drop ALL caps); no toy placeholders.
- Diagrams: Mermaid in `.mmd` files or `diagram_source.txt`; ASCII diagrams must stay terminal-safe plain ASCII and split Control Plane vs Data Plane.
