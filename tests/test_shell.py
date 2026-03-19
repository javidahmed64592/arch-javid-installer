"""Unit tests for the arch_javid_installer.shell module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from arch_javid_installer.models import RegionOptions
from arch_javid_installer.shell import (
    LIST_BLOCKS_COMMAND,
    ScriptType,
    get_available_keyboard_layouts,
    get_disks_json,
    get_supported_locales,
    get_zones_for_region,
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


@pytest.fixture
def mock_path_read_text() -> Generator[MagicMock]:
    """Fixture to mock the Path.read_text method."""
    with patch("pathlib.Path.read_text") as mock_read_text:
        yield mock_read_text


@pytest.fixture
def mock_path_iterdir() -> Generator[MagicMock]:
    """Fixture to mock the Path.iterdir method."""
    with patch("pathlib.Path.iterdir") as mock_iterdir:
        yield mock_iterdir


class TestPreInstallationMethods:
    """Tests for the pre-installation shell command methods."""

    def test_get_supported_locales(self, mock_path_read_text: MagicMock) -> None:
        """Test that get_supported_locales returns a list of locales."""
        mock_path_read_text.return_value = "en_US.UTF-8 UTF-8\nde_DE.UTF-8 UTF-8\nfr_FR.UTF-8 UTF-8"
        result = get_supported_locales()
        assert result == ["en_US.UTF-8 UTF-8", "de_DE.UTF-8 UTF-8", "fr_FR.UTF-8 UTF-8"]

    def test_get_zones_for_region(self, mock_path_iterdir: MagicMock) -> None:
        """Test that get_zones_for_region returns a list of timezones for a given region."""
        region = RegionOptions.EUROPE
        mock_entry1 = MagicMock()
        mock_entry1.name = "London"
        mock_entry1.is_file.return_value = True
        mock_entry1.is_dir.return_value = False

        mock_entry2 = MagicMock()
        mock_entry2.name = "Paris"
        mock_entry2.is_file.return_value = False
        mock_entry2.is_dir.return_value = True

        mock_path_iterdir.return_value = [mock_entry1, mock_entry2]

        result = get_zones_for_region(region)
        assert result == [mock_entry1.name, mock_entry2.name]

    def test_get_available_keyboard_layouts(self, mock_path_read_text: MagicMock) -> None:
        """Test that get_available_keyboard_layouts returns a list of keyboard layouts."""
        mock_path_read_text.return_value = "! model\n  pc104    Generic 104-key PC\n! layout\n  us    English (US)"
        result = get_available_keyboard_layouts()
        assert result == ["! model", "  pc104    Generic 104-key PC", "! layout", "  us    English (US)"]

    def test_get_disks_json(self, mock_run_command: MagicMock) -> None:
        """Test that get_disks_json returns a JSON string of available disks."""
        assert get_disks_json() == mock_run_command.return_value.stdout
        mock_run_command.assert_called_once_with(LIST_BLOCKS_COMMAND.split())
