[private]
default:
	@just --list

# setup virtual environment
devel:
	@uv sync --frozen

# tidy everything with ruff
[group("Analysis/Fixing")]
tidy:
	@uv run --frozen ruff check --fix

# initialise the database, &c.
init:
	@uv run thirdplace-tool initdb

# run dev server
dev-server:
	@uv run thirdplace-tool run

# clean up any caches or temporary files and directories
clean:
	@rm -rf .mypy_cache .pytest_cache .ruff_cache .venv dist htmlcov .coverage
	@find . -name \*.orig -delete

# run the test suite
[group("Testing")]
tests:
	@uv run --frozen pytest

# run the typechecker
typecheck:
	@uv run --frozen mypy src
