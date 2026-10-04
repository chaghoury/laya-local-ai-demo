from collections.abc import Mapping

import pytest

from laya_local_ai_demo.triage import QUEUE_DESCRIPTIONS, TicketTriage


class FakeRouter:
    def __init__(self, prediction: Mapping[str, object]) -> None:
        self.prediction = prediction
        self.calls: list[tuple[dict[str, str], dict[str, object]]] = []

    def predict(
        self,
        state: dict[str, str],
        questions: dict[str, dict[str, object]],
    ) -> Mapping[str, object]:
        self.calls.append((state, questions))
        return self.prediction


def test_classify_returns_queue_and_checkpoint() -> None:
    router = FakeRouter(
        {
            "answers": {"queue": {"choice": "billing"}},
            "routing": {"model": "english"},
        }
    )

    result = TicketTriage(router).classify("Duplicate charge on my invoice")

    assert result.queue == "billing"
    assert result.checkpoint == "english"
    assert router.calls[0][0] == {"body": "Duplicate charge on my invoice"}
    assert set(router.calls[0][1]["queue"]["criteria"]) == set(QUEUE_DESCRIPTIONS)


@pytest.mark.parametrize("ticket", ["", "  \n"])
def test_classify_rejects_empty_ticket(ticket: str) -> None:
    router = FakeRouter({})

    with pytest.raises(ValueError, match="must not be empty"):
        TicketTriage(router).classify(ticket)

    assert router.calls == []


def test_classify_rejects_unknown_queue() -> None:
    router = FakeRouter(
        {
            "answers": {"queue": {"choice": "unknown"}},
            "routing": {"model": "english"},
        }
    )

    with pytest.raises(RuntimeError, match="outside the configured choices"):
        TicketTriage(router).classify("A ticket")


def test_classify_rejects_missing_routing_metadata() -> None:
    router = FakeRouter({"answers": {"queue": {"choice": "technical"}}})

    with pytest.raises(TypeError, match="invalid routing value"):
        TicketTriage(router).classify("A ticket")
