import pytest
from pytest import MonkeyPatch

from qatoolbox.markers.labeling import requirement
from tests.integration.utils import skip_unless_set


class TestUserAuthentication:
    """Example test class demonstrating marker usage."""

    @skip_unless_set("RUN_INTEGRATION")
    @requirement("AUTH-001", priority="critical", component="authentication")
    def test_user_login_success(self):
        """Test successful user login."""
        # Simulate login logic
        username = "testuser"
        password = "testpass"  # pragma: allowlist secret
        assert username == "testuser"
        assert password == "testpass"  # pragma: allowlist secret

    @requirement("AUTH-002", priority="high", component="authentication")
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        username = "testuser"
        password = "wrongpass"  # pragma: allowlist secret

        # In a real test, you would verify that login fails
        assert username == "testuser"
        assert password != "testpass"  # pragma: allowlist secret

    @requirement("AUTH-003", priority="medium", component="authentication")
    def test_user_logout(self):
        """Test user logout functionality."""
        user_session = {"user_id": 123, "logged_in": True}
        assert user_session["logged_in"] is True


class TestPaymentProcessing:
    """Example test class for payment functionality."""

    @requirement("PAY-001", priority="critical", component="payment")
    def test_payment_success(self):
        """Test successful payment processing."""
        amount = 100.00
        currency = "USD"

        # In a real test, you would call your payment processing function
        assert amount > 0
        assert currency == "USD"

    @requirement("PAY-002", priority="high", component="payment")
    def test_payment_insufficient_funds(self):
        """Test payment with insufficient funds."""
        amount = 1000.00
        available_balance = 50.00

        # In a real test, you would verify that payment fails
        assert amount > available_balance

    @requirement("PAY-003", priority="medium", component="payment")
    def test_payment_refund(self):
        """Test payment refund functionality."""
        original_amount = 100.00
        refund_amount = 50.00

        # In a real test, you would call your refund function
        assert refund_amount <= original_amount


class TestDataValidation:
    """Example test class for data validation."""

    @requirement("DATA-001", priority="high", component="validation")
    def test_email_validation(self):
        """Test email address validation."""
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "user+tag@example.org",
        ]

        for email in valid_emails:
            # In a real test, you would call your email validation function
            assert "@" in email
            assert "." in email.split("@")[1]


# Example of using markers with pytest parametrize
@pytest.mark.parametrize(
    "test_case,expected",
    [
        ("TC-001", "success"),
        ("TC-002", "failure"),
        ("TC-003", "pending"),
    ],
)
@requirement("PARAM-001", priority="low", component="parametrized")
def test_parametrized_with_markers(test_case, expected):
    """Test showing how markers work with parametrized tests."""
    # Each parametrized test will have the same markers applied
    assert test_case.startswith("TC-")
    assert expected in ["success", "failure", "pending"]


# Example of using markers with pytest fixtures
@requirement("FIXTURE-001", priority="medium", component="fixtures")
def test_with_fixtures(monkeypatch):
    """Test showing how markers work with pytest fixtures."""
    # Set up test environment
    monkeypatch.setenv("TEST_MODE", "true")

    # Verify the environment variable was set
    import os

    assert os.getenv("TEST_MODE") == "true"


# Example of using markers with pytest skip/xfail
@pytest.mark.skip(reason="Feature not implemented yet")
@requirement("SKIP-001", priority="low", component="skipped")
def test_skipped_with_markers():
    """Test that is skipped but still has markers applied."""
    assert False  # This won't run due to skip


@pytest.mark.xfail(reason="Known issue to be fixed")
@requirement("XFAIL-001", priority="medium", component="xfail")
def test_xfail_with_markers():
    """Test that is expected to fail but still has markers applied."""
    assert False  # This will fail as expected
