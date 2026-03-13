"""Location page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage

from arch_javid_installer.models import LocationChoice, RegionOptions


class LocationPage(QWizardPage):
    """Location page of the installer.

    This page allows the user to select their region and timezone.
    This determines the system language, locale, and time settings.

    The regions correspond to the directories in `/usr/share/zoneinfo`, and the timezones correspond to the files within
    those directories.
    """

    def __init__(
        self, title: str, regions_dict: dict[RegionOptions, list[str]], default_region: RegionOptions, default_zone: str
    ) -> None:
        """Initialize the location page."""
        super().__init__()
        self.setTitle(title)
        self._regions_dict = regions_dict
        self._default_region = default_region
        self._default_zone = default_zone

        layout = QVBoxLayout()

        self._add_region_selection(layout)
        self._add_timezone_selection(layout)

        self.region_list.currentIndexChanged.connect(self._update_timezones)

        self.setLayout(layout)

    def _add_region_selection(self, layout: QVBoxLayout) -> None:
        """Add the region selection to the layout."""
        layout.addWidget(QLabel("Region:"))
        self.region_list = QComboBox()

        for region in self._regions_dict.keys():
            self.region_list.addItem(region.value)

        # Set the default region
        default_index = list(self._regions_dict.keys()).index(self._default_region)
        self.region_list.setCurrentIndex(default_index)

        layout.addWidget(self.region_list)

    def _add_timezone_selection(self, layout: QVBoxLayout) -> None:
        """Add the timezone selection to the layout."""
        layout.addWidget(QLabel("Timezone:"))
        self.timezone_list = QComboBox()

        self._update_timezones()
        layout.addWidget(self.timezone_list)

    def _update_timezones(self) -> None:
        """Update the timezone list based on the selected region."""
        selected_region_str = self.region_list.currentText()
        selected_region = RegionOptions(selected_region_str)

        self.timezone_list.clear()

        timezones = self._regions_dict[selected_region]
        for timezone in timezones:
            self.timezone_list.addItem(timezone)

        if self._default_zone in timezones:
            default_zone_index = timezones.index(self._default_zone)
            self.timezone_list.setCurrentIndex(default_zone_index)

    def get_choice(self) -> LocationChoice:
        """Get the selected location choice."""
        selected_region_str = self.region_list.currentText()
        selected_region = RegionOptions(selected_region_str)
        selected_zone = self.timezone_list.currentText()
        return LocationChoice(region=selected_region, zone=selected_zone)
