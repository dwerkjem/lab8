from difflib import get_close_matches
from typing import Literal

from lists_.helpers import input_or_arg, yes_or_no

event_types: set[str] = {"wedding", "birthday", "conference"}


def get_event_information(
    event_type: str | None = None,  # Will add to a set
    event_name: str | None = None,
    guest_count: int | None = None,
    estimated_revenue_per_guest: int | None = None,
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


if __name__ == "__main__":
    get_event_information()
