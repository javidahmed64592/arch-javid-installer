"""Unit tests for the template_python.workflows module."""

from unittest.mock import patch

import pytest

from template_python.workflows import (
    _get_name_pyproject,
    _get_version_pyproject,
    _get_version_uv_lock,
    _load_pyproject,
    _load_uv_lock,
    print_name_pyproject,
    print_version_pyproject,
    print_version_uv_lock,
)


class TestWorkflows:
    """Tests for the template_python.workflows module."""

    def test_load_pyproject(self) -> None:
        """Test loading the pyproject.toml file."""
        pyproject = _load_pyproject()
        assert "project" in pyproject
        assert "name" in pyproject["project"]
        assert "version" in pyproject["project"]

    def test_load_uv_lock(self) -> None:
        """Test loading the uv.lock file."""
        name = _get_name_pyproject()
        uv_lock = _load_uv_lock()
        assert "package" in uv_lock
        assert any(p["name"] == name for p in uv_lock["package"])

    def test_get_version_pyproject(self) -> None:
        """Test getting the version from pyproject.toml."""
        version = _get_version_pyproject()
        assert isinstance(version, str)

    def test_get_name_pyproject(self) -> None:
        """Test getting the name from pyproject.toml."""
        name = _get_name_pyproject()
        assert isinstance(name, str)

    def test_get_version_uv_lock(self) -> None:
        """Test getting the version from uv.lock."""
        version = _get_version_uv_lock()
        assert isinstance(version, str)

    def test_get_version_uv_lock_not_found(self) -> None:
        """Test getting the version from uv.lock when the package is not found."""
        pyproject = _load_pyproject()

        _get_version_uv_lock.cache_clear()

        with (
            patch("template_python.workflows._load_uv_lock", return_value={"package": []}),
            pytest.raises(ValueError, match=rf"Package '{pyproject['project']['name']}' not found in uv.lock"),
        ):
            _get_version_uv_lock()

    def test_print_version_pyproject(self) -> None:
        """Test printing the version from pyproject.toml."""
        print_version_pyproject()

    def test_print_name_pyproject(self) -> None:
        """Test printing the name from pyproject.toml."""
        print_name_pyproject()

    def test_print_version_uv_lock(self) -> None:
        """Test printing the version from uv.lock."""
        print_version_uv_lock()
