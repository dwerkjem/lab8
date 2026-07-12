"""Shared fixtures for Fountain View Hall tests."""

import pytest

from lists_.event_info import event_types
from lists_.records import event_records


@pytest.fixture(autouse=True)
def clear_stored_data() -> None:
    """Prevent one test's records and event types from affecting another."""
    event_records.clear()
    event_types.clear()
