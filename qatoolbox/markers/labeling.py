import functools
import os
import sys
from typing import Any, Callable, Optional, TypeVar

import pytest

from qatoolbox.internal.errors import ToolboxInvalidTestError
from qatoolbox.internal.utils import is_running_in_ci

TestFunction = TypeVar("TestFunction", bound=Callable[..., Any])


def requirement(
    testcase_id: str,
    *,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    component: Optional[str] = None,
) -> Callable:
    """Decorator to assign unique test case IDs with optional metadata.

    This decorator stores test case metadata and prints it during test execution.
    It avoids pytest marker complexity by using a simple function wrapper approach.

    Args:
        testcase_id: Unique identifier for the test case (e.g., "TC001", "USER_LOGIN_001")
        description: Optional human-readable description of the test
        priority: Optional priority level (e.g., "high", "medium", "low", "critical")
        component: Optional component/module being tested

    Returns:
        Decorator function that wraps the test function with metadata printing
    """
    if not isinstance(testcase_id, str) or not testcase_id.strip():
        raise ToolboxInvalidTestError("Test case ID must be a non-empty string")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Internal decorator function that wraps the test with metadata printing.

        Args:
            func (TestFunction): Base test function

        Returns:
            TestFunction: Wrapped test function that prints metadata
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n{'='*60}")
            print(f"TEST CASE: {testcase_id}")
            print(f"{'='*60}")

            if description:
                print(f"Description: {description}")
            if priority:
                print(f"Priority: {priority}")
            if component:
                print(f"Component: {component}")

            print(f"Function: {func.__name__}")
            print(f"Module: {func.__module__}")
            print(f"{'='*60}\n")

            # Execute the original function
            return func(*args, **kwargs)

        # Store metadata as attributes for potential future use
        wrapper._qatoolbox_metadata = {  # type: ignore
            "testcase_id": testcase_id,
            "description": description,
            "priority": priority,
            "component": component,
        }

        return wrapper

    return decorator
