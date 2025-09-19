class ToolboxBaseError(Exception):
    """Base class for test errors."""


class ToolboxInvalidTestError(ToolboxBaseError):
    """Test was improperly configured or executed."""


class ToolboxFailedTestError(ToolboxBaseError):
    """Test failed due to an unexpected error."""
