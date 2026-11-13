
from datetime import datetime, timedelta, timezone
 
 
def deals_needing_followup(deals, today=None):
    """Return names of open deals with no contact in the last 14 days,
    most stale first. Timestamps are normalised to UTC, so mixed
    offsets are handled correctly."""
    today = today or datetime.now(timezone.utc)
    if today.tzinfo is None:
        today = today.replace(tzinfo=timezone.utc)
    today = today.astimezone(timezone.utc)
    result = []
    for deal in deals:
        if deal["stage"].startswith("Closed"):
            continue
        if deal["last_contact"] is None:
            last = datetime.min.replace(tzinfo=timezone.utc)
        else:
            last = datetime.fromisoformat(deal["last_contact"])
            if last.tzinfo is None:
                last = last.replace(tzinfo=timezone.utc)
            last = last.astimezone(timezone.utc)
        if today - last > timedelta(days=14):
            result.append((last, deal["name"]))
    result.sort(key=lambda item: item[0])
    return [name for _, name in result]
