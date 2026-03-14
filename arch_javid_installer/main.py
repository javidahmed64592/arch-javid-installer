"""Main entry point for Arch-Javid Installer."""

from PySide6.QtWidgets import QApplication

from arch_javid_installer.installer_wizard import InstallerWizard


def main() -> None:
    """Run the installer."""
    app = QApplication([])
    wizard = InstallerWizard()
    wizard.show()
    app.exec()
