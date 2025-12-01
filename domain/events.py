from dataclasses import dataclass
from datetime import date
from domain.plans import Plan

@dataclass(frozen=True)
class SubscriptionEvent:
    date: date
    type: str  # "start", "upgrade", "downgrade", "cancel"
    plan: Plan | None

