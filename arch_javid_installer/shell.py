"""Shell commands for the installer to use."""

import logging
import subprocess
from enum import StrEnum
from pathlib import Path
from site import getsitepackages

from arch_javid_installer.models import RegionOptions

logger = logging.getLogger(__name__)

# Resource filepaths and command templates
SCRIPTS_DIRECTORY = Path(getsitepackages()[0]) / "scripts"

SUPPORTED_LOCALES_FILEPATH = "/usr/share/i18n/SUPPORTED"
KEYBOARD_LAYOUTS_FILEPATH = "/usr/share/X11/xkb/rules/base.lst"
ZONEINFO_DIRECTORY = "/usr/share/zoneinfo"

LIST_BLOCKS_COMMAND = "lsblk -J -o NAME,SIZE,MODEL,LABEL,FSTYPE,MOUNTPOINT"


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


# General methods
def run_command(command: list[str]) -> subprocess.CompletedProcess:
    """Run a command in the shell."""
    try:
        completed_process = subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603
        if (stdout := completed_process.stdout) and stdout.strip():
            logger.info("STDOUT:\n%s", stdout)
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed with exit code {e.returncode}\n"
        if e.stderr:
            error_msg += f"STDERR:\n{e.stderr}"
        raise RuntimeError(error_msg) from e
    else:
        return completed_process


def run_script(script_type: ScriptType, script_name: str, flags: list[str]) -> subprocess.CompletedProcess:
    """Run a script of the given type and name."""
    logger.info("Running script: %s", script_name)
    script_path = script_type.get_script_path(script_name)
    return run_command([*script_type.command_prefix, script_path, *flags])


# Pre-installation methods
def get_supported_locales() -> list[str]:
    """Get a list of supported locales from the system."""
    return Path(SUPPORTED_LOCALES_FILEPATH).read_text().splitlines()


def get_zones_for_region(region: RegionOptions) -> list[str]:
    """Get a list of timezones for a given region."""
    region_path = Path(ZONEINFO_DIRECTORY) / str(region)
    return [entry.name for entry in region_path.iterdir() if entry.is_file() or entry.is_dir()]


def get_available_keyboard_layouts() -> list[str]:
    """Get a list of keyboard models, layouts, and variants."""
    return Path(KEYBOARD_LAYOUTS_FILEPATH).read_text().splitlines()


def get_disks_json() -> str:
    """Get a JSON string of available disks and their partitions."""
    logger.info("Listing available disks with: %s", " ".join(LIST_BLOCKS_COMMAND.split()))
    result = run_command(LIST_BLOCKS_COMMAND.split())
    disks: str = result.stdout
    return disks
