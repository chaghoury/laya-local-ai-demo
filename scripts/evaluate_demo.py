"""Run the small synthetic ticket fixture through Laya and report raw accuracy."""

import json
from pathlib import Path

from laya_local_ai_demo.triage import TicketTriage

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "data" / "demo_tickets.json"


def main() -> None:
    examples = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    triage = TicketTriage()
    results = []

    for example in examples:
        prediction = triage.classify(example["ticket"])
        results.append(
            {
                "expected": example["expected_queue"],
                "predicted": prediction.queue,
                "correct": prediction.queue == example["expected_queue"],
            }
        )

    correct = sum(result["correct"] for result in results)
    report = {
        "correct": correct,
        "total": len(results),
        "accuracy": correct / len(results) if results else 0.0,
        "results": results,
        "note": "Small synthetic demo fixture; not a general accuracy estimate.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
