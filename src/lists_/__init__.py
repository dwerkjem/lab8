"""

Name: Derek R. Neilson

Description: Fountain View Hall event-booking collection manager

Program Design:
    Information collected:
        Client name and email, event name and type, guest count, estimated
        revenue per guest, start and end dates, catering selection, and
        deposit status.

    Information stored in lists:
        Every collected field, calculated fee, discount, final charge,
        booking status, and generated event code is stored in an event record.

    Lists used:
        The program uses one main list named event_records. Each item in that
        list is another list containing one complete event record.

    Calculations performed:
        Subtotal, weekend surcharge, premium-catering fee, wedding-cleanup
        fee, large-event discount, final charge, required deposit, total
        events, total guests, total revenue, average guests, and the largest
        and smallest events.

    Search options:
        Users can search by client name, event name, or event code.

    Functions used:
        get_client_information(), get_event_information(),
        calculate_event_charge(), calculate_deposit(), generate_event_code(),
        determine_booking_status(), display_reservation_summary(),
        display_all_records(), search_records(), calculate_statistics(),
        and main().

Business-rule assumptions:
    The weekend surcharge is $200 per weekend day. Premium catering costs $15
    per guest. Weddings receive a $250 cleanup fee. A deposit is 25% of the
    final charge. Events with at least 60 guests receive a 20% discount.
    Events exceeding 300 guests require manager approval. No holiday fee is
    charged; holidays are counted and displayed for informational purposes.

"""

import datetime
from difflib import get_close_matches
from enum import Enum, auto
from typing import Literal, cast

import holidays

from lists_.helpers import input_or_arg, yes_or_no

Catering = Literal["premium", "standard", "none"]
EventRecord = list[object]


# The assignment allows reasonable assumptions when a price is not specified.
# These values are documented in the module's Business-rule assumptions.
WEEKEND_SURCHARGE_PER_DAY = 200.00
PREMIUM_CATERING_FEE_PER_GUEST = 15.00
WEDDING_CLEANUP_FEE = 250.00
DEPOSIT_PERCENT = 0.25
LARGE_GUEST_AMOUNT = 60
LARGE_GUEST_DISCOUNT_PERCENT = 0.80
MANAGER_APPROVAL_GUEST_AMOUNT = 300


event_types: set[str] = set()
event_records: list[EventRecord] = []


class BookingDeniedError(Exception):
    """Represent a booking rejected for violating a business rule."""


class DayState(
    Enum
):  # Safer than a string because it restricts the value to a known set of named options
    # Equivalent Literal code could be used but I think this is cleaner
    """Represent the possible classifications of a calendar day."""

    NONE = auto()  #                  1 `auto` auto enumerates
    WEEKEND = auto()  #               2
    HOLIDAY = auto()  #               3
    WEEKEND_AND_HOLIDAY = auto()  #   4


def _match_substring(value: str, options: tuple[str, ...]) -> str | None:
    """Return the one option containing value, or None when it is ambiguous."""
    if value in options:
        return value

    matches = [option for option in options if value and value in option]

    if len(matches) == 1:
        return matches[0]

    return None


def get_client_information(
    client_name: str | None = None,
    client_email: str | None = None,
) -> tuple[str, str]:
    """Collect and validate the client's name and email address."""
    client_name_value = ""

    while not client_name_value:
        client_name_value = str(
            input_or_arg(client_name, "What is the client's full name: ")
        ).strip()

        if not client_name_value:
            print("Invalid name. Please enter the client's full name.")
            client_name = None

    client_email_value = ""

    while not client_email_value:
        possible_email = str(
            input_or_arg(client_email, "What is the client's email address: ")
        ).strip()
        email_parts = possible_email.split("@")

        if (
            len(email_parts) == 2
            and email_parts[0]
            and "." in email_parts[1]
            and not email_parts[1].startswith(".")
            and not email_parts[1].endswith(".")
        ):
            client_email_value = possible_email.lower()
        else:
            print("Invalid email. The address must contain one @ and a domain.")
            client_email = None

    return client_name_value.title(), client_email_value


