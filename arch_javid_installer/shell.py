"""Shell commands for the installer to use."""

import subprocess
from enum import StrEnum
from pathlib import Path

from pyhere import here

from arch_javid_installer.models import RegionOptions

# Constants
SCRIPTS_DIRECTORY = here() / "scripts"


class ScriptType(StrEnum):
    """Subdirectory names for different types of scripts."""

    CHROOT = "chroot"
    SYSTEM = "system"

    @property
    def command_prefix(self) -> list[str]:
        """Get the command prefix for this script type."""
        match self:
            case ScriptType.CHROOT:
                return ["arch-chroot", "/mnt"]
            case ScriptType.SYSTEM:
                return ["/bin/bash"]

    @property
    def script_directory(self) -> Path:
        """Get the directory name for this script type."""
        return SCRIPTS_DIRECTORY / self.value

    def get_script_path(self, script_name: str) -> str:
        """Get the full path to a script of this type."""
        return str(self.script_directory / script_name)


# Resource filepaths and command templates
SUPPORTED_LOCALES_FILEPATH = "/usr/share/i18n/SUPPORTED"
KEYBOARD_LAYOUTS_FILEPATH = "/usr/share/X11/xkb/rules/base.lst"

ZONEINFO_DIRECTORY = "/usr/share/zoneinfo"

LIST_BLOCKS_COMMAND = "lsblk -J -o NAME,SIZE,MODEL,LABEL,FSTYPE,MOUNTPOINT"


# General methods
def list_directory_command(directory: str) -> list[str]:
    """Return a command to list the contents of a directory."""
    return ["ls", directory]


def read_file_command(filepath: str) -> list[str]:
    """Return a command to read the contents of a file."""
    return ["cat", filepath]


def run_command(command: list[str]) -> subprocess.CompletedProcess:
    """Run a command in the shell."""
    return subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603


def run_script(script_type: ScriptType, script_name: str, flags: list[str]) -> subprocess.CompletedProcess:
    """Run a script of the given type and name."""
    script_path = script_type.get_script_path(script_name)
    return run_command([*script_type.command_prefix, script_path, *flags])


# Pre-installation methods
def get_supported_locales() -> list[str]:
    """Get a list of supported locales from the system."""
    result = run_command(read_file_command(SUPPORTED_LOCALES_FILEPATH))
    locales: list[str] = result.stdout.splitlines()
    return locales


def get_zones_for_region(region: RegionOptions) -> list[str]:
    """Get a list of timezones for a given region."""
    result = run_command(list_directory_command(f"{ZONEINFO_DIRECTORY}/{region}"))
    zones: list[str] = result.stdout.splitlines()
    return zones


def get_available_keyboard_layouts() -> list[str]:
    """Get a list of keyboard models, layouts, and variants."""
    result = run_command(read_file_command(KEYBOARD_LAYOUTS_FILEPATH))
    lines: list[str] = result.stdout.splitlines()
    return lines


def get_disks_json() -> str:
    """Get a JSON string of available disks and their partitions."""
    result = run_command(LIST_BLOCKS_COMMAND.split())
    disks: str = result.stdout
    return disks


# Installation methods
def make_scripts_executable(script_type: ScriptType) -> None:
    """Make all scripts of the given type executable."""
    run_command(["chmod", "+x", f"{script_type.script_directory}/*.sh"])
