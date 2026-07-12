"""Tests for charges, deposits, and booking status."""

import pytest

from lists_.models import BookingDeniedError, DayState
from lists_.pricing import (
    calculate_deposit,
    calculate_event_charge,
    determine_booking_status,
)


def empty_day_counts() -> dict[DayState, int]:
    """Return a zero-filled day-state mapping for pricing tests."""
    return {state: 0 for state in DayState}


def test_normal_event_calculation() -> None:
    """A standard weekday event has no special fees or discount."""
    result = calculate_event_charge(
        "Conference",
        40,
        25.00,
        empty_day_counts(),
        "standard",
    )

    assert result == (1000.00, 0.00, 0.00, 0.00, 0.00, 1000.00)
    assert calculate_deposit(result[-1]) == 250.00


def test_combined_fees_and_large_event_discount() -> None:
    """Weekend, premium, wedding, and large-event rules combine correctly."""
    day_counts = empty_day_counts()
    day_counts[DayState.WEEKEND] = 2

    assert calculate_event_charge(
        "Wedding",
        60,
        45.50,
        day_counts,
        "premium",
    ) == (2730.00, 400.00, 900.00, 250.00, 856.00, 3424.00)


def test_booking_status_boundaries() -> None:
    """Deposit and 300-guest rules approve, deny, or require review."""
    with pytest.raises(BookingDeniedError):
        determine_booking_status(False, 50)

    assert determine_booking_status(True, 300) == "Approved"
    assert determine_booking_status(True, 301) == "Pending manager approval"
