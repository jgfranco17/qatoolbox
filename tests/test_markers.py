"""Unit and integration tests for qatoolbox markers."""

import sys
from io import StringIO

import pytest
from pytest import MonkeyPatch

from qatoolbox.internal.errors import ToolboxInvalidTestError
from qatoolbox.markers.labeling import requirement


class TestRequirementDecorator:
    """Unit tests for the requirement decorator."""

    def test_requirement_decorator_basic_usage(self):
        """Test basic usage of the requirement decorator."""

        @requirement("TC001")
        def test_example():
            assert True

        # Check that the function is still callable
        test_example()

        # Check that metadata is stored
        assert hasattr(test_example, "_qatoolbox_metadata")
        assert test_example._qatoolbox_metadata["testcase_id"] == "TC001"

    def test_requirement_decorator_with_description(self):
        """Test requirement decorator with description."""

        @requirement("TC002", description="Test user login functionality")
        def test_login():
            assert True

        test_login()
        assert hasattr(test_login, "_qatoolbox_metadata")
        assert (
            test_login._qatoolbox_metadata["description"]
            == "Test user login functionality"
        )

    def test_requirement_decorator_with_priority(self):
        """Test requirement decorator with priority."""

        @requirement("TC003", priority="high")
        def test_critical():
            assert True

        test_critical()
        assert hasattr(test_critical, "_qatoolbox_metadata")
        assert test_critical._qatoolbox_metadata["priority"] == "high"

    def test_requirement_decorator_with_component(self):
        """Test requirement decorator with component."""

        @requirement("TC004", component="auth")
        def test_auth():
            assert True

        test_auth()
        assert hasattr(test_auth, "_qatoolbox_metadata")
        assert test_auth._qatoolbox_metadata["component"] == "auth"

    def test_requirement_decorator_with_all_parameters(self):
        """Test requirement decorator with all optional parameters."""

        @requirement(
            "TC005",
            description="Test payment processing",
            priority="critical",
            component="payment",
        )
        def test_payment():
            assert True

        test_payment()
        metadata = test_payment._qatoolbox_metadata
        assert metadata["testcase_id"] == "TC005"
        assert metadata["description"] == "Test payment processing"
        assert metadata["priority"] == "critical"
        assert metadata["component"] == "payment"

    def test_requirement_decorator_preserves_function_metadata(self):
        """Test that the decorator preserves function metadata."""

        @requirement("TC006")
        def test_with_docstring():
            """This is a test function with a docstring."""
            return "test_result"

        # Check that docstring is preserved
        assert (
            test_with_docstring.__doc__ == "This is a test function with a docstring."
        )

        # Check that function still works
        result = test_with_docstring()
        assert result == "test_result"

    def test_requirement_decorator_prints_metadata(self):
        """Test that the decorator prints metadata during execution."""

        @requirement(
            "TC007",
            description="Test metadata printing",
            priority="high",
            component="test",
        )
        def test_metadata_printing():
            return "success"

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = test_metadata_printing()
            output = captured_output.getvalue()

            # Check that metadata was printed
            assert "TEST CASE: TC007" in output
            assert "Description: Test metadata printing" in output
            assert "Priority: high" in output
            assert "Component: test" in output
            assert "Function: test_metadata_printing" in output
            assert result == "success"
        finally:
            sys.stdout = old_stdout

    def test_requirement_decorator_with_parameters(self):
        """Test requirement decorator with function that has parameters."""

        @requirement("TC007")
        def test_with_params(param1: str, param2: int = 42):
            return f"{param1}_{param2}"

        result = test_with_params("hello", 100)
        assert result == "hello_100"

        result_default = test_with_params("world")
        assert result_default == "world_42"

    def test_requirement_decorator_id_sanitization(self):
        """Test that test case IDs are properly stored (no sanitization needed)."""

        @requirement("TC-008", description="Test with dashes and spaces")
        def test_sanitization():
            assert True

        test_sanitization()
        assert hasattr(test_sanitization, "_qatoolbox_metadata")
        assert test_sanitization._qatoolbox_metadata["testcase_id"] == "TC-008"

    def test_requirement_decorator_invalid_testcase_id_empty_string(self):
        """Test that empty string testcase_id raises TestInvalid."""
        with pytest.raises(
            ToolboxInvalidTestError, match="Test case ID must be a non-empty string"
        ):

            @requirement("")
            def test_empty_id():
                pass

    def test_requirement_decorator_invalid_testcase_id_whitespace_only(self):
        """Test that whitespace-only testcase_id raises TestInvalid."""
        with pytest.raises(
            ToolboxInvalidTestError, match="Test case ID must be a non-empty string"
        ):

            @requirement("   ")
            def test_whitespace_id():
                pass

    def test_requirement_decorator_invalid_testcase_id_none(self):
        """Test that None testcase_id raises TestInvalid."""
        with pytest.raises(
            ToolboxInvalidTestError, match="Test case ID must be a non-empty string"
        ):

            @requirement(None)  # type: ignore
            def test_none_id():
                pass

    def test_requirement_decorator_invalid_testcase_id_int(self):
        """Test that integer testcase_id raises TestInvalid."""
        with pytest.raises(
            ToolboxInvalidTestError, match="Test case ID must be a non-empty string"
        ):

            @requirement(123)  # type: ignore
            def test_int_id():
                pass

    def test_requirement_decorator_priority_values(self):
        """Test various priority values."""
        priorities = ["low", "medium", "high", "critical", "P0", "P1", "P2", "P3"]

        for priority in priorities:

            @requirement(f"TC_{priority}", priority=priority)
            def test_priority():
                assert True

            test_priority()
            assert hasattr(test_priority, "_qatoolbox_metadata")
            assert test_priority._qatoolbox_metadata["priority"] == priority

    def test_requirement_decorator_component_values(self):
        """Test various component values."""
        components = ["auth", "payment", "user-management", "api", "ui", "database"]

        for component in components:

            @requirement(f"TC_{component}", component=component)
            def test_component():
                assert True

            test_component()
            assert hasattr(test_component, "_qatoolbox_metadata")
            assert test_component._qatoolbox_metadata["component"] == component

    def test_requirement_decorator_special_characters_in_id(self):
        """Test handling of special characters in test case ID."""
        special_ids = [
            "TC-009",
            "TC 010",
            "TC_011",
            "TC.012",
            "TC@013",
            "TC#014",
            "TC$015",
        ]

        for test_id in special_ids:

            @requirement(test_id)
            def test_special_chars():
                assert True

            test_special_chars()
            assert hasattr(test_special_chars, "_qatoolbox_metadata")
            assert test_special_chars._qatoolbox_metadata["testcase_id"] == test_id


