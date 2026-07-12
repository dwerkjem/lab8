"""
Name: Derek R. Neilson
Description: Helper functions for my project
"""

from typing import TypeVar
import os

T = TypeVar(
    "T"
)  # "T" can be any type. Note this is purely for stylistic and type hinting purposes


def input_or_arg(argument: T | None, prompt: str) -> T | str:
    """Return the supplied argument or prompt the user when it is None."""
    if argument is not None:
        return argument

    return input(prompt)


def yes_or_no(prompt: str, value: bool | None = None) -> bool:
    """
    Return the supplied Boolean, or ask the user for a yes-or-no response.

    Args:
        prompt: The message displayed when requesting input.
        value: A Boolean value. When None, the user is prompted.

    Returns:
        True for yes and False for no.

    Raises:
        TypeError: If value is not a Boolean or None.
    """
    if isinstance(
        value, bool
    ):  # `isinstance(value, bool)` checks whether value is a Boolean preferred over `type()` because it respects inheritance.
        return value

    if value is not None:
        raise TypeError("value must be a Boolean or None")

    while True:
        response = input(prompt).strip().lower()

        if response in ("yes", "y"):
            return True

        if response in ("no", "n"):
            return False

        print("Please enter yes or no.")


terminal_width = os.get_terminal_size().columns
