"""Location page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage


class LocationPage(QWizardPage):
    """Location page of the installer."""

    def __init__(self) -> None:
        """Initialize the location page."""
        super().__init__()

        self.setTitle("Location")

        layout = QVBoxLayout()

        # Region selection
        layout.addWidget(QLabel("Region:"))
        self.region_list = QComboBox()

        region_options = [
            "Africa",
            "America",
            "Antarctica",
            "Asia",
            "Atlantic",
            "Australia",
            "Europe",
            "Indian",
            "Pacific",
        ]

        for region in region_options:
            self.region_list.addItem(region)

        layout.addWidget(self.region_list)

        # Timezone selection
        layout.addWidget(QLabel("Timezone:"))
        self.timezone_list = QComboBox()
        layout.addWidget(self.timezone_list)

        timezones = [
            "Cairo",
            "New_York",
            "McMurdo",
        ]

        for timezone in timezones:
            self.timezone_list.addItem(timezone)

        layout.addWidget(self.timezone_list)

        self.setLayout(layout)
