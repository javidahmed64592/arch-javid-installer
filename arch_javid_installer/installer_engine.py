"""Orchestrator for the installer scripts."""

from PySide6.QtCore import QObject, Signal

from arch_javid_installer.models import InstallationConfig
from arch_javid_installer.shell import ScriptType, run_script

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

    def run_system_scripts(self) -> None:
        """Run all system scripts in the correct order."""
        self.log_message.emit("Running system scripts...")
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
                "--disk",
                _disk,
                "--efi-size",
                str(self.EFI_SIZE_MB),
            ],
        )
        self.log_message.emit("Disk partitioned successfully.")

        self._update_progress("Creating filesystems...")
        run_script(
            script_type=script_type,
            script_name=scripts["makefs"],
            flags=[
                "--efi-part",
                _efi_part,
                "--root-part",
                _root_part,
            ],
        )
        self.log_message.emit("Filesystems created successfully.")

        self._update_progress("Mounting partitions...")
        run_script(
            script_type=script_type,
            script_name=scripts["mount"],
            flags=[
                "--efi-part",
                _efi_part,
                "--root-part",
                _root_part,
            ],
        )
        self.log_message.emit("Partitions mounted successfully.")

        self._update_progress("Installing base system packages...")
        run_script(
            script_type=script_type,
            script_name=scripts["base"],
            flags=[
                "--pacman-conf",
                self.PACMAN_CONF_FILEPATH,
                "--packages",
                self.PACKAGES_FILEPATH,
            ],
        )
        self.log_message.emit("Base system packages installed successfully.")

        self._update_progress("Generating fstab...")
        run_script(script_type=script_type, script_name=scripts["fstab"], flags=[])
        self.log_message.emit("fstab generated successfully.")

        self._update_progress("Preparing chroot environment...")
        run_script(
            script_type=script_type,
            script_name=scripts["chroot"],
            flags=[
                "--script-directory",
                str(ScriptType.CHROOT.script_directory),
            ],
        )
        self.log_message.emit("Chroot environment prepared successfully.")

    def run_chroot_scripts(self) -> None:
        """Run all chroot scripts in the correct order."""
        self.log_message.emit("Running chroot scripts...")
        script_type = ScriptType.CHROOT
        scripts = SCRIPTS[script_type]

        self._update_progress("Configuring locale and timezone...")
        run_script(
            script_type=script_type,
            script_name=scripts["locale"],
            flags=[
                "--locale",
                self.config.language.locale.code,
                "--region",
                self.config.location.region,
                "--zone",
                self.config.location.zone,
            ],
        )
        self.log_message.emit("Locale and timezone configured successfully.")

        self._update_progress("Configuring keyboard layout...")

        run_script(
            script_type=script_type,
            script_name=scripts["keyboard"],
            flags=[
                "--model",
                self.config.keyboard.model.model,
                "--layout",
                self.config.keyboard.layout.layout,
                "--variant",
                self.config.keyboard.variant.variant,
            ],
        )
        self.log_message.emit("Keyboard layout configured successfully.")

        self._update_progress("Creating user accounts...")
        run_script(
            script_type=script_type,
            script_name=scripts["users"],
            flags=[
                "--hostname",
                self.config.user.hostname,
                "--username",
                self.config.user.username,
                "--password",
                self.config.user.password,
                "--root-password",
                self.config.user.root_password,
            ],
        )
        self.log_message.emit("User accounts created successfully.")

        self._update_progress("Enabling system services...")
        run_script(script_type=script_type, script_name=scripts["services"], flags=[])
        self.log_message.emit("System services enabled successfully.")

        self._update_progress("Installing NVIDIA drivers...")
        run_script(script_type=script_type, script_name=scripts["nvidia"], flags=[])
        self.log_message.emit("NVIDIA drivers installed successfully.")

        self._update_progress("Installing bootloader...")
        run_script(script_type=script_type, script_name=scripts["bootloader"], flags=[])
        self.log_message.emit("Bootloader installed successfully.")

    def run(self) -> None:
        """Run the installer engine."""
        try:
            self.log_message.emit("Starting installation...")
            self.current_step = 0

            self.run_system_scripts()
            self.run_chroot_scripts()

            self._update_progress("Unmounting partitions...")
            run_script(script_type=ScriptType.SYSTEM, script_name=SCRIPTS[ScriptType.SYSTEM]["unmount"], flags=[])
            self.log_message.emit("Partitions unmounted successfully.")

            self.log_message.emit("Installation completed successfully!")
            self.progress_updated.emit(100)
            self.installation_complete.emit(True)  # noqa: FBT003
        except Exception as e:
            self.log_message.emit(f"Installation failed:\n{e!s}")
            self.installation_complete.emit(False)  # noqa: FBT003
