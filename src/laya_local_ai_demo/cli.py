"""Command-line entry point for the local ticket-routing example."""

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict

from laya_local_ai_demo.triage import TicketTriage


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Classify a synthetic or user-provided support ticket with Laya."
    )
    parser.add_argument("ticket", help="English support-ticket text")
    arguments = parser.parse_args(argv)

    try:
        result = TicketTriage().classify(arguments.ticket)
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        parser.exit(
            1,
            f"{parser.prog}: Laya inference failed. On first use, check Hugging "
            f"Face access and available memory. Details: {error}\n",
        )

    print(json.dumps(asdict(result), indent=2))
