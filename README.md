# Lists

**Student:** Derek R. Neilson  
**Course:** Programming 1  
**Lab:** Lab 8 — Lists lab 8

Practicing lists and meeting or exceeding the requirements in the requirements document.

## Project structure

- `src/lists_/client_info.py` collects client details and creates event codes.
- `src/lists_/event_info.py` validates event input and classifies event dates.
- `src/lists_/pricing.py` calculates charges, deposits, and booking status.
- `src/lists_/records.py` stores, displays, searches, and summarizes records.
- `src/lists_/models.py` defines shared types, exceptions, and enumerations.
- `src/lists_/constants.py` contains the documented business-rule values.
- `src/lists_/main.py` coordinates the interactive program.
- `src/lists_/helpers.py` contains reusable input helpers.

The test files follow the same module boundaries so failures are easy to locate.

## Set up the project

```bash
git init
uv sync --dev
uv run pre-commit install
```

## Run the project

```bash
uv run lists
```

You can also run the package directly:

```bash
uv run python -m lists_
```

## Run the tests

```bash
uv run pytest
```

## Format the code

```bash
uv run black .
uv run pre-commit run --all-files
```

The pre-commit hook only formats Python files with Black. It does not lint the
code or enforce additional style rules.

## Assignment requirements

See `docs/percived-requirments.md` for the cumulative Fountain View Hall requirements.
