"""Tests for the package entry point."""

from lists_ import main


def test_main_stops_on_done(monkeypatch, capsys) -> None:
    """The done sentinel ends entry without requiring a booking."""
    monkeypatch.setattr("builtins.input", lambda prompt: "done")

    assert main() is None
    output = capsys.readouterr().out
    assert "No event records were entered." in output
    assert "No event records are available for statistics." in output
