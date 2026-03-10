"""Shell commands for the installer to use."""

import subprocess

from arch_javid_installer.models import RegionOptions

SUPPORTED_LOCALES_FILEPATH = "/usr/share/i18n/SUPPORTED"
ZONEINFO_DIRECTORY = "/usr/share/zoneinfo"


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


# Pre-installation methods
def get_supported_locales() -> list[str]:
    """Get a list of supported locales from the system."""
    result = run_command(read_file_command(SUPPORTED_LOCALES_FILEPATH))
    return result.stdout.splitlines()


def get_zones_for_region(region: RegionOptions) -> list[str]:
    """Get a list of timezones for a given region."""
    directory = f"{ZONEINFO_DIRECTORY}/{region}"
    result = run_command(list_directory_command(directory))
    return result.stdout.splitlines()
