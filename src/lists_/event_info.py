from difflib import get_close_matches
from typing import Literal

import datetime
import holidays
from lists_.helpers import input_or_arg, yes_or_no
from enum import Enum, auto

event_types: set[str] = set()


class DayState(
    Enum
):  # Safer than a string because it restricts the value to a known set of named options
    # Equivalent Literal code could be used but I think this is cleaner
    """Represent the possible classifications of a calendar day."""

    NONE = auto()  #                  1 `auto` auto enumerates
    WEEKEND = auto()  #               2
    HOLIDAY = auto()  #               3
    WEEKEND_AND_HOLIDAY = auto()  #   4


def get_event_information(
    event_type: str | None = None,  # Will add to a set
    event_name: str | None = None,
    guest_count: int | None = None,
    estimated_revenue_per_guest: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    catering: Literal["premium", "standard", "none"] | None = None,
    deposit_status: str | None = None,
) -> None:

    event_type = (
        str(input_or_arg(event_type, "What is the event type: ")).strip().lower()
    )

    if event_type not in event_types:
        matches = get_close_matches(
            event_type,
            sorted(event_types),
            n=2,  # Upper limit for matches
        )

        for match in matches:
            if yes_or_no(f'Did you mean "{match}"? [Yes/No]: '):
                event_type = match
                break
        else:
            should_add = yes_or_no(
                f'Would you like to add "{event_type}" '
                "to the list of event types? [Yes/No]: "
            )

            if not should_add:
                return

    event_types.add(event_type)

    event_name = (
        str(input_or_arg(event_name, "What is the event name: ")).strip().title()
    )
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

        except ValueError:
            print("Invalid input. Please enter a positive whole number.")
            guest_count = None

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
                "Invalid date. The end date must use YYYY-MM-DD and cannot be before the start date."
            )
            end_date = None
            end_date_value = None

    us_holidays = holidays.US(
        years=range(start_date_value.year, end_date_value.year + 1),
        observed=True,
    )

    day_state_counts: dict[DayState, int] = {
        state: 0 for state in DayState  # dictatory comprehension with 0 as values
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

    catering_value = None

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

        if catering_input == "none":
            catering_value = "none"
        elif catering_input == "standard":
            catering_value = "standard"
        elif catering_input == "premium":
            catering_value = "premium"
        else:
            print(
                "Invalid catering option. " "Please enter none, standard, or premium."
            )
            catering = None


if __name__ == "__main__":
    get_event_information()
