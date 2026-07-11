"""
Name: Derek R. Neilson
Description: Fountain View Hall event-booking collection manager
"""

from typing import TypeVar

# Q: What information will the program collect?
# A:
# - Client name and email
# - Event name and type
# - Guest count
# - Estimated revenue and pricing information
# - Weekend status
# - Catering package
# - Deposit status


# Q: Which information will be stored in lists?
# A: All information for each event booking will be stored as a record
# inside the event_records list.


# Q: Will the solution require one list or multiple lists?
# A: The program will use one main list named event_records. Each item
# will be another list containing all information for one event.


# Q: What calculations will the program perform?
# A:
# - Calculate each event's subtotal
# - Add weekend, premium-catering, and wedding-cleanup fees
# - Apply large-event discounts
# - Calculate each event's final charge
# - Calculate total events, guests, and revenue
# - Calculate average guests per event
# - Determine the largest and smallest events


# Q: What value will the user be able to search for?
# A: The user will be able to search by event code, client name,
# or event name.


# Q: Which functions will organize the program?
# A:
# - get_client_information()
# - get_event_information()
# - calculate_event_charge()
# - calculate_deposit()
# - generate_event_code()
# - display_reservation_summary()
# - display_all_records()
# - search_records()
# - calculate_statistics()
# - main()
T = TypeVar(
    "T"
)  # "T" can be any type. Note this is purely for stylistic and type hinting purposes


def input_or_arg(argument: T | None, prompt: str) -> T | str:
    """Return the supplied argument or prompt the user when it is None."""
    if argument is not None:
        return argument

    return input(prompt)


def get_client_information(
    client_name: (
        str | None
    ) = None,  # Must use this pattern for thing that would be in input from this point on.
    email: str | None = None,  # See comment above.
) -> tuple[str, str]:
    """Collect and validate the client's name and email address.

    Args:
        client_name (str | None, optional): Client's name. If `None`, the
            user will be prompted for input. Defaults to None.
        email (str | None, optional): Client's email address. If `None`, the
            user will be prompted for input. Defaults to None.

    Raises:
        ValueError: If an email supplied as an argument does not contain
            both an '@' and a '.'.

    Returns:
        tuple[str, str]: The formatted client name and validated email
            address.

    Example:
        >>> get_client_information("derek neilson", "derek@example.com")
        ('Derek Neilson', 'derek@example.com')
    """
    client_name = (
        str(
            input_or_arg(
                client_name, "Enter the client's name: "
            )  # This is how input will be collected usually from this point.
        )
        .strip()
        .title()
    )

    email_was_argument = email is not None
    email = str(input_or_arg(email, "Enter the client's email: ")).strip()

    while "@" not in email or "." not in email:
        if email_was_argument:
            raise ValueError("Email must contain both '@' and '.'.")

        print("Email must contain both '@' and '.'.")
        email = input("Enter a valid email: ").strip()

    return client_name, email


def get_event_information(): ...


def main() -> None:
    """Run the lab program."""
    return None
