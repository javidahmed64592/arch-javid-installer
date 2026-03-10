"""Installer wizard UI."""

from PySide6.QtWidgets import QWizard

from arch_javid_installer.helpers import get_regions_dict, supported_locales_to_language_options
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
from arch_javid_installer.shell import get_supported_locales


class InstallerWizard(QWizard):
    """Main installer wizard."""

    def __init__(self) -> None:
        """Initialize the installer wizard."""
        super().__init__()

        # Pre-installation
        _supported_locales = get_supported_locales()
        _language_options = supported_locales_to_language_options(_supported_locales)

        _regions_dict = get_regions_dict()

        self.pages = {
            "welcome": WelcomePage(language_options=_language_options),
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
