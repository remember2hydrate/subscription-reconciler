# Subscription Reconciler

A production-quality billing engine that calculates monthly subscription charges based on a stream of SubscriptionEvents.

The engine supports:
- Daily proration
- Immediate upgrades
- Next-day downgrades
- Cancellation
- “Indecisive” rule: upgrade + downgrade within 24h = ignored

## Architecture
The solution is divided into:
- `/domain`  — Events, Plans, Periods
- `/engine`  — Normalization and billing logic
- `/tests`   — Unit tests for all business rules

The pipeline is:
1. Sort → 2. Normalize → 3. Build billing periods → 4. Calculate total

## Design Decisions
- Billing periods are used to isolate arithmetic from rule application.
- The “indecisive” rule is handled before the main logic.

## How to Test
pytest tests/test_reconciler.py