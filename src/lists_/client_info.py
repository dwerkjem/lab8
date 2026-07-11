"""
Name: Derek R. Neilson

Description: Gets all relevant Client info and has a function to display event code
"""

from lists_.helpers import input_or_arg


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

    email_was_argument = (
        email is not None
    )  # To skip re-promoting as it doesn't make sense with a arg
    email = str(input_or_arg(email, "Enter the client's email: ")).strip().lower()

    while "@" not in email or "." not in email:
        if email_was_argument:
            raise ValueError("Email must contain both '@' and '.'.")

        print("Email must contain both '@' and '.'.")
        email = input("Enter a valid email: ").strip()

    return client_name, email


def generate_event_code(
    client_last_name: str,
    event_type: str,
    existing_codes: list[str] = [],
) -> str:
    """Generate an uppercase event code from the first three letters of the event type and client’s last name, such as `WED-JOH`. Note: if it exists to avoid collision it will append `-x` where x is the next  possible increment of the number of collisions

    Args:
        event_type (str): The type of event
        client_last_name (str): The clients name
        existing_codes (list[str], optional): The list of existing codes. Defaults to [].

    Returns:
        str: A unique valid code
    """
    base_code = (f"{event_type[:3]}-{client_last_name[:3]}").upper()

    candidate = base_code
    suffix = 2

    while candidate in existing_codes:
        candidate = f"{base_code}-{suffix}"
        suffix += 1

    return candidate
