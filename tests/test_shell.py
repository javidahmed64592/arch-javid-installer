"""Unit tests for the arch_javid_installer.shell module."""

import subprocess
from collections.abc import Generator
from unittest.mock import patch

import pytest

from arch_javid_installer.shell import (
    KEYBOARD_LAYOUTS_FILEPATH,
    LIST_BLOCKS_COMMAND,
    SUPPORTED_LOCALES_FILEPATH,
    ZONEINFO_DIRECTORY,
    get_available_keyboard_layouts,
    get_disks_json,
    get_supported_locales,
    get_zones_for_region,
    list_directory_command,
    read_file_command,
    run_command,
)


@pytest.fixture
def mock_run_command() -> Generator[subprocess.CompletedProcess]:
    """Fixture to mock the run_command function."""
    with patch("arch_javid_installer.shell.run_command") as mock_run:
        yield mock_run


class TestGeneralMethods:
    """Tests for the general shell command methods."""

    def test_list_directory_command(self) -> None:
        """Test that the list_directory_command returns the correct command."""
        directory = "/some/directory"
        expected_command = ["ls", directory]
        assert list_directory_command(directory) == expected_command

    def test_read_file_command(self) -> None:
        """Test that the read_file_command returns the correct command."""
        filepath = "/some/file.txt"
        expected_command = ["cat", filepath]
        assert read_file_command(filepath) == expected_command

    def test_run_command(self) -> None:
        """Test that run_command calls subprocess.run with the correct arguments."""
        command = ["echo", "Hello, World!"]

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=command, returncode=0, stdout="Hello, World!\n", stderr=""
            )
            result = run_command(command)

        mock_run.assert_called_once_with(command, check=True, capture_output=True, text=True)
        assert result.stdout == "Hello, World!\n"


class TestPreInstallationMethods:
    """Tests for the pre-installation shell command methods."""

    def test_get_supported_locales(self, mock_run_command: subprocess.CompletedProcess) -> None:
        """Test that get_supported_locales returns a list of locales."""
        assert get_supported_locales() == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(read_file_command(SUPPORTED_LOCALES_FILEPATH))

    def test_get_zones_for_region(self, mock_run_command: subprocess.CompletedProcess) -> None:
        """Test that get_zones_for_region returns a list of timezones for a given region."""
        region = "Europe"
        assert get_zones_for_region(region) == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(list_directory_command(f"{ZONEINFO_DIRECTORY}/{region}"))

    def test_get_available_keyboard_layouts(self, mock_run_command: subprocess.CompletedProcess) -> None:
        """Test that get_available_keyboard_layouts returns a list of keyboard layouts."""
        assert get_available_keyboard_layouts() == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(read_file_command(KEYBOARD_LAYOUTS_FILEPATH))

    def test_get_disks_json(self, mock_run_command: subprocess.CompletedProcess) -> None:
        """Test that get_disks_json returns a JSON string of available disks."""
        assert get_disks_json() == mock_run_command.return_value.stdout
        mock_run_command.assert_called_once_with(LIST_BLOCKS_COMMAND.split())
