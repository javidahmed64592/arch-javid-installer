"""Orchestrator for the installer scripts."""

from arch_javid_installer.models import InstallationConfig
from arch_javid_installer.shell import ScriptType, make_scripts_executable, run_script

SCRIPTS = {
    ScriptType.CHROOT: {
        "bootloader": "bootloader.sh",
        "keyboard": "keyboard.sh",
        "locale": "locale.sh",
        "nvidia": "nvidia.sh",
        "services": "services.sh",
        "users": "users.sh",
    },
    ScriptType.SYSTEM: {
        "base": "base.sh",
        "chroot": "chroot.sh",
        "fstab": "fstab.sh",
        "makefs": "makefs.sh",
        "mount": "mount.sh",
        "partition": "partition.sh",
        "unmount": "unmount.sh",
    },
}


class InstallerEngine:
    """Orchestrator for the installer scripts."""

    EFI_SIZE_MB = 2048
    PACMAN_CONF_FILEPATH = "/etc/pacman.conf"
    PACKAGES_FILEPATH = "/root/packages.txt"

    def __init__(self, config: InstallationConfig) -> None:
        """Initialize the installer engine with the given configuration."""
        self.config = config

    def make_scripts_executable(self) -> None:
        """Make all scripts executable."""
        for script_type in ScriptType:
            make_scripts_executable(script_type)

    def run_system_scripts(self) -> None:
        """Run all system scripts in the correct order."""
        script_type = ScriptType.SYSTEM
        scripts = SCRIPTS[script_type]

        _disk = self.config.disk
        _efi_part = f"{_disk}1"
        _root_part = f"{_disk}2"

        run_script(
            script_type=script_type,
            script_name=scripts["partition"],
            flags=[
                f"--disk {_disk}",
                f"--efi-size {self.EFI_SIZE_MB}",
            ],
        )

        run_script(
            script_type=script_type,
            script_name=scripts["makefs"],
            flags=[
                f"--efi-part {_efi_part}",
                f"--root-part {_root_part}",
            ],
        )

        run_script(
            script_type=script_type,
            script_name=scripts["mount"],
            flags=[
                f"--efi-part {_efi_part}",
                f"--root-part {_root_part}",
            ],
        )

        run_script(
            script_type=script_type,
            script_name=scripts["base"],
            flags=[
                f"--pacman-conf {self.PACMAN_CONF_FILEPATH}",
                f"--packages {self.PACKAGES_FILEPATH}",
            ],
        )

        run_script(script_type=script_type, script_name=scripts["fstab"], flags=[])

        run_script(
            script_type=script_type,
            script_name=scripts["chroot"],
            flags=[
                f"--script-directory {ScriptType.CHROOT.script_directory}",
            ],
        )

    def run_chroot_scripts(self) -> None:
        """Run all chroot scripts in the correct order."""
        script_type = ScriptType.CHROOT
        scripts = SCRIPTS[script_type]

        run_script(
            script_type=script_type,
            script_name=scripts["locale"],
            flags=[
                f"--locale {self.config.language.locale.code}",
                f"--region {self.config.location.region}",
                f"--zone {self.config.location.zone}",
            ],
        )

        run_script(
            script_type=script_type,
            script_name=scripts["keyboard"],
            flags=[
                f"--model {self.config.keyboard.model.model}",
                f"--layout {self.config.keyboard.layout.layout}",
                f"--variant {self.config.keyboard.variant.variant}",
            ],
        )

        run_script(
            script_type=script_type,
            script_name=scripts["users"],
            flags=[
                f"--hostname {self.config.user.hostname}",
                f"--username {self.config.user.username}",
                f"--password {self.config.user.password}",
                f"--root_password {self.config.user.root_password}",
            ],
        )

        run_script(script_type=script_type, script_name=scripts["services"], flags=[])
        run_script(script_type=script_type, script_name=scripts["nvidia"], flags=[])
        run_script(script_type=script_type, script_name=scripts["bootloader"], flags=[])

    def run(self) -> None:
        """Run the installer engine."""
        self.make_scripts_executable()
        self.run_system_scripts()
        self.run_chroot_scripts()
        run_script(script_type=ScriptType.SYSTEM, script_name=SCRIPTS[ScriptType.SYSTEM]["unmount"], flags=[])
