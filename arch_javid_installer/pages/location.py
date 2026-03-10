"""Location page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage

from arch_javid_installer.models import RegionOptions


class LocationPage(QWizardPage):
    """Location page of the installer.

    This page allows the user to select their region and timezone.
    This determines the system language, locale, and time settings.

    The regions correspond to the directories in `/usr/share/zoneinfo`, and the timezones correspond to the files within
    those directories.

    A symlink will be created: `ln -sf /usr/share/zoneinfo/{region}/{timezone} /etc/localtime`
    """

    def __init__(self, regions_dict: dict[RegionOptions, list[str]], default_region: RegionOptions) -> None:
        """Initialize the location page."""
        super().__init__()
        self._regions_dict = regions_dict
        self._default_region = default_region

        self.setTitle("Location")

        layout = QVBoxLayout()

        # Region selection
        layout.addWidget(QLabel("Region:"))
        self.region_list = QComboBox()

        for region in self._regions_dict.keys():
            self.region_list.addItem(region.value)

        # Set the default region
        default_index = list(self._regions_dict.keys()).index(self._default_region)
        self.region_list.setCurrentIndex(default_index)

        layout.addWidget(self.region_list)

        # Timezone selection
        layout.addWidget(QLabel("Timezone:"))
        self.timezone_list = QComboBox()
        layout.addWidget(self.timezone_list)

        # Populate initial timezones
        self._update_timezones()

        # Connect signal to update timezones when region changes
        self.region_list.currentIndexChanged.connect(self._update_timezones)

        layout.addWidget(self.timezone_list)

        self.setLayout(layout)

    def _update_timezones(self) -> None:
        """Update the timezone list based on the selected region."""
        # Get the selected region
        selected_region_str = self.region_list.currentText()
        selected_region = RegionOptions(selected_region_str)

        # Clear existing timezones
        self.timezone_list.clear()

        # Add timezones for the selected region
        timezones = self._regions_dict[selected_region]
        for timezone in timezones:
            self.timezone_list.addItem(timezone)
