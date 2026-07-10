# Collections

**Student:** Derek R. Neilson  
**Course:** Programming 1  
**Lab:** Lab 8 — Collections lab 8

Practicing collections and meeting or exceeding the requirements in the requirements document.

## Set up the project

```bash
git init
uv sync --dev
uv run pre-commit install
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

- [ ] Add the assignment requirements here.
- [ ] Replace the placeholder function in `src/collections/__init__.py`.
- [ ] Replace the placeholder test and add tests for every requirement.
- [ ] Complete the pseudocode and integrity statement in `docs/`.
