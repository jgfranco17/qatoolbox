import pytest
from pytest import MonkeyPatch

from qatoolbox.internal.utils import is_running_in_ci


@pytest.mark.parametrize(
    "env_variable",
    [
        "CI",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
    ],
)
def test_is_running_in_ci(monkeypatch: MonkeyPatch, env_variable: str):
    monkeypatch.setenv(env_variable, "true")
    check_if_ci = is_running_in_ci()
    assert check_if_ci is True