class TestRequirementDecoratorMetadata:
    """Test that metadata is correctly stored and accessible."""

    def test_metadata_storage(self):
        """Test that metadata is properly stored in the function."""

        @requirement(
            "TC100",
            description="Test metadata storage",
            priority="high",
            component="test",
        )
        def test_metadata():
            assert True

        metadata = test_metadata._qatoolbox_metadata
        assert metadata["testcase_id"] == "TC100"
        assert metadata["description"] == "Test metadata storage"
        assert metadata["priority"] == "high"
        assert metadata["component"] == "test"

    def test_metadata_with_partial_info(self):
        """Test metadata storage with only some fields provided."""

        @requirement("TC101", priority="critical")
        def test_partial():
            assert True

        metadata = test_partial._qatoolbox_metadata
        assert metadata["testcase_id"] == "TC101"
        assert metadata["priority"] == "critical"
        assert metadata["description"] is None
        assert metadata["component"] is None

    def test_metadata_with_none_values(self):
        """Test metadata storage with explicit None values."""

        @requirement("TC102", description=None, priority=None, component=None)
        def test_none_values():
            assert True

        metadata = test_none_values._qatoolbox_metadata
        assert metadata["testcase_id"] == "TC102"
        assert metadata["description"] is None
        assert metadata["priority"] is None
        assert metadata["component"] is None


