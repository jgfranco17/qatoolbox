import os

import pytest
from _pytest.mark.structures import MarkDecorator


def skip_unless_set(env_variable: str) -> MarkDecorator:
    """Skip the test unless the environment variable is set."""
    return pytest.mark.skipif(
        os.getenv(env_variable) is not None,
        reason=f"Skipping test because '{env_variable}' is not set",
    )
