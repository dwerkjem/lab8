"""Tests for event input choices and date classification."""

import datetime

from lists_ import event_info
from lists_.models import DayState


def test_match_substring_accepts_only_unambiguous_values() -> None:
    """Partial catering input resolves only when it has one possible match."""
    options = ("none", "standard", "premium")

    assert event_info.match_substring("prem", options) == "premium"
    assert event_info.match_substring("stand", options) == "standard"
    assert event_info.match_substring("n", options) is None


def test_count_day_states_handles_weekend_holiday_overlap() -> None:
    """A holiday on Saturday is counted as both weekend and holiday."""
    counts = event_info.count_day_states(
        datetime.date(2026, 7, 3),
        datetime.date(2026, 7, 5),
        {datetime.date(2026, 7, 4)},
    )

    assert counts == {
        DayState.NONE: 1,
        DayState.WEEKEND: 1,
        DayState.HOLIDAY: 0,
        DayState.WEEKEND_AND_HOLIDAY: 1,
    }


def test_get_event_information_accepts_partial_catering(monkeypatch) -> None:
    """Validated event data is returned as a list with formatted values."""
    monkeypatch.setattr(event_info, "yes_or_no", lambda prompt: True)

    event = event_info.get_event_information(
        event_type="wedding",
        event_name="summer wedding",
        guest_count=60,
        estimated_revenue_per_guest=45.50,
        start_date="2030-07-05",
        end_date="2030-07-07",
        catering="prem",
        deposit_status="yes",
    )

    assert event is not None
    assert event[0] == "Summer Wedding"
    assert event[1] == "Wedding"
    assert event[2] == 60
    assert event[7] == "premium"
    assert event[8] is True
