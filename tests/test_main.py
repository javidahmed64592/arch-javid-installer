"""Unit tests for the arch_javid_installer.main module."""

from arch_javid_installer.main import example_function


def test_example_function() -> None:
    """Test the example_function."""
    result = example_function()
    assert result == "This is an example function."
