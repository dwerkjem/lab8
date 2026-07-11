from typing import TypeVar

T = TypeVar(
    "T"
)  # "T" can be any type. Note this is purely for stylistic and type hinting purposes


def input_or_arg(argument: T | None, prompt: str) -> T | str:
    """Return the supplied argument or prompt the user when it is None."""
    if argument is not None:
        return argument

    return input(prompt)
