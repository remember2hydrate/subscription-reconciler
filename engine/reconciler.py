from datetime import date, timedelta
from domain.plans import DAILY_RATES

FEB_END_EXCLUSIVE = date(2024, 2, 28) 

def normalize_events(events):
    events = sorted(events, key=lambda e: e.date)
    cleaned = []
    i = 0

    while i < len(events):
        e = events[i]
        if e.type == "upgrade" and i + 1 < len(events):
            nxt = events[i + 1]
            # indecisive: upgrade followed by downgrade within 24 hours -> ignore both
            if nxt.type == "downgrade" and (nxt.date - e.date) < timedelta(days=1):
                i += 2
                continue
        cleaned.append(e)
        i += 1

    return cleaned

def build_periods(events):
    
    #Returns list of (start_inclusive_date, end_exclusive_date, plan)
    # upgrade applies same day; previous period ends at upgrade date (exclusive)
    # downgrade applies next day: keep charging higher rate for downgrade day
    # so previous period ends at (downgrade_date + 1) exclusive
    # cancel applies immediately and cancel day is NOT billed,
    # so previous period ends at cancel_date (exclusive)
    # No cancel: extend to month end exclusive

    periods = []
    plan = None
    start = None

    for idx, e in enumerate(events):
        if e.type == "start":
            plan = e.plan
            start = e.date

        elif e.type == "upgrade":
        
            periods.append((start, e.date, plan))
            plan = e.plan
            start = e.date

        elif e.type == "downgrade":
            
            periods.append((start, e.date + timedelta(days=1), plan))
            plan = e.plan
            start = e.date + timedelta(days=1)

        elif e.type == "cancel":
            
            periods.append((start, e.date, plan))
            return periods

    periods.append((start, FEB_END_EXCLUSIVE, plan))
    return periods

def bill(periods):
    total = 0.0
    for start, end, plan in periods:
        if plan is None or start is None or end is None:
            continue
        days = (end - start).days
        total += days * DAILY_RATES[plan]
    return total