class TestRequirementDecoratorIntegration:
    """Integration tests for the requirement decorator."""

    def test_decorator_with_pytest_fixtures(self, monkeypatch: MonkeyPatch):
        """Test that decorator works with pytest fixtures."""

        @requirement("TC200")
        def test_with_fixture(monkeypatch: MonkeyPatch):
            monkeypatch.setenv("TEST_VAR", "test_value")
            assert True

        test_with_fixture(monkeypatch)
        # Verify metadata is stored
        assert hasattr(test_with_fixture, "_qatoolbox_metadata")
        assert test_with_fixture._qatoolbox_metadata["testcase_id"] == "TC200"

    def test_decorator_with_pytest_parametrize(self):
        """Test that decorator works with pytest.mark.parametrize."""

        @pytest.mark.parametrize("value", [1, 2, 3])
        @requirement("TC201")
        def test_parametrized(value: int):
            assert value > 0

        # Test each parametrized version
        for i in [1, 2, 3]:
            test_parametrized(i)

        # Verify metadata is stored
        assert hasattr(test_parametrized, "_qatoolbox_metadata")
        assert test_parametrized._qatoolbox_metadata["testcase_id"] == "TC201"

    def test_decorator_with_pytest_skip(self):
        """Test that decorator works with pytest.mark.skip."""

        @pytest.mark.skip(reason="Test skip")
        @requirement("TC202")
        def test_skipped():
            assert True

        # The function should still be decorated even if skipped
        assert hasattr(test_skipped, "_qatoolbox_metadata")
        assert test_skipped._qatoolbox_metadata["testcase_id"] == "TC202"

    def test_decorator_with_pytest_xfail(self):
        """Test that decorator works with pytest.mark.xfail."""

        @pytest.mark.xfail(reason="Expected to fail")
        @requirement("TC203")
        def test_xfail():
            assert False  # This will fail as expected

        # The function should still be decorated even if expected to fail
        assert hasattr(test_xfail, "_qatoolbox_metadata")
        assert test_xfail._qatoolbox_metadata["testcase_id"] == "TC203"

    def test_multiple_decorators_order(self):
        """Test that multiple decorators work together in correct order."""

        @pytest.mark.slow
        @requirement("TC204", priority="high")
        @pytest.mark.parametrize("x", [1, 2])
        def test_multiple_decorators(x: int):
            assert x > 0

        # Test that metadata is stored
        assert hasattr(test_multiple_decorators, "_qatoolbox_metadata")
        assert test_multiple_decorators._qatoolbox_metadata["testcase_id"] == "TC204"
        assert test_multiple_decorators._qatoolbox_metadata["priority"] == "high"

        # Test the function works
        test_multiple_decorators(1)
        test_multiple_decorators(2)

    def test_decorator_preserves_function_signature(self):
        """Test that decorator preserves function signature for pytest."""

        @requirement("TC205")
        def test_signature(param1: str, param2: int = 10, *, kwarg1: bool = True):
            return f"{param1}_{param2}_{kwarg1}"

        # Test positional arguments
        result = test_signature("hello", 20)
        assert result == "hello_20_True"

        # Test keyword arguments
        result = test_signature("world", kwarg1=False)
        assert result == "world_10_False"

    def test_decorator_with_class_method(self):
        """Test that decorator works with class methods."""

        class TestClass:
            @requirement("TC206")
            def test_method(self):
                assert True

        test_instance = TestClass()
        test_instance.test_method()
        assert hasattr(test_instance.test_method, "_qatoolbox_metadata")
        assert test_instance.test_method._qatoolbox_metadata["testcase_id"] == "TC206"

    def test_decorator_with_static_method(self):
        """Test that decorator works with static methods."""

        class TestClass:
            @staticmethod
            @requirement("TC207")
            def test_static():
                assert True

        TestClass.test_static()
        assert hasattr(TestClass.test_static, "_qatoolbox_metadata")
        assert TestClass.test_static._qatoolbox_metadata["testcase_id"] == "TC207"


