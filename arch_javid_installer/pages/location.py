"""Location page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class LocationPage(QWizardPage):
    """Location page of the installer."""

    def __init__(self) -> None:
        """Initialize the location page."""
        super().__init__()

        self.setTitle("Location & Region")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your location to set the timezone and locale."))

        self.setLayout(layout)
