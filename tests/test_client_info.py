from lists_ import client_info
import pytest


def test_generate_event_code() -> None:
    event_code = client_info.generate_event_code
    assert event_code("Colter", "Wedding") == "WED-COL"
    list_of_codes = []
    list_of_codes.append(event_code("Colter", "Wedding", list_of_codes))
    list_of_codes.append(event_code("Colter", "Wedding", list_of_codes))
    list_of_codes.append(event_code("Colter", "Wedding", list_of_codes))
    list_of_codes.append(event_code("Coleen", "Wedding", list_of_codes))
    list_of_codes.append(event_code("Colin", "Wedding ceremony", list_of_codes))
    assert "WED-COL-1" not in list_of_codes
    assert "WED-COL-2" in list_of_codes
    assert "WED-COL-3" in list_of_codes
    assert "WED-COL-4" in list_of_codes
    assert "WED-COL-5" in list_of_codes
    assert len(list_of_codes) == 5


def test_get_client_information() -> None:
    client_inf = client_info.get_client_information
    assert client_inf("deReK", "derekRneilson@gmail.com") == (
        "Derek",
        "derekrneilson@gmail.com",
    )
    with pytest.raises(ValueError, match="Email must contain both '@' and '.'."):
        client_inf("deReK", "derekRneilsongmailcom")
    with pytest.raises(ValueError, match="Email must contain both '@' and '.'."):
        client_inf("deReK", "derekRneilson@gmailcom")
    with pytest.raises(ValueError, match="Email must contain both '@' and '.'."):
        client_inf("deReK", "derekRneilsongmail.com")
