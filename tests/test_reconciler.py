from datetime import date
from domain.events import SubscriptionEvent
from domain.plans import Plan
from engine.reconciler import normalize_events, build_periods, bill

def print_periods(periods):
    print("\nBilling Periods:")
    for start, end, plan in periods:
        print(f"  {start} → {end} | {plan.value}")
    print()

def test_given_scenario():
    print("\n=== Running: test_given_scenario ===")

    events = [
        SubscriptionEvent(date(2024,2,2), "start", Plan.BASIC),
        SubscriptionEvent(date(2024,2,10), "upgrade", Plan.PREMIUM),
        SubscriptionEvent(date(2024,2,12), "downgrade", Plan.BASIC),
        SubscriptionEvent(date(2024,2,25), "cancel", None),
    ]

    clean = normalize_events(events)
    periods = build_periods(clean)
    total = bill(periods)

    print_periods(periods)
    print(f"Total billed: {total:.2f}")

    assert round(total, 2) == 10.36
    print("Result: OK")


def test_indecisive_rule():
    print("\n=== Running: test_indecisive_rule ===")

    events = [
        SubscriptionEvent(date(2024,2,5), "start", Plan.BASIC),
        SubscriptionEvent(date(2024,2,10), "upgrade", Plan.PREMIUM),
        SubscriptionEvent(date(2024,2,10), "downgrade", Plan.BASIC), 
    ]

    clean = normalize_events(events)
    periods = build_periods(clean)
    total = bill(periods)

    print_periods(periods)
    print(f"Total billed: {total:.2f}")

    expected_days = (date(2024,2,28) - date(2024,2,5)).days
    assert round(total, 2) == round(expected_days * (10/28), 2)
    print("Result: OK")

