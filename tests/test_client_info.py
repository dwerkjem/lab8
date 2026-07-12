"""Tests for client information and event-code generation."""

import pytest

from lists_.client_info import generate_event_code, get_client_information


def test_get_client_information_formats_valid_values() -> None:
    """Client names use title case and emails use lowercase."""
    assert get_client_information("deReK neilson", "DEREK@example.com") == (
        "Derek Neilson",
        "derek@example.com",
    )


@pytest.mark.parametrize(
    "email",
    ["derekgmailcom", "derek@gmailcom", "derekgmail.com"],
)
def test_get_client_information_rejects_invalid_email(email: str) -> None:
    """An email argument must contain both an at sign and a domain dot."""
    with pytest.raises(ValueError, match="Email must contain both '@' and '.'."):
        get_client_information("Derek", email)


def test_generate_event_code_resolves_collisions() -> None:
    """Repeated base codes receive increasing numeric suffixes."""
    existing_codes: list[str] = []

    for _ in range(5):
        existing_codes.append(
            generate_event_code("Derek Neilson", "Wedding", existing_codes)
        )

    assert existing_codes == [
        "WED-NEI",
        "WED-NEI-2",
        "WED-NEI-3",
        "WED-NEI-4",
        "WED-NEI-5",
    ]
