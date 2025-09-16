from typing import Iterator

import pytest
from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def non_ci_environment(monkeypatch: MonkeyPatch) -> Iterator[None]:
    """Mock non-CI environment variables.

    This fixture mocks non-CI environment variables since the
    tests themselves will need to run in a CI environment.
    For tests involving CI-specific functionality, the environment
    variables should be set with monkeypatch in the test itself.
    """
    for var in ("CI", "GITHUB_ACTIONS", "GITLAB_CI"):
        monkeypatch.delenv(var, raising=False)

    yield
