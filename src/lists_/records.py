"""Store, display, search, and summarize event records."""

from typing import cast

from lists_.helpers import input_or_arg, terminal_width
from lists_.models import DayState, EventField, EventRecord

event_records: list[EventRecord] = []


def existing_event_codes(records: list[EventRecord] | None = None) -> list[str]:
    """Return all event codes currently stored in the provided record list."""
    if records is None:
        records = event_records

    return [str(record[EventField.CODE]) for record in records]


def display_reservation_summary(record: EventRecord) -> None:
    """Display one formatted reservation summary."""
    day_state_counts = cast(
        dict[DayState, int],
        record[EventField.DAY_STATE_COUNTS],
    )
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
{"-" * terminal_width}
Status: {record[EventField.STATUS]}
Event code: {record[EventField.CODE]}
Client: {record[EventField.CLIENT_NAME]} ({record[EventField.CLIENT_EMAIL]})
Event: {record[EventField.EVENT_NAME]} ({record[EventField.EVENT_TYPE]})
Dates: {record[EventField.START_DATE]} through {record[EventField.END_DATE]}
Guests: {record[EventField.GUEST_COUNT]}
Estimated revenue per guest: ${record[EventField.REVENUE_PER_GUEST]:,.2f}
Catering: {str(record[EventField.CATERING]).title()}
Deposit paid: {"Yes" if record[EventField.DEPOSIT_PAID] else "No"}
Weekend days: {weekend_days}
Holiday days: {holiday_days}
Subtotal: ${record[EventField.SUBTOTAL]:,.2f}
Weekend fee: ${record[EventField.WEEKEND_FEE]:,.2f}
Premium-catering fee: ${record[EventField.PREMIUM_CATERING_FEE]:,.2f}
Wedding-cleanup fee: ${record[EventField.WEDDING_CLEANUP_FEE]:,.2f}
Large-event discount: -${record[EventField.DISCOUNT]:,.2f}
Final charge: ${record[EventField.FINAL_CHARGE]:,.2f}
Required deposit: ${record[EventField.DEPOSIT_REQUIRED]:,.2f}
{"-" * terminal_width}
""")


def display_all_records(records: list[EventRecord] | None = None) -> None:
    """Display every stored event record."""
    if records is None:
        records = event_records

    if not records:
        print("No event records were entered.")
        return

    print("\nAll Event Records")

    for record in records:
        display_reservation_summary(record)


def search_records(
    search_value: str | None = None,
    records: list[EventRecord] | None = None,
) -> list[EventRecord]:
    """Search records by event code, client name, or event name."""
    if records is None:
        records = event_records

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
        for record in records
        if search_text in str(record[EventField.CODE]).casefold()
        or search_text in str(record[EventField.CLIENT_NAME]).casefold()
        or search_text in str(record[EventField.EVENT_NAME]).casefold()
    ]


def calculate_statistics(
    records: list[EventRecord] | None = None,
) -> dict[str, object] | None:
    """Calculate, display, and return totals and event-size extremes."""
    if records is None:
        records = event_records

    if not records:
        print("No event records are available for statistics.")
        return None

    total_events = 0
    total_guests = 0
    total_revenue = 0.0

    for record in records:
        total_events += 1
        total_guests += int(record[EventField.GUEST_COUNT])
        total_revenue += float(record[EventField.FINAL_CHARGE])

    total_revenue = round(total_revenue, 2)
    average_guests = total_guests / total_events
    largest_event = max(
        records,
        key=lambda record: int(record[EventField.GUEST_COUNT]),
    )
    smallest_event = min(
        records,
        key=lambda record: int(record[EventField.GUEST_COUNT]),
    )
    statistics = {
        "total_events": total_events,
        "total_guests": total_guests,
        "total_revenue": total_revenue,
        "average_guests": average_guests,
        "largest_event": largest_event,
        "smallest_event": smallest_event,
    }
    largest_name = largest_event[EventField.EVENT_NAME]
    largest_guests = largest_event[EventField.GUEST_COUNT]
    smallest_name = smallest_event[EventField.EVENT_NAME]
    smallest_guests = smallest_event[EventField.GUEST_COUNT]

    print(f"""
Event Statistics
{"-" * terminal_width}
Total events: {total_events}
Total guests: {total_guests}
Total revenue: ${total_revenue:,.2f}
Average guests per event: {average_guests:,.2f}
Largest event: {largest_name} ({largest_guests} guests)
Smallest event: {smallest_name} ({smallest_guests} guests)
{"-" * terminal_width}
""")

    return statistics
