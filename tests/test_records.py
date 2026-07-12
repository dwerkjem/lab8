"""Tests for record searching, output, and statistics."""

import datetime

from lists_.models import DayState, EventField, EventRecord
from lists_.records import (
    calculate_statistics,
    display_reservation_summary,
    search_records,
)


def make_record(
    code: str = "WED-NEI",
    client: str = "Derek Neilson",
    event_name: str = "Summer Wedding",
    guests: int = 60,
    final_charge: float = 3424.00,
) -> EventRecord:
    """Create one complete record for reporting tests."""
    day_counts = {state: 0 for state in DayState}

    return [
        code,
        client,
        "derek@example.com",
        event_name,
        "Wedding",
        guests,
        45.50,
        datetime.date(2026, 7, 11),
        datetime.date(2026, 7, 12),
        day_counts,
        "premium",
        True,
        2730.00,
        400.00,
        900.00,
        250.00,
        856.00,
        final_charge,
        856.00,
        "Approved",
    ]


def test_search_records_uses_all_required_fields() -> None:
    """Code, client name, and event name can each find a record."""
    record = make_record()
    records = [record]

    assert search_records("WED-NEI", records) == [record]
    assert search_records("derek", records) == [record]
    assert search_records("summer", records) == [record]
    assert search_records("missing", records) == []


def test_display_reservation_summary_contains_required_output(capsys) -> None:
    """The formatted summary contains identity, choices, status, and charges."""
    display_reservation_summary(make_record())
    output = capsys.readouterr().out

    assert "Status: Approved" in output
    assert "Event code: WED-NEI" in output
    assert "Derek Neilson" in output
    assert "Catering: Premium" in output
    assert "Final charge: $3,424.00" in output


def test_calculate_statistics_returns_totals_and_extremes(capsys) -> None:
    """Statistics use counters and accumulators across stored records."""
    small = make_record("CON-SMI", "Alex Smith", "Conference", 40, 1000.00)
    large = make_record()
    statistics = calculate_statistics([small, large])

    assert statistics is not None
    assert statistics["total_events"] == 2
    assert statistics["total_guests"] == 100
    assert statistics["total_revenue"] == 4424.00
    assert statistics["average_guests"] == 50
    assert statistics["largest_event"][EventField.EVENT_NAME] == "Summer Wedding"
    assert statistics["smallest_event"][EventField.EVENT_NAME] == "Conference"
    assert "Total events: 2" in capsys.readouterr().out
