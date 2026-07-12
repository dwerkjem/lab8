"""Collect event details and classify the dates in an event range."""

import datetime
from collections.abc import Container
from difflib import get_close_matches
from typing import cast

import holidays

from lists_.helpers import input_or_arg, yes_or_no
from lists_.models import Catering, DayState, EventRecord

event_types: set[str] = set()


def match_substring(value: str, options: tuple[str, ...]) -> str | None:
    """Return the one option containing value, or None when it is ambiguous."""
    if value in options:
        return value

    matches = [option for option in options if value and value in option]

    if len(matches) == 1:
        return matches[0]

    return None


def count_day_states(
    start_date: datetime.date,
    end_date: datetime.date,
    holiday_calendar: Container[datetime.date] | None = None,
) -> dict[DayState, int]:
    """Count weekdays, weekends, holidays, and combined days in a date range."""
    if end_date < start_date:
        raise ValueError("The end date cannot be before the start date.")

    if holiday_calendar is None:
        holiday_calendar = holidays.US(
            years=range(start_date.year, end_date.year + 1),
            observed=True,
        )

    day_state_counts = {state: 0 for state in DayState}
    current_date = start_date

    while current_date <= end_date:
        is_weekend = current_date.weekday() >= 5
        is_holiday = current_date in holiday_calendar

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

    return day_state_counts


def get_event_information(
    event_type: str | None = None,
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
        event_type_value = str(
            input_or_arg(event_type, "What is the event type: ")
        ).strip().lower()

        if not event_type_value:
            print("Invalid event type. Please enter an event type.")
            event_type = None

    if event_type_value not in event_types:
        matches = get_close_matches(event_type_value, sorted(event_types), n=2)

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

    day_state_counts = count_day_states(start_date_value, end_date_value)
    catering_value: Catering | None = None
    catering_options = ("none", "standard", "premium")

    while catering_value is None:
        catering_input = str(
            input_or_arg(
                catering,
                "Choose a catering option [none, standard, premium]: ",
            )
        ).strip().lower()
        catering_match = match_substring(catering_input, catering_options)

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
        deposit_input = str(
            input_or_arg(
                deposit_status,
                "Has the required deposit been paid? [Yes/No]: ",
            )
        ).strip().lower()
        deposit_match = match_substring(deposit_input, ("yes", "no"))

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
