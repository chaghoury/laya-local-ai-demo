# Project Guidance

## Purpose and Scope

This repository demonstrates Laya, an open-weight local System 1 decision model, through an English support-ticket routing example. Laya returns structured decisions; it is not a general-purpose chat or text-generation model. The example is educational and advisory, not an automated decision system.

Read `PLAN.md` for the ordered delivery scope and verified upstream caveats. Recheck Laya's official documentation before changing the integration or repeating version-specific claims.

## Environment and Commands

- Use the pinned Python interpreter and dependencies managed by `uv`.
- Create or synchronize the environment with `uv sync`.
- Run project commands with `uv run ...`; do not install project dependencies with global `pip`.
- Keep `pyproject.toml` and `uv.lock` in sync when changing dependencies.
- The VS Code notebook kernel should use this repository's `.venv`.

## Project Layout

- `src/laya_local_ai_demo/`: reusable implementation and command-line entry point.
- `tests/`: fast tests for project-owned behavior.
- `notebooks/`: explanatory, top-to-bottom runnable walkthroughs.
- `docs/`: supporting setup and troubleshooting material.
- `PLAN.md`: ordered work and decisions.

Keep model integration behind a small project-owned API. Keep notebook examples focused on calling that API rather than duplicating implementation logic.

## Model and Data Safety

- Explain that model weights are downloaded from Hugging Face on the first prediction; inference runs locally afterward.
- Never commit model weights, caches, real customer tickets, credentials, or machine-specific paths.
- Use synthetic examples in source, tests, documentation, and notebooks.
- Do not claim accuracy, calibration, or Jev parity based on vendor benchmarks. Validate behavior on the project's own labeled examples and identify that evaluation as illustrative.
- Do not perform consequential actions from model output. Keep routing suggestions advisory and do not rely on confidence thresholds without project-specific validation.
- Keep the initial question to a small set of distinct labels; avoid high-cardinality choices.

## Code and Tests

- Prefer small, typed, documented functions and standard-library code where practical.
- Validate inputs at project boundaries and provide actionable errors for missing model/runtime or download failures.
- Add tests for deterministic project-owned behavior. Tests must not download model weights; keep real-model checks explicitly opt-in or manual.
- Format and lint with Ruff, and run the fast suite with pytest before considering implementation complete.
- Keep notebooks free of large saved outputs and execute every code cell in order before updating the walkthrough.
