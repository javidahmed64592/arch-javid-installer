"""Shell commands for the installer to use."""

import subprocess
from enum import StrEnum
from pathlib import Path
from site import getsitepackages

from arch_javid_installer.models import RegionOptions

# Constants
SCRIPTS_DIRECTORY = Path(getsitepackages()[0]) / "scripts"


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
        return Path(SCRIPTS_DIRECTORY / self.value)

    def get_script_path(self, script_name: str) -> str:
        """Get the full path to a script of this type."""
        return str(self.script_directory / script_name)


# Resource filepaths and command templates
SUPPORTED_LOCALES_FILEPATH = "/usr/share/i18n/SUPPORTED"
KEYBOARD_LAYOUTS_FILEPATH = "/usr/share/X11/xkb/rules/base.lst"

ZONEINFO_DIRECTORY = "/usr/share/zoneinfo"

LIST_BLOCKS_COMMAND = "lsblk -J -o NAME,SIZE,MODEL,LABEL,FSTYPE,MOUNTPOINT"


# General methods
def run_command(command: list[str]) -> subprocess.CompletedProcess:
    """Run a command in the shell."""
    try:
        return subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed with exit code {e.returncode}\n"
        if e.stdout:
            error_msg += f"STDOUT:\n{e.stdout}\n"
        if e.stderr:
            error_msg += f"STDERR:\n{e.stderr}"
        raise RuntimeError(error_msg) from e


def run_script(script_type: ScriptType, script_name: str, flags: list[str]) -> subprocess.CompletedProcess:
    """Run a script of the given type and name."""
    script_path = script_type.get_script_path(script_name)
    return run_command([*script_type.command_prefix, script_path, *flags])


def list_directory_command(directory: str) -> list[str]:
    """Return a command to list the contents of a directory."""
    return ["ls", directory]


def read_file_command(filepath: str) -> list[str]:
    """Return a command to read the contents of a file."""
    return ["cat", filepath]


def list_directory(directory: str) -> list[str]:
    """List the contents of a directory."""
    result = run_command(list_directory_command(directory))
    return result.stdout.splitlines()


def read_file(filepath: str) -> str:
    """Read the contents of a file."""
    result = run_command(read_file_command(filepath))
    return result.stdout


# Pre-installation methods
def get_supported_locales() -> list[str]:
    """Get a list of supported locales from the system."""
    return read_file(SUPPORTED_LOCALES_FILEPATH).splitlines()


def get_zones_for_region(region: RegionOptions) -> list[str]:
    """Get a list of timezones for a given region."""
    return list_directory(f"{ZONEINFO_DIRECTORY}/{region}")


def get_available_keyboard_layouts() -> list[str]:
    """Get a list of keyboard models, layouts, and variants."""
    return read_file(KEYBOARD_LAYOUTS_FILEPATH).splitlines()


def get_disks_json() -> str:
    """Get a JSON string of available disks and their partitions."""
    result = run_command(LIST_BLOCKS_COMMAND.split())
    disks: str = result.stdout
    return disks


# Installation methods
def make_scripts_executable(script_type: ScriptType) -> None:
    """Make all scripts of the given type executable."""
    scripts = list_directory(str(script_type.script_directory))
    run_command(["chmod", "+x", *[str(script_type.script_directory / s) for s in scripts]])
