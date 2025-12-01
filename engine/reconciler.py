from datetime import timedelta

def normalize_events(events):
    events = sorted(events, key=lambda e: e.date)
    cleaned = []
    i = 0

    while i < len(events):
        e = events[i]
        if e.type == "upgrade" and i + 1 < len(events):
            nxt = events[i+1]
            if nxt.type == "downgrade" and (nxt.date - e.date) < timedelta(days=1):
                i += 2
                continue
        cleaned.append(e)
        i += 1

    return cleaned