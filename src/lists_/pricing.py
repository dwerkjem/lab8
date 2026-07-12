"""Calculate event charges, deposits, and booking status."""

from lists_.constants import (
    DEPOSIT_PERCENT,
    LARGE_GUEST_AMOUNT,
    LARGE_GUEST_DISCOUNT_PERCENT,
    MANAGER_APPROVAL_GUEST_AMOUNT,
    PREMIUM_CATERING_FEE_PER_GUEST,
    WEEKEND_SURCHARGE_PER_DAY,
    WEDDING_CLEANUP_FEE,
)
from lists_.models import BookingDeniedError, Catering, DayState


def calculate_event_charge(
    event_type: str,
    guest_count: int,
    estimated_revenue_per_guest: float,
    day_state_counts: dict[DayState, int],
    catering: Catering,
) -> tuple[float, float, float, float, float, float]:
    """Calculate the subtotal, fees, discount, and final event charge."""
    subtotal = round(guest_count * estimated_revenue_per_guest, 2)
    weekend_days = (
        day_state_counts[DayState.WEEKEND]
        + day_state_counts[DayState.WEEKEND_AND_HOLIDAY]
    )
    weekend_fee = round(weekend_days * WEEKEND_SURCHARGE_PER_DAY, 2)
    premium_catering_fee = 0.0

    if catering == "premium":
        premium_catering_fee = round(
            guest_count * PREMIUM_CATERING_FEE_PER_GUEST,
            2,
        )

    wedding_cleanup_fee = 0.0

    if "wedding" in event_type.lower():
        wedding_cleanup_fee = WEDDING_CLEANUP_FEE

    charge_before_discount = round(
        subtotal + weekend_fee + premium_catering_fee + wedding_cleanup_fee,
        2,
    )
    discount = 0.0

    if guest_count >= LARGE_GUEST_AMOUNT:
        discount = round(
            charge_before_discount * (1 - LARGE_GUEST_DISCOUNT_PERCENT),
            2,
        )

    final_charge = round(charge_before_discount - discount, 2)

    return (
        subtotal,
        weekend_fee,
        premium_catering_fee,
        wedding_cleanup_fee,
        discount,
        final_charge,
    )


def calculate_deposit(final_charge: float) -> float:
    """Calculate the deposit required for an event."""
    return round(final_charge * DEPOSIT_PERCENT, 2)


def determine_booking_status(deposit_paid: bool, guest_count: int) -> str:
    """Return the approval status or raise when the deposit rule is violated."""
    if not deposit_paid:
        raise BookingDeniedError("Denied: deposit has not been paid")
    elif guest_count > MANAGER_APPROVAL_GUEST_AMOUNT:
        return "Pending manager approval"
    else:
        return "Approved"
