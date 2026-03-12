"""Installer wizard UI."""

from PySide6.QtWidgets import QWizard

from arch_javid_installer.helpers import (
    get_disk_options,
    get_keyboard_options,
    get_language_options,
    get_region_options,
)
from arch_javid_installer.models import PagesEnum, RegionOptions
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
        _regions_options = get_region_options()
        _keyboard_models, _keyboard_layouts_dict = get_keyboard_options()
        _disk_options = get_disk_options()

        self.pages = {
            PagesEnum.WELCOME: WelcomePage(
                title="Welcome",
                language_options=_language_options,
                default_locale="en_GB.UTF-8",
            ),
            PagesEnum.LOCATION: LocationPage(
                title="Location",
                regions_dict=_regions_options,
                default_region=RegionOptions.EUROPE,
                default_zone="London",
            ),
            PagesEnum.KEYBOARD: KeyboardPage(
                title="Keyboard",
                models=_keyboard_models,
                layouts_dict=_keyboard_layouts_dict,
                default_model=next(
                    (model for model in _keyboard_models if model.model == "pc105"), _keyboard_models[0]
                ),
                default_layout=next(
                    (layout for layout in _keyboard_layouts_dict.keys() if layout.layout == "gb"),
                    next(iter(_keyboard_layouts_dict.keys())),
                ),
            ),
            PagesEnum.DISK: DiskPage(
                title="Disk Selection",
                disk_options=_disk_options,
            ),
            PagesEnum.USER: UserPage(
                title="User Account",
            ),
            PagesEnum.SUMMARY: SummaryPage(
                title="Summary",
            ),
            PagesEnum.INSTALL: InstallPage(
                title="Installation",
            ),
            PagesEnum.FINISH: FinishPage(
                title="Complete",
            ),
        }

        self.setWindowTitle("Arch-Javid Installer")

        for i, page in enumerate(self.pages.values()):
            self.setPage(i, page)
