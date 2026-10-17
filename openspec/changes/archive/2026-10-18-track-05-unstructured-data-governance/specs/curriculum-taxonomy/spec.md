# Spec Delta: curriculum-taxonomy

## MODIFIED Requirements

### Requirement: Four Core Technical Tracks
The repository SHALL organize all engineering modules under five distinct top-level track directories: `tracks/01-cloud-native-infra`, `tracks/02-ai-models-inference`, `tracks/03-modern-data-layers`, `tracks/04-agentic-workflows`, and `tracks/05-unstructured-data-governance`.

#### Scenario: Valid track directory access
- **WHEN** an author or consumer inspects the `tracks/` directory
- **THEN** the five designated track directories exist with track-level `README.md` syllabus overviews.

#### Scenario: Track 05 syllabus and linter recognition
- **WHEN** `shared/scripts/validate-module.py` or a curriculum consumer validates `tracks/05-unstructured-data-governance`
- **THEN** the track is recognized as a valid first-class curriculum domain.
