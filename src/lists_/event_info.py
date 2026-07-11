from typing import Literal
from lists_.helpers import input_or_arg
import datetime


def get_event_information(
    event_type: str | None = None,  # Will add to a set
    event_name: str | None = None,
    guest_count: (
        int | None
    ) = None,  # Note Because of how we set up `input_or_arg` it can take any type
    estimated_revenue_per_guest: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    catering: Literal["premium", "standard", "none"] | None = None,
    deposit_status: str | None = None,
):
    event_types: set[str] = {}
    event_type = str(input_or_arg(event_type))


if __name__ == "__main__":
    get_event_information()
