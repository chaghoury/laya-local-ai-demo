# Project Plan

## Goal

Build a reproducible, beginner-friendly Python demo that uses Laya, an open-weight local System 1 decision model, for structured decisions and explains where it can and cannot substitute for Jev. Include a runnable Jupyter walkthrough. Keep claims tied to upstream documentation and project-owned evaluation.

## Delivery Principles

- Keep setup reproducible with `uv`, a committed `pyproject.toml`, and `uv.lock` for this application/demo.
- Prefer the Python standard library and LAYA's supported integration. Add third-party packages only when a demonstrated feature needs them; do not install `pip` or `requests` by default without a concrete use.
- Keep reusable Python code separate from notebooks, documentation, and tests.
- Make inference local by default, while clearly explaining that the first prediction downloads model weights from Hugging Face. Never commit credentials, model weights, local databases, or generated environment files.
- Test the documented commands from a clean environment and run the notebook from top to bottom before calling the walkthrough complete.

## Ordered Work

### 1. Create the `uv` project and environment

- Initialize the Python application with `uv` and create `pyproject.toml`. Set the supported Python floor from the upstream Laya requirement and keep `.python-version` as the project's reproducible development interpreter pin.
- Create the project environment (`.venv`) and add a `.python-version` file if useful for keeping local tooling consistent.
- Generate and commit `uv.lock` so contributors can reproduce the resolved application dependencies.
- Ensure `.venv`, caches, secrets, and generated artifacts are ignored by Git.
- Document the prerequisites and initial setup commands.
- **Checkpoint:** a clean checkout can create the environment and run a minimal Python entry point using the documented `uv` commands.

### 2. Verify LAYA and the demo scope

- **Verified project:** [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya), published on PyPI as [`laya`](https://pypi.org/project/laya/) and with official weights on [Hugging Face](https://huggingface.co/convaiinnovations/laya). The upstream README currently reports release `0.3.26` (reviewed 2026-10-04); recheck before adding the dependency.
- Laya is a non-autoregressive System 1 model for typed `choice`, `score`, and yes/no (`noul`) decisions over supplied input. It does not generate free-form text and is not a general-purpose chat model.
- Upstream requires Python 3.10 or newer. Keep the project's development pin at Python 3.12, but set `requires-python` to `>=3.10` so the package metadata does not unnecessarily exclude supported Python users.
- The code and model card identify Apache-2.0. Verify and retain the upstream notices if distributing or modifying its code or weights.
- Installing the package does not download weights. `Router()` downloads the selected checkpoint from Hugging Face on first prediction; afterward inference can run locally without a hosted inference API. The README lists English and typed-decision checkpoints at about 421M parameters and multilingual at about 322M; actual disk and memory requirements vary by checkpoint, precision, and runtime. CPU is supported; upstream also documents Apple MPS and other hardware paths. Do not promise a minimum RAM figure without measuring it on the target machine.
- Jev is TypeSafe's hosted System 1 decision API. Laya offers a similar typed-decision workflow and an optional self-hosted `/v1/systemone` server, but it is not a drop-in replacement in every respect: upstream documents differences in option limits and confidence semantics, and some tasks require fine-tuning or calibration.
- **Chosen demo scope:** English support-ticket triage using the Python `Router` SDK and a small `choice` question (for example, billing, technical, or account support). Show the structured result and selected checkpoint. Keep it illustrative, compare outputs against a small hand-labeled fixture, and do not automate consequential actions. Defer `noul` and confidence thresholds until their behavior is validated on project data.
- **Checkpoint:** plan uses the verified package/API and Python floor; setup and model download expectations are explicit; the demo avoids claiming parity or general accuracy based only on vendor benchmarks.

### 3. Add only the required Python dependencies

- Separate runtime dependencies from development dependencies in `pyproject.toml`.
- Add the core PyPI package (`laya`) with `uv add laya`, after rechecking the current release. Use `Router`; do not add the optional server/framework extras for the initial SDK demo.
- Add development tools appropriate to the small demo, such as a formatter/linter and `pytest`; add Jupyter tooling for the walkthrough.
- Do not add `requests` for the SDK example; Laya provides the Python API. Add it only if a later, separately scoped HTTP-client example requires it. `pip` is not a project dependency when `uv` manages installation.
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
- Demonstrate local support-ticket classification with a small number of distinct labels, structured output, and the chosen checkpoint. Explain the first-use Hugging Face download and subsequent local inference.
- Add a small hand-labeled evaluation fixture and report its results as a demo check, not a general accuracy claim. Keep predictions advisory; do not trigger refunds, escalations, or other consequential actions automatically.
- Add focused tests for project-owned logic and a smoke test or documented manual check for the Laya integration. Tests that require a model download should be clearly marked and should not make the fast default test suite unexpectedly expensive.
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

## Decisions to Recheck During Implementation

- Recheck the current PyPI release and upstream install instructions before dependency installation; upstream listed `0.3.26` on 2026-10-04.
- Confirm runtime behavior on the target machine and document actual checkpoint download size, latency, and memory use; hardware-specific figures from upstream are not guarantees for this project.
- Validate triage behavior on the project's own examples before presenting any quality or confidence claims.
- Keep the optional Jev-compatible HTTP server out of the initial scope unless demonstrating wire-protocol compatibility becomes a concrete requirement.
- Select optional development tools only when they support the tests, notebook, or maintenance needs of this small demo.
