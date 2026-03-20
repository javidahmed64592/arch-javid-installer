"""Main entry point for Arch-Javid Installer."""

from PySide6.QtWidgets import QApplication

from arch_javid_installer.installer_wizard import InstallerWizard
from arch_javid_installer.logging_setup import setup_logging


def main() -> None:
    """Run the installer."""
    setup_logging()
    app = QApplication([])
    wizard = InstallerWizard()
    wizard.show()
    app.exec()
