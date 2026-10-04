# Laya and Jev: Scope and Caveats

This project uses Laya for a small, local structured-classification example. It does not claim that Laya matches Jev on every task or that the demo is production-ready.

## What Laya Is

Laya is a non-autoregressive decision model. Its Python SDK accepts an input state and typed questions such as `choice`, `score`, and `noul`, and returns structured answers. It does not generate free-form text. The SDK's `Router` selects a checkpoint and is the recommended starting point for the Python example.

The package is published on PyPI as `laya`. Upstream documents Python 3.10 or newer and an Apache-2.0 license for the project. Review upstream license notices before redistributing the package or weights.

## Local Execution and Downloads

Installing the Python package does not install model weights. The first prediction retrieves the selected checkpoint from Hugging Face; later inference can run from the local cache without a hosted inference API. This requires network access for the initial download and local disk, memory, and compute resources. The demo intentionally does not preload every checkpoint.

## Relationship to Jev

Jev is TypeSafe's hosted System 1 decision API. Laya provides a similar typed-decision workflow and an optional self-hosted HTTP server using the Jev-shaped `/v1/systemone` endpoint. That protocol similarity does not make the underlying systems equivalent:

- Their hosted/local deployment models differ. Laya's direct SDK runs the model locally after weights are downloaded; the optional server also runs on infrastructure you operate.
- Laya documents differences in option limits and confidence semantics. In particular, do not transfer a Jev confidence threshold to Laya without measuring and calibrating it for your own data.
- Laya's upstream benchmarks note cases where it performs poorly, including high-cardinality choice questions. Some reported strong task results use fine-tuned checkpoints; they should not be attributed to the base model.
- A structured result is not proof that a decision is correct. The demo does not take actions based on model output.

The first example is deliberately limited to four clear support queues. Its tiny synthetic fixture helps show how to run a basic check, but it is not representative of real ticket traffic.

## Upstream References

- [Laya GitHub repository and README](https://github.com/NandhaKishorM/laya)
- [Laya on PyPI](https://pypi.org/project/laya/)
- [Official Laya model on Hugging Face](https://huggingface.co/convaiinnovations/laya)
- [Laya's published benchmark notes](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md)
