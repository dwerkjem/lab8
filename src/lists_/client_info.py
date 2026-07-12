"""Collect client information and generate unique event codes."""

from lists_.helpers import input_or_arg


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

    email_was_argument = client_email is not None
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
        elif email_was_argument:
            raise ValueError("Email must contain both '@' and '.'.")
        else:
            print("Invalid email. The address must contain one @ and a domain.")
            client_email = None

    return client_name_value.title(), client_email_value


def generate_event_code(
    client_name: str,
    event_type: str,
    existing_codes: list[str] | None = None,
) -> str:
    """Generate an uppercase event code and resolve collisions with a suffix."""
    if existing_codes is None:
        existing_codes = []

    client_last_name = client_name.split()[-1]
    base_code = f"{event_type[:3]}-{client_last_name[:3]}".upper()
    candidate = base_code
    suffix = 2

    while candidate in existing_codes:
        candidate = f"{base_code}-{suffix}"
        suffix += 1

    return candidate
