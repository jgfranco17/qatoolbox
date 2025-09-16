import os


def is_running_in_ci() -> bool:
    """Check if the tests are running in a CI environment."""
    env_vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI"]
    return any(os.getenv(var) for var in env_vars)
