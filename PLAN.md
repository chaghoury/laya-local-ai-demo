# Project Plan

## Goal

Build a reproducible, beginner-friendly Python demo that installs and runs LAYA locally, explains how it can be used as an open-source alternative to Jev, and provides a runnable Jupyter walkthrough. Verify LAYA's official name, capabilities, installation method, license, and relationship to Jev before documenting claims or choosing an integration.

## Delivery Principles

- Keep setup reproducible with `uv`, a committed `pyproject.toml`, and `uv.lock` for this application/demo.
- Prefer the Python standard library and LAYA's supported integration. Add third-party packages only when a demonstrated feature needs them; do not install `pip` or `requests` by default without a concrete use.
- Keep reusable Python code separate from notebooks, documentation, and tests.
- Make local execution the default, explain any model downloads or network use, and never commit credentials, model weights, local databases, or generated environment files.
- Test the documented commands from a clean environment and run the notebook from top to bottom before calling the walkthrough complete.

## Ordered Work

### 1. Create the `uv` project and environment

- Initialize the Python application with `uv` and create `pyproject.toml`. Use a provisional Python version until LAYA's compatibility is verified in step 2.
- Create the project environment (`.venv`) and add a `.python-version` file if useful for keeping local tooling consistent.
- Generate and commit `uv.lock` so contributors can reproduce the resolved application dependencies.
- Ensure `.venv`, caches, secrets, and generated artifacts are ignored by Git.
- Document the prerequisites and initial setup commands.
- **Checkpoint:** a clean checkout can create the environment and run a minimal Python entry point using the documented `uv` commands.

### 2. Verify LAYA and the demo scope

- Find and review LAYA's official repository and installation/usage documentation.
- Confirm supported operating systems, Python/runtime requirements, installation channels, license, local resource requirements, model behavior, and any optional cloud or telemetry behavior.
- Confirm what “Jev alternative” means for this project and select one focused, useful demo scenario that can run locally.
- Revisit the provisional Python version selected in step 1 and adjust it if LAYA's supported requirements call for a different version.
- Record verified facts and any limitations in the README or a short reference section in `docs/`.
- **Checkpoint:** installation and API choices are based on current upstream guidance rather than guessed package names or commands.

### 3. Add only the required Python dependencies

- Separate runtime dependencies from development dependencies in `pyproject.toml`.
- Add LAYA's supported Python package or client after verifying its official installation instructions.
- Add development tools appropriate to the small demo, such as a formatter/linter and `pytest`; add Jupyter tooling for the walkthrough.
- Add `requests` only if the chosen example directly makes HTTP requests and LAYA does not already provide a suitable client. `pip` is normally not a project dependency when `uv` manages installation.
- Lock dependency versions and document the commands for syncing runtime and development dependencies.
- **Checkpoint:** `uv sync` and the project's import/test smoke checks succeed in a fresh environment.

### 4. Establish the repository structure and contributor guidance

- Organize the implementation and supporting material along these lines, adjusting names to the actual LAYA integration:

  ```text
  .github/                 # Optional issue or contribution templates
  docs/                    # Setup notes, design choices, troubleshooting
  notebooks/               # Ordered, executable walkthrough
  src/laya_local_ai_demo/  # Reusable Python code and CLI/demo entry point
  tests/                   # Fast tests for project-owned behavior
  AGENTS.md                # Canonical contributor and coding guidance
  CLAUDE.md                # Points to AGENTS.md
  GEMINI.md                # Points to AGENTS.md
  PLAN.md
  README.md
  pyproject.toml
  uv.lock
  ```

- Write `AGENTS.md` as the single source of project guidance: environment setup, commands, layout, style, testing expectations, local-first behavior, and rules for handling secrets and large model files.
- Make `CLAUDE.md` and `GEMINI.md` short compatibility files that direct their respective agents to read and follow `AGENTS.md`; avoid duplicating policy that can drift.
- **Checkpoint:** the three guidance files agree, and a contributor can discover the supported setup, run, and test commands from the root documentation.

### 5. Implement and test the LAYA example

- Implement one small end-to-end use case under `src/laya_local_ai_demo/`, using LAYA's verified local API.
- Keep configuration explicit and safe: provide sensible defaults, validate user input, explain model selection and resource requirements, and avoid embedding secrets or machine-specific paths.
- Make the example show a real benefit of the local workflow, such as running an inference/task locally and inspecting the result; distinguish verified behavior from claims or assumptions.
- Add focused tests for project-owned logic and a smoke test or documented manual check for the LAYA integration. Tests that require a model or large download should be clearly marked and should not make the fast default test suite unexpectedly expensive.
- **Checkpoint:** the example runs using documented commands on a supported machine, and failures such as a missing runtime/model produce actionable guidance.

### 6. Build the Jupyter walkthrough

- Create `notebooks/laya_local_ai_walkthrough.ipynb` with alternating Markdown and Python cells.
- Present the walkthrough in runnable order: goals and prerequisites; environment/dependency setup; LAYA installation or verification; local configuration; the selected example; result inspection; troubleshooting and cleanup.
- Use the project's `uv` environment as the notebook kernel and avoid asking readers to paste secrets into notebook cells.
- Keep substantive reusable logic in `src/`; notebook code should demonstrate and explain the public workflow rather than become a second implementation.
- Run all cells from a clean, supported environment. Make expensive model downloads clear and avoid committing large outputs or downloaded artifacts.
- **Checkpoint:** the notebook executes top-to-bottom and agrees with the README and `AGENTS.md` commands.

### 7. Complete documentation and quality checks

- Update `README.md` with the project purpose, verified LAYA/Jev context, prerequisites, setup, run/test commands, example outcome, notebook link, and known limitations.
- Add concise module and API docstrings where they clarify non-obvious behavior; comment only where a decision or operation is not self-evident.
- Add troubleshooting notes for common environment, installation, model, and resource issues.
- From a clean environment, run formatting/linting, tests, the example smoke check, and the notebook walkthrough; resolve discrepancies in documented commands.
- Review the repository for accidental secrets, machine-specific paths, generated files, and oversized artifacts.
- **Completion checkpoint:** a new contributor can follow the README from checkout through local execution and notebook completion without undocumented steps.

## Decisions to Confirm During Implementation

- The exact LAYA project/package and its current supported installation method.
- Supported Python and operating-system versions, based on LAYA's upstream requirements.
- The specific feature or workflow that makes the demo a meaningful Jev alternative.
- Whether the example requires a model download, additional system runtime, or optional network access.
- Which optional development tools provide value without making setup unnecessarily heavy.
