from typing import Callable, List

TRANSITIONS = {
    "NEW": {
        "PAY_OK": "PAID",
        "PAY_FAIL": "CANCELLED",
    },
    "PAID": {},
    "CANCELLED": {},
}

def next_state(state: str, event: str) -> str:
    state = state.strip().upper()
    event = event.strip().upper()

    if state not in TRANSITIONS:
        raise ValueError(f"Unknown state: {state}")
    if event not in TRANSITIONS[state]:
        raise ValueError(f"Unknown event: {event} for state {state}")

    return TRANSITIONS[state][event]


class SagaStep:
    def __init__(self, name: str, action: Callable[[], None], compensate: Callable[[], None], succ: str):
        self.name = name
        self.action = action
        self.compensate = compensate
        self.succ = succ


class SagaOrch:
    def __init__(self, steps: List[SagaStep]):
        self.steps = steps
        self.state = "NEW"
        self.completed: List[SagaStep] = []

    def run(self) -> None:
        try:
            for step in self.steps:
                step.action()
                self.completed.append(step)

            self.state = next_state(self.state, "PAY_OK")

        except Exception:
            self.state = next_state(self.state, "PAY_FAIL")

            for step in reversed(self.completed):
                try:
                    step.compensate()
                except Exception:
                    pass
            raise