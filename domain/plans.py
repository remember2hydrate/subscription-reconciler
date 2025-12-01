from enum import Enum

class Plan(Enum):
    BASIC = "basic"
    PREMIUM = "premium"

DAILY_RATES = {
    Plan.BASIC: 10 / 28,
    Plan.PREMIUM: 30 / 28,
}

