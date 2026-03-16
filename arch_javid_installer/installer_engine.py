"""Orchestrator for the installer scripts."""

from PySide6.QtCore import QObject, Signal

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


class InstallerEngine(QObject):
    """Orchestrator for the installer scripts."""

    # Signals for progress tracking
    progress_updated = Signal(int)  # Emits progress percentage (0-100)
    log_message = Signal(str)  # Emits log messages for display
    installation_complete = Signal(bool)  # Emits True on success, False on failure

    EFI_SIZE_MB = 2048
    PACMAN_CONF_FILEPATH = "/etc/pacman.conf"
    PACKAGES_FILEPATH = "/root/packages.txt"

    # Total number of installation steps for progress calculation
    TOTAL_STEPS = 13

    def __init__(self, config: InstallationConfig) -> None:
        """Initialize the installer engine with the given configuration."""
        super().__init__()
        self.config = config
        self.current_step = 0

    def _update_progress(self, message: str) -> None:
        """Update progress and emit signals."""
        self.current_step += 1
        progress = int((self.current_step / self.TOTAL_STEPS) * 100)
        self.progress_updated.emit(progress)
        self.log_message.emit(message)

    def make_scripts_executable(self) -> None:
        """Make all scripts executable."""
        self.log_message.emit("Making scripts executable...")
        for script_type in ScriptType:
            make_scripts_executable(script_type)

    def run_system_scripts(self) -> None:
        """Run all system scripts in the correct order."""
        script_type = ScriptType.SYSTEM
        scripts = SCRIPTS[script_type]

        _disk = self.config.disk.disk_to_use.name
        _efi_part = f"{_disk}1"
        _root_part = f"{_disk}2"

        self._update_progress("Partitioning disk...")
        run_script(
            script_type=script_type,
            script_name=scripts["partition"],
            flags=[
                f"--disk {_disk}",
                f"--efi-size {self.EFI_SIZE_MB}",
            ],
        )

        self._update_progress("Creating filesystems...")
        run_script(
            script_type=script_type,
            script_name=scripts["makefs"],
            flags=[
                f"--efi-part {_efi_part}",
                f"--root-part {_root_part}",
            ],
        )

        self._update_progress("Mounting partitions...")
        run_script(
            script_type=script_type,
            script_name=scripts["mount"],
            flags=[
                f"--efi-part {_efi_part}",
                f"--root-part {_root_part}",
            ],
        )

        self._update_progress("Installing base system packages...")
        run_script(
            script_type=script_type,
            script_name=scripts["base"],
            flags=[
                f"--pacman-conf {self.PACMAN_CONF_FILEPATH}",
                f"--packages {self.PACKAGES_FILEPATH}",
            ],
        )

        self._update_progress("Generating fstab...")
        run_script(script_type=script_type, script_name=scripts["fstab"], flags=[])

        self._update_progress("Preparing chroot environment...")
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

        self._update_progress("Configuring locale and timezone...")
        run_script(
            script_type=script_type,
            script_name=scripts["locale"],
            flags=[
                f"--locale {self.config.language.locale.code}",
                f"--region {self.config.location.region}",
                f"--zone {self.config.location.zone}",
            ],
        )

        self._update_progress("Configuring keyboard layout...")
        run_script(
            script_type=script_type,
            script_name=scripts["keyboard"],
            flags=[
                f"--model {self.config.keyboard.model.model}",
                f"--layout {self.config.keyboard.layout.layout}",
                f"--variant {self.config.keyboard.variant.variant}",
            ],
        )

        self._update_progress("Creating user accounts...")
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

        self._update_progress("Enabling system services...")
        run_script(script_type=script_type, script_name=scripts["services"], flags=[])

        self._update_progress("Installing NVIDIA drivers...")
        run_script(script_type=script_type, script_name=scripts["nvidia"], flags=[])

        self._update_progress("Installing bootloader...")
        run_script(script_type=script_type, script_name=scripts["bootloader"], flags=[])

    def run(self) -> None:
        """Run the installer engine."""
        try:
            self.current_step = 0
            self.log_message.emit("Starting installation...")

            self.make_scripts_executable()
            self.run_system_scripts()
            self.run_chroot_scripts()

            self._update_progress("Unmounting partitions...")
            run_script(script_type=ScriptType.SYSTEM, script_name=SCRIPTS[ScriptType.SYSTEM]["unmount"], flags=[])

            self.log_message.emit("Installation completed successfully!")
            self.progress_updated.emit(100)
            self.installation_complete.emit(True)  # noqa: FBT003
        except Exception as e:
            self.log_message.emit(f"Installation failed: {e!s}")
            self.installation_complete.emit(False)  # noqa: FBT003
