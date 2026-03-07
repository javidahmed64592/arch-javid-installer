"""Utility script for GitHub workflows."""

import tomllib
from functools import cache

from pyhere import here


@cache
def _load_pyproject() -> dict:
    """Load the pyproject.toml file."""
    with here("pyproject.toml").open("rb") as f:
        return tomllib.load(f)


@cache
def _load_uv_lock() -> dict:
    """Load the uv.lock file."""
    with here("uv.lock").open("rb") as f:
        return tomllib.load(f)


@cache
def _get_version_pyproject() -> str:
    """Get the version from pyproject.toml."""
    pyproject = _load_pyproject()
    return str(pyproject["project"]["version"])


@cache
def _get_name_pyproject() -> str:
    """Get the name from pyproject.toml."""
    pyproject = _load_pyproject()
    return str(pyproject["project"]["name"])


@cache
def _get_version_uv_lock() -> str:
    """Get the version from uv.lock."""
    name = _get_name_pyproject()
    uv_lock = _load_uv_lock()
    if pkg := next((p for p in uv_lock["package"] if p["name"] == name), None):
        return str(pkg["version"])

    error_msg = f"Package '{name}' not found in uv.lock"
    raise ValueError(error_msg)


def print_version_pyproject() -> None:
    """Get the version from pyproject.toml."""
    print(_get_version_pyproject())


def print_name_pyproject() -> None:
    """Get the name from pyproject.toml."""
    print(_get_name_pyproject())


def print_version_uv_lock() -> None:
    """Get the version from uv.lock."""
    print(_get_version_uv_lock())
