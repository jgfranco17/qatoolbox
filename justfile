# QA Toolbox: Justfile utility

# Print list of available recipe (this)
_default:
    @just --list --unsorted

# Install dependencies with UV
install:
    uv venv --clear
    uv sync --all-extras --dev
    @echo "Installed dependencies!"

# Run pytest via uv
pytest *ARGS:
    uv run pytest {{ ARGS }}
