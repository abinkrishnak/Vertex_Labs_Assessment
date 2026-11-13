from datetime import datetime, timezone
 
from fix import deals_needing_followup
 
TODAY = datetime(2026, 11, 1, tzinfo=timezone.utc)
 
 
def deal(name, last, stage="Sourcing"):
    return {"name": name, "stage": stage, "last_contact": last}
 
 
# ---- original tests (only change: fixed `today` so they don't use the clock)
def test_excludes_closed():
    deals = [
        {"name": "A", "stage": "Closed - Won",
         "last_contact": "2026-09-01T09:00:00+08:00"},
    ]
    assert deals_needing_followup(deals, today=TODAY) == []
 
 
def test_stale_deal_returned():
    deals = [
        {"name": "B", "stage": "Diligence",
         "last_contact": "2026-10-01T09:30:00+08:00"},
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["B"]
 
 
def test_no_shared_state():
    deals = [
        {"name": "C", "stage": "Sourcing",
         "last_contact": "2026-09-01T09:00:00+08:00"},
    ]
    deals_needing_followup(deals, today=TODAY)
    assert deals_needing_followup(deals, today=TODAY) == ["C"]
 
 
def test_mixed_offsets_sorted_most_stale_first():
    deals = [
        {"name": "India", "stage": "Sourcing",
         "last_contact": "2026-10-02T10:00:00+05:30"},
        {"name": "Singapore", "stage": "Sourcing",
         "last_contact": "2026-10-01T09:30:00+08:00"},
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["Singapore", "India"]
 
 
# ---- new tests (the 4 in the written answer)
def test_none_last_contact_included_first():
    deals = [deal("Old", "2026-10-01T09:00:00+08:00"), deal("Never", None)]
    assert deals_needing_followup(deals, today=TODAY) == ["Never", "Old"]
 
 
def test_mixed_offsets_sorted_by_real_time():
    # Singapore = 10-01 16:00 UTC (older), India = 10-01 18:00 UTC
    deals = [deal("India", "2026-10-01T23:30:00+05:30"),
             deal("Singapore", "2026-10-02T00:00:00+08:00")]
    assert deals_needing_followup(deals, today=TODAY) == ["Singapore", "India"]
 
 
def test_14_day_boundary():
    deals = [deal("Exact", "2026-10-18T00:00:00+00:00"),
             deal("Over", "2026-10-17T23:59:59+00:00")]
    assert deals_needing_followup(deals, today=TODAY) == ["Over"]
 
 
def test_naive_inputs_do_not_crash():
    deals = [deal("Naive", "2026-10-01T09:00:00")]
    assert deals_needing_followup(deals, today=datetime(2026, 11, 1)) == ["Naive"]