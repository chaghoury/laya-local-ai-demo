"""Advisory support-ticket routing through Laya's typed decision API."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

QUEUE_DESCRIPTIONS = {
    "billing": "Invoices, payments, duplicate charges, or refunds",
    "technical": "Product bugs, errors, outages, or integrations",
    "account": "Login, password, access, or account settings",
    "other": "A request that does not fit the other support queues",
}


class RouterProtocol(Protocol):
    def predict(
        self,
        state: dict[str, str],
        questions: dict[str, dict[str, object]],
    ) -> Mapping[str, object]: ...


@dataclass(frozen=True)
class TriageResult:
    queue: str
    checkpoint: str


def _questions() -> dict[str, dict[str, object]]:
    return {
        "queue": {
            "type": "choice",
            "instructions": "Which support queue should handle this ticket?",
            "criteria": QUEUE_DESCRIPTIONS.copy(),
        }
    }


def _as_mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"Laya returned an invalid {field} value")
    return value


class TicketTriage:
    """Classify one English ticket and report Laya's selected checkpoint."""

    def __init__(self, router: RouterProtocol | None = None) -> None:
        self._router = router

    def classify(self, ticket: str) -> TriageResult:
        if not isinstance(ticket, str):
            raise TypeError("ticket must be a string")
        if not ticket.strip():
            raise ValueError("ticket must not be empty")

        prediction = self._get_router().predict({"body": ticket}, _questions())
        answers = _as_mapping(prediction.get("answers"), "answers")
        queue_answer = _as_mapping(answers.get("queue"), "queue answer")
        queue = queue_answer.get("choice")
        if not isinstance(queue, str) or queue not in QUEUE_DESCRIPTIONS:
            raise RuntimeError("Laya returned a queue outside the configured choices")

        routing = _as_mapping(prediction.get("routing"), "routing")
        checkpoint = routing.get("model")
        if not isinstance(checkpoint, str) or not checkpoint:
            raise RuntimeError("Laya did not report the selected checkpoint")

        return TriageResult(queue=queue, checkpoint=checkpoint)

    def _get_router(self) -> RouterProtocol:
        if self._router is None:
            try:
                from laya import Router
            except ImportError as error:
                raise RuntimeError(
                    "Laya is not installed in this environment; run `uv sync`."
                ) from error
            self._router = Router()
        return self._router
