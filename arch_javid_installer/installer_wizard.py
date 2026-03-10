"""Installer wizard UI."""

from PySide6.QtWidgets import QWizard

from arch_javid_installer.helpers import get_language_options, get_regions_dict
from arch_javid_installer.models import RegionOptions
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

        # Pre-installation
        _language_options = get_language_options()
        _regions_dict = get_regions_dict()

        self.pages = {
            "welcome": WelcomePage(language_options=_language_options, default_locale="en_GB.UTF-8"),
            "location": LocationPage(regions_dict=_regions_dict, default_region=RegionOptions.EUROPE),
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
