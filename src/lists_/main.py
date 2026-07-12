"""Coordinate the Fountain View Hall event-booking workflow."""

from typing import cast

from lists_.client_info import generate_event_code, get_client_information
from lists_.event_info import get_event_information
from lists_.helpers import yes_or_no
from lists_.models import BookingDeniedError, Catering, DayState, EventRecord
from lists_.pricing import (
    calculate_deposit,
    calculate_event_charge,
    determine_booking_status,
)
from lists_.records import (
    calculate_statistics,
    display_all_records,
    display_reservation_summary,
    event_records,
    existing_event_codes,
    search_records,
)


def main() -> None:
    """Collect multiple bookings, display results, and allow searches."""
    while True:
        client_name_input = input(
            "Enter the client's full name, or done to finish: "
        ).strip()

        if client_name_input.casefold() == "done":
            break

        client_name, client_email = get_client_information(
            client_name=client_name_input
        )
        event_information = get_event_information()

        if event_information is None:
            continue

        (
            event_name,
            event_type,
            guest_count,
            estimated_revenue_per_guest,
            start_date,
            end_date,
            day_state_counts,
            catering,
            deposit_paid,
        ) = event_information

        (
            subtotal,
            weekend_fee,
            premium_catering_fee,
            wedding_cleanup_fee,
            discount,
            final_charge,
        ) = calculate_event_charge(
            str(event_type),
            int(guest_count),
            float(estimated_revenue_per_guest),
            cast(dict[DayState, int], day_state_counts),
            cast(Catering, catering),
        )
        deposit_required = calculate_deposit(final_charge)

        try:
            status = determine_booking_status(
                bool(deposit_paid),
                int(guest_count),
            )
        except BookingDeniedError as error:
            status = str(error)

        event_code = generate_event_code(
            client_name,
            str(event_type),
            existing_event_codes(),
        )
        record: EventRecord = [
            event_code,
            client_name,
            client_email,
            event_name,
            event_type,
            guest_count,
            estimated_revenue_per_guest,
            start_date,
            end_date,
            day_state_counts,
            catering,
            deposit_paid,
            subtotal,
            weekend_fee,
            premium_catering_fee,
            wedding_cleanup_fee,
            discount,
            final_charge,
            deposit_required,
            status,
        ]
        event_records.append(record)
        print(f"\nBooking decision: {status}")
        display_reservation_summary(record)

    display_all_records()
    calculate_statistics()

    while event_records and yes_or_no(
        "Would you like to search the event records? [Yes/No]: "
    ):
        matching_records = search_records()

        if matching_records:
            print("Matching event records found:")
            for record in matching_records:
                display_reservation_summary(record)
        else:
            print("No matching event records were found.")
