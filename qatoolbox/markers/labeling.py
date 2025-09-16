import functools
import os
import sys
from typing import Any, Callable, Optional, TypeVar

import pytest

from qatoolbox.internal.errors import TestInvalid
from qatoolbox.internal.utils import is_running_in_ci

TestFunction = TypeVar("TestFunction", bound=Callable[..., Any])


def requirement(
    testcase_id: str,
    *,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    component: Optional[str] = None,
) -> Callable[[TestFunction], TestFunction]:
    """Decorator to assign unique test case IDs with optional metadata.

    This decorator adds structured test identification that enables:
    - Running specific tests by ID using pytest markers
    - Test case tracking and reporting
    - Integration with test management systems
    - Organized test categorization

    Args:
        test_id: Unique identifier for the test case (e.g., "TC001", "USER_LOGIN_001")
        description: Optional human-readable description of the test
        priority: Optional priority level (e.g., "high", "medium", "low", "critical")
        component: Optional component/module being tested

    Returns:
        Decorator function that applies pytest markers for test identification
    """
    if not isinstance(testcase_id, str) or not testcase_id.strip():
        raise TestInvalid("Test case ID must be a non-empty string")

    sanitized_id = testcase_id.replace("-", "_").replace(" ", "_")

    def decorator(func: TestFunction) -> TestFunction:
        """Internal decorator function that applies pytest markers.

        Args:
            func (TestFunction): Base test function

        Returns:
            TestFunction: Modified test function
        """
        func = pytest.mark.test_id(testcase_id)(func)
        func = getattr(pytest.mark, f"id_{sanitized_id}")(func)

        if priority:
            func = pytest.mark.priority(priority)(func)
            func = getattr(pytest.mark, f"priority_{priority}")(func)

        if component:
            func = pytest.mark.component(component)(func)
            func = getattr(pytest.mark, f"component_{component}")(func)

        return func

    return decorator
