# Laya Local AI Demo

A small Python project showing how to use [Laya](https://github.com/NandhaKishorM/laya), an open-weight local decision model, for structured support-ticket routing. Laya is a Jev alternative for typed decisions, not a general-purpose chat model or a universal drop-in replacement.

## What This Demo Does

The CLI passes a synthetic English support ticket to Laya's `Router` and asks one `choice` question over four queues: billing, technical, account, and other. It prints the suggested queue and selected checkpoint as advisory output; it does not automate ticket assignment or other consequential actions.

The first prediction downloads the selected checkpoint from Hugging Face. After that download, the Python SDK performs inference locally without calling a hosted inference API. Model weights are not stored in this repository.

For this workflow, typed output can be consumed directly as a queue suggestion instead of parsing generated prose. Local inference can keep ticket text off a hosted inference endpoint and avoids per-request hosted inference billing after setup; hardware, power, storage, and maintenance still have costs.

## Requirements

- `uv`
- Python 3.10 or newer; the repository's development interpreter is pinned to Python 3.12
- Network access to Hugging Face for the first prediction
- Enough disk and available memory for the selected checkpoint; exact requirements vary by runtime and machine

## Setup and Run

From the repository root:

```sh
uv sync
uv run laya-local-ai-demo "I was charged twice for my monthly subscription."
```

On first use, the command downloads the selected model checkpoint. Subsequent runs use the local cache. The output is JSON, for example:

```json
{
  "queue": "billing",
  "checkpoint": "english"
}
```

Treat the predicted queue as a suggestion and have a person review it. Avoid sending real customer data through this demo.

## Evaluation and Tests

Run the eight-example, synthetic demonstration fixture:

```sh
uv run python scripts/evaluate_demo.py
```

The printed accuracy describes only this tiny hand-labeled fixture. It is not a general accuracy estimate or a production readiness test.

Run the weight-free unit tests and code checks:

```sh
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Unit tests use a fake router and do not download model weights.

## Notebook Walkthrough

Open [notebooks/laya_local_ai_walkthrough.ipynb](notebooks/laya_local_ai_walkthrough.ipynb) and select the `Python (laya-local-ai-demo)` kernel. To register it if needed:

```sh
uv run --group dev python -m ipykernel install --user --name laya-local-ai-demo --display-name "Python (laya-local-ai-demo)"
```

Run the notebook from top to bottom. Its first prediction uses the same Hugging Face checkpoint cache as the CLI.

For a concise, self-contained presentation example that imports only Laya and the Python standard library, see [notebooks/laya_presentation_demo.ipynb](notebooks/laya_presentation_demo.ipynb).

## Laya and Jev

Both systems support typed decisions, but their models, hosting, limits, and confidence semantics differ. Laya can be run with local open weights; Jev is a hosted API. The optional Laya HTTP server implements a Jev-shaped endpoint, but protocol compatibility does not guarantee equal predictions or behavior. See [docs/laya-and-jev.md](docs/laya-and-jev.md) before evaluating a migration.

## Project Guidance

See [AGENTS.md](AGENTS.md) for contributor commands, structure, test expectations, and local-data/model safety rules. `CLAUDE.md` and `GEMINI.md` point to that canonical guidance.