def get_event_information(
    event_type: str | None = None,  # Will add to a set
    event_name: str | None = None,
    guest_count: int | None = None,
    estimated_revenue_per_guest: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    catering: str | None = None,
    deposit_status: str | None = None,
) -> EventRecord | None:
    """Collect, validate, and return the information for one event."""
    event_type_value = ""

    while not event_type_value:
        event_type_value = (
            str(input_or_arg(event_type, "What is the event type: ")).strip().lower()
        )

        if not event_type_value:
            print("Invalid event type. Please enter an event type.")
            event_type = None

    if event_type_value not in event_types:
        matches = get_close_matches(
            event_type_value,
            sorted(event_types),
            n=2,  # Upper limit for matches
        )

        for match in matches:
            if yes_or_no(f'Did you mean "{match}"? [Yes/No]: '):
                event_type_value = match
                break
        else:
            should_add = yes_or_no(
                f'Would you like to add "{event_type_value}" '
                "to the list of event types? [Yes/No]: "
            )

            if not should_add:
                return None

    event_types.add(event_type_value)

    event_name_value = ""

    while not event_name_value:
        event_name_value = str(
            input_or_arg(event_name, "What is the event name: ")
        ).strip()

        if not event_name_value:
            print("Invalid event name. Please enter a name.")
            event_name = None

    event_name_value = event_name_value.title()
    guest_count_value = None

    while guest_count_value is None:
        try:
            guest_count_value = int(
                input_or_arg(
                    guest_count,
                    "How many guests are attending? Example [65]: ",
                )
            )

            if guest_count_value < 1:
                raise ValueError

        except (ValueError, TypeError):
            print("Invalid input. Please enter a positive whole number.")
            guest_count = None
            guest_count_value = None

    estimated_revenue_value = None

    while estimated_revenue_value is None:
        try:
            estimated_revenue_value = float(
                input_or_arg(
                    estimated_revenue_per_guest,
                    "What is the estimated revenue per guest? Example [45.50]: ",
                )
            )

            if estimated_revenue_value < 0:
                raise ValueError

        except (ValueError, TypeError):
            print("Invalid input. Please enter a positive number.")
            estimated_revenue_per_guest = None
            estimated_revenue_value = None

    start_date_value = None

    while start_date_value is None:
        try:
            start_date_value = datetime.datetime.strptime(
                str(
                    input_or_arg(
                        start_date,
                        "What is the start date? Example [2026-07-11]: ",
                    )
                ).strip(),
                "%Y-%m-%d",
            ).date()

            if start_date_value < datetime.date.today():
                raise ValueError("The start date cannot be in the past.")

        except (ValueError, TypeError) as error:
            print(f"Invalid date. {error}")
            start_date = None
            start_date_value = None

    end_date_value = None

    while end_date_value is None:
        try:
            end_date_value = datetime.datetime.strptime(
                str(
                    input_or_arg(
                        end_date,
                        "What is the end date? Example [2026-07-13]: ",
                    )
                ).strip(),
                "%Y-%m-%d",
            ).date()

            if end_date_value < start_date_value:
                raise ValueError

        except (ValueError, TypeError):
            print(
                "Invalid date. The end date must use YYYY-MM-DD and cannot "
                "be before the start date."
            )
            end_date = None
            end_date_value = None

    us_holidays = holidays.US(
        years=range(start_date_value.year, end_date_value.year + 1),
        observed=True,
    )

    day_state_counts: dict[DayState, int] = {
        state: 0 for state in DayState  # dictionary comprehension with 0 as values
    }

    current_date = start_date_value

    while current_date <= end_date_value:
        is_weekend = current_date.weekday() >= 5
        is_holiday = current_date in us_holidays

        if is_weekend and is_holiday:
            day_state = DayState.WEEKEND_AND_HOLIDAY
        elif is_weekend:
            day_state = DayState.WEEKEND
        elif is_holiday:
            day_state = DayState.HOLIDAY
        else:
            day_state = DayState.NONE

        day_state_counts[day_state] += 1
        current_date += datetime.timedelta(days=1)

    catering_value: Catering | None = None
    catering_options = ("none", "standard", "premium")

    while catering_value is None:
        catering_input = (
            str(
                input_or_arg(
                    catering,
                    "Choose a catering option [none, standard, premium]: ",
                )
            )
            .strip()
            .lower()
        )

        catering_match = _match_substring(catering_input, catering_options)

        if catering_match is not None:
            catering_value = cast(Catering, catering_match)
        else:
            print(
                "Invalid or ambiguous catering option. Please enter an "
                "unambiguous part of none, standard, or premium."
            )
            catering = None

    deposit_paid: bool | None = None

    while deposit_paid is None:
        deposit_input = (
            str(
                input_or_arg(
                    deposit_status,
                    "Has the required deposit been paid? [Yes/No]: ",
                )
            )
            .strip()
            .lower()
        )

        deposit_match = _match_substring(deposit_input, ("yes", "no"))

        if deposit_match == "yes":
            deposit_paid = True
        elif deposit_match == "no":
            deposit_paid = False
        else:
            print("Invalid deposit status. Please enter yes or no.")
            deposit_status = None

    return [
        event_name_value,
        event_type_value.title(),
        guest_count_value,
        estimated_revenue_value,
        start_date_value,
        end_date_value,
        day_state_counts,
        catering_value,
        deposit_paid,
    ]


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


