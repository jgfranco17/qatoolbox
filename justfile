# project - Justfile utility

# Print list of available recipe (this)
_default:
    @just --list --unsorted

# Install dependencies with UV
install:
    uv venv --clear
    uv sync --all-extras --dev
    @echo "Installed dependencies!"

# Run the CLI tool with Poetry
codexa *ARGS:
    @uv run codexa {{ ARGS }}

# Build Docker image
docker-build:
    docker build -t codexa:0.0.0 .

# Run CLI through Docker
docker-run *ARGS:
    docker run --rm codexa:0.0.0 {{ ARGS }}

# Run pytest via uv
pytest *ARGS:
    uv run pytest {{ ARGS }}

# Run test coverage
coverage:
    uv run coverage run --source=codexa --omit="*/__*.py,*/test_*.py,/tmp/*" -m pytest
    uv run coverage report -m
