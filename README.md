# QA Toolbox

A collection of utility functions and decorators to enhance `pytest` testing
with better organization, conditional test execution, and test identification.

## Installation

```bash
pip install qa-toolbox
```

## Usage

### Decorators

#### `requirement`

Decorator to assign unique test case IDs with optional metadata.

This decorator adds structured test identification that enables:

- Running specific tests by ID using pytest markers
- Test case tracking and reporting
- Integration with test management systems
- Organized test categorization

```python
from qatoolbox.markers import requirement


@requirement(
    "TC001", description="This is my test case", priority="high", component="auth"
)
def test_login():
    # Test implementation
    assert some_value == expected_value, "Test failed"
```
