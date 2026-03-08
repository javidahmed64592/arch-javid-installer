"""Installer wizard UI."""

from PySide6.QtWidgets import QWizard

from arch_javid_installer.pages import (
    DiskPage,
    FinishPage,
    InstallPage,
    KeyboardPage,
    LocationPage,
    SummaryPage,
    UserPage,
    WelcomePage,
)


class InstallerWizard(QWizard):
    """Main installer wizard."""

    def __init__(self) -> None:
        """Initialize the installer wizard."""
        super().__init__()

        self.pages = {
            "welcome": WelcomePage(),
            "location": LocationPage(),
            "keyboard": KeyboardPage(),
            "disk": DiskPage(),
            "user": UserPage(),
            "summary": SummaryPage(),
            "install": InstallPage(),
            "finish": FinishPage(),
        }

        self.setWindowTitle("Arch-Javid Installer")

        for i, page in enumerate(self.pages.values()):
            self.setPage(i, page)