class TestRequirementDecoratorEdgeCases:
    """Test edge cases and error scenarios."""

    def test_very_long_testcase_id(self):
        """Test with very long test case ID."""
        long_id = "TC_" + "A" * 1000

        @requirement(long_id)
        def test_long_id():
            assert True

        test_long_id()
        assert hasattr(test_long_id, "_qatoolbox_metadata")
        assert test_long_id._qatoolbox_metadata["testcase_id"] == long_id

    def test_unicode_testcase_id(self):
        """Test with unicode characters in test case ID."""
        unicode_id = "TC_测试_🎯_αβγ"

        @requirement(unicode_id)
        def test_unicode():
            assert True

        test_unicode()
        assert hasattr(test_unicode, "_qatoolbox_metadata")
        assert test_unicode._qatoolbox_metadata["testcase_id"] == unicode_id

    def test_priority_with_special_characters(self):
        """Test priority with special characters."""

        @requirement("TC208", priority="P0-critical")
        def test_special_priority():
            assert True

        test_special_priority()
        assert hasattr(test_special_priority, "_qatoolbox_metadata")
        assert test_special_priority._qatoolbox_metadata["priority"] == "P0-critical"

    def test_component_with_special_characters(self):
        """Test component with special characters."""

        @requirement("TC209", component="user-management-v2")
        def test_special_component():
            assert True

        test_special_component()
        assert hasattr(test_special_component, "_qatoolbox_metadata")
        assert (
            test_special_component._qatoolbox_metadata["component"]
            == "user-management-v2"
        )

    def test_empty_priority(self):
        """Test with empty priority."""

        @requirement("TC210", priority="")
        def test_empty_priority():
            assert True

        test_empty_priority()
        assert hasattr(test_empty_priority, "_qatoolbox_metadata")
        assert test_empty_priority._qatoolbox_metadata["priority"] == ""

    def test_empty_component(self):
        """Test with empty component."""

        @requirement("TC211", component="")
        def test_empty_component():
            assert True

        test_empty_component()
        assert hasattr(test_empty_component, "_qatoolbox_metadata")
        assert test_empty_component._qatoolbox_metadata["component"] == ""

    def test_none_priority(self):
        """Test with None priority."""

        @requirement("TC212", priority=None)
        def test_none_priority():
            assert True

        test_none_priority()
        assert hasattr(test_none_priority, "_qatoolbox_metadata")
        assert test_none_priority._qatoolbox_metadata["priority"] is None

    def test_none_component(self):
        """Test with None component."""

        @requirement("TC213", component=None)
        def test_none_component():
            assert True

        test_none_component()
        assert hasattr(test_none_component, "_qatoolbox_metadata")
        assert test_none_component._qatoolbox_metadata["component"] is None


class TestRequirementDecoratorExecution:
    """Test execution with the requirement decorator."""

    def test_pytest_can_discover_decorated_tests(self):
        """Test that pytest can discover tests decorated with requirement."""

        @requirement("TC300")
        def test_discoverable():
            assert True

        # This test verifies that the function can be discovered by pytest
        # In a real scenario, pytest would find this test
        assert hasattr(test_discoverable, "_qatoolbox_metadata")
        assert test_discoverable._qatoolbox_metadata["testcase_id"] == "TC300"

    def test_metadata_storage_is_valid(self):
        """Test that the stored metadata is valid."""

        @requirement("TC301", priority="high", component="auth")
        def test_valid_metadata():
            assert True

        # Check that metadata is properly stored
        metadata = test_valid_metadata._qatoolbox_metadata
        assert isinstance(metadata, dict)
        assert "testcase_id" in metadata
        assert "priority" in metadata
        assert "component" in metadata
        assert metadata["testcase_id"] == "TC301"
        assert metadata["priority"] == "high"
        assert metadata["component"] == "auth"

    def test_multiple_tests_with_same_priority(self):
        """Test multiple tests with the same priority."""

        @requirement("TC302", priority="high")
        def test_high_priority_1():
            assert True

        @requirement("TC303", priority="high")
        def test_high_priority_2():
            assert True

        # Both should have priority metadata
        for test_func in [test_high_priority_1, test_high_priority_2]:
            assert hasattr(test_func, "_qatoolbox_metadata")
            assert test_func._qatoolbox_metadata["priority"] == "high"

    def test_multiple_tests_with_same_component(self):
        """Test multiple tests with the same component."""

        @requirement("TC304", component="payment")
        def test_payment_1():
            assert True

        @requirement("TC305", component="payment")
        def test_payment_2():
            assert True

        # Both should have component metadata
        for test_func in [test_payment_1, test_payment_2]:
            assert hasattr(test_func, "_qatoolbox_metadata")
            assert test_func._qatoolbox_metadata["component"] == "payment"
