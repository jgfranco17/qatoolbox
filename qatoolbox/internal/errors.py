class TestError(Exception):
    """Base class for test errors."""


class TestInvalid(TestError):
    """Test was improperly configured or executed."""


class TestFailed(TestError):
    """Test failed due to an unexpected error."""
