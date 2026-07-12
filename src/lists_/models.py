"""Shared types and enumerations for Fountain View Hall bookings."""

from enum import Enum, IntEnum, auto
from typing import Literal

Catering = Literal["premium", "standard", "none"]
EventRecord = list[object]


class BookingDeniedError(Exception):
    """Represent a booking rejected for violating a business rule."""


class DayState(Enum):
    """Represent the possible classifications of a calendar day."""

    NONE = auto()
    WEEKEND = auto()
    HOLIDAY = auto()
    WEEKEND_AND_HOLIDAY = auto()


class EventField(IntEnum):
    """Name each position in an event record while keeping records as lists."""

    CODE = 0
    CLIENT_NAME = 1
    CLIENT_EMAIL = 2
    EVENT_NAME = 3
    EVENT_TYPE = 4
    GUEST_COUNT = 5
    REVENUE_PER_GUEST = 6
    START_DATE = 7
    END_DATE = 8
    DAY_STATE_COUNTS = 9
    CATERING = 10
    DEPOSIT_PAID = 11
    SUBTOTAL = 12
    WEEKEND_FEE = 13
    PREMIUM_CATERING_FEE = 14
    WEDDING_CLEANUP_FEE = 15
    DISCOUNT = 16
    FINAL_CHARGE = 17
    DEPOSIT_REQUIRED = 18
    STATUS = 19
