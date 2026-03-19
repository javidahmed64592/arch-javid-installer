"""Unit tests for the arch_javid_installer.shell module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from arch_javid_installer.models import RegionOptions
from arch_javid_installer.shell import (
    KEYBOARD_LAYOUTS_FILEPATH,
    LIST_BLOCKS_COMMAND,
    SUPPORTED_LOCALES_FILEPATH,
    ZONEINFO_DIRECTORY,
    ScriptType,
    get_available_keyboard_layouts,
    get_disks_json,
    get_supported_locales,
    get_zones_for_region,
    list_directory_command,
    read_file_command,
    run_command,
    run_script,
)


@pytest.fixture
def mock_run_command() -> Generator[MagicMock]:
    """Fixture to mock the run_command function."""
    with patch("arch_javid_installer.shell.run_command") as mock_run:
        yield mock_run


class TestGeneralMethods:
    """Tests for the general shell command methods."""

    def test_run_command(self) -> None:
        """Test that run_command calls subprocess.run with the correct arguments."""
        command = ["echo", "Hello, World!"]

        with patch("subprocess.run") as mock_run:
            result = run_command(command)

        mock_run.assert_called_once_with(command, check=True, capture_output=True, text=True)
        assert result.stdout == mock_run.return_value.stdout

    @pytest.mark.parametrize(
        ("script_type", "expected_prefix"),
        [
            (ScriptType.CHROOT, ["arch-chroot", "/mnt"]),
            (ScriptType.SYSTEM, ["/bin/bash"]),
        ],
    )
    def test_run_script(self, script_type: ScriptType, expected_prefix: list[str], mock_run_command: MagicMock) -> None:
        """Test that run_script calls run_command with the correct arguments."""
        script_name = "test_script.sh"
        flags = ["--input1", "value1", "--input2", "value2"]

        result = run_script(script_type, script_name, flags)

        mock_run_command.assert_called_once_with([*expected_prefix, script_type.get_script_path(script_name), *flags])
        assert result == mock_run_command.return_value

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


class TestPreInstallationMethods:
    """Tests for the pre-installation shell command methods."""

    def test_get_supported_locales(self, mock_run_command: MagicMock) -> None:
        """Test that get_supported_locales returns a list of locales."""
        assert get_supported_locales() == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(read_file_command(SUPPORTED_LOCALES_FILEPATH))

    def test_get_zones_for_region(self, mock_run_command: MagicMock) -> None:
        """Test that get_zones_for_region returns a list of timezones for a given region."""
        region = RegionOptions.EUROPE
        assert get_zones_for_region(region) == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(list_directory_command(f"{ZONEINFO_DIRECTORY}/{region}"))

    def test_get_available_keyboard_layouts(self, mock_run_command: MagicMock) -> None:
        """Test that get_available_keyboard_layouts returns a list of keyboard layouts."""
        assert get_available_keyboard_layouts() == mock_run_command.return_value.stdout.splitlines()
        mock_run_command.assert_called_once_with(read_file_command(KEYBOARD_LAYOUTS_FILEPATH))

    def test_get_disks_json(self, mock_run_command: MagicMock) -> None:
        """Test that get_disks_json returns a JSON string of available disks."""
        assert get_disks_json() == mock_run_command.return_value.stdout
        mock_run_command.assert_called_once_with(LIST_BLOCKS_COMMAND.split())
