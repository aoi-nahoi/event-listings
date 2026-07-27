# Project context

## Requirements

### Requirement: Repository provides agent and tooling context
The repository SHALL include agent guidance and lint/test tooling for reviewers and AI assistants.

#### Scenario: Agent guidance is present
- **WHEN** a contributor opens the repository
- **THEN** they SHALL find `AGENTS.md`, `.gitignore`, `.pylintrc`, Ruff config, Cursor skills, and OpenSpec context

### Requirement: Documentation maps to the course rubric
The repository SHALL document how implementation evidence maps to the grading rubric.

#### Scenario: Rubric evidence
- **WHEN** a reviewer opens `docs/rubric-alignment.md`
- **THEN** each rubric item SHALL point to concrete files or GitHub evidence