def generate_event_code(client_name: str, event_type: str) -> str:
    """Generate a unique event code and resolve collisions with a suffix."""
    client_last_name = client_name.split()[-1]
    base_code = f"{event_type[:3]}-{client_last_name[:3]}".upper()
    existing_codes = {str(record[0]) for record in event_records}

    if base_code not in existing_codes:
        return base_code

    suffix = 2

    while f"{base_code}-{suffix}" in existing_codes:
        suffix += 1

    return f"{base_code}-{suffix}"


def display_reservation_summary(record: EventRecord) -> None:
    """Display one formatted reservation summary."""
    (
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
    ) = record

    weekend_days = (
        day_state_counts[DayState.WEEKEND]
        + day_state_counts[DayState.WEEKEND_AND_HOLIDAY]
    )
    holiday_days = (
        day_state_counts[DayState.HOLIDAY]
        + day_state_counts[DayState.WEEKEND_AND_HOLIDAY]
    )

    print(f"""
Reservation Summary
{"-" * 65}
Status: {status}
Event code: {event_code}
Client: {client_name} ({client_email})
Event: {event_name} ({event_type})
Dates: {start_date} through {end_date}
Guests: {guest_count}
Estimated revenue per guest: ${estimated_revenue_per_guest:,.2f}
Catering: {str(catering).title()}
Deposit paid: {"Yes" if deposit_paid else "No"}
Weekend days: {weekend_days}
Holiday days: {holiday_days}
Subtotal: ${subtotal:,.2f}
Weekend fee: ${weekend_fee:,.2f}
Premium-catering fee: ${premium_catering_fee:,.2f}
Wedding-cleanup fee: ${wedding_cleanup_fee:,.2f}
Large-event discount: -${discount:,.2f}
Final charge: ${final_charge:,.2f}
Required deposit: ${deposit_required:,.2f}
{"-" * 65}
""")


def display_all_records() -> None:
    """Display every event record."""
    if not event_records:
        print("No event records were entered.")
        return

    print("\nAll Event Records")

    for record in event_records:
        display_reservation_summary(record)


def search_records(search_value: str | None = None) -> list[EventRecord]:
    """Search records by event code, client name, or event name."""
    search_text = ""

    while not search_text:
        search_text = (
            str(
                input_or_arg(
                    search_value,
                    "Search by event code, client name, or event name: ",
                )
            )
            .strip()
            .casefold()
        )

        if not search_text:
            print("Invalid search. Please enter a value to search for.")
            search_value = None

    return [
        record
        for record in event_records
        if search_text in str(record[0]).casefold()
        or search_text in str(record[1]).casefold()
        or search_text in str(record[3]).casefold()
    ]


def calculate_statistics() -> None:
    """Calculate and display totals, averages, and event-size extremes."""
    if not event_records:
        print("No event records are available for statistics.")
        return

    total_events = 0  # Counter
    total_guests = 0  # Accumulator
    total_revenue = 0.0  # Accumulator

    for record in event_records:
        total_events += 1
        total_guests += int(record[5])
        total_revenue += float(record[17])

    total_revenue = round(total_revenue, 2)
    average_guests = total_guests / total_events
    largest_event = max(event_records, key=lambda record: int(record[5]))
    smallest_event = min(event_records, key=lambda record: int(record[5]))

    print(f"""
Event Statistics
{"-" * 65}
Total events: {total_events}
Total guests: {total_guests}
Total revenue: ${total_revenue:,.2f}
Average guests per event: {average_guests:,.2f}
Largest event: {largest_event[3]} ({largest_event[5]} guests)
Smallest event: {smallest_event[3]} ({smallest_event[5]} guests)
{"-" * 65}
""")


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

        event_code = generate_event_code(client_name, str(event_type))
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
            for record in matching_records:
                display_reservation_summary(record)
        else:
            print("No matching event records were found.")


if __name__ == "__main__":
    main()
