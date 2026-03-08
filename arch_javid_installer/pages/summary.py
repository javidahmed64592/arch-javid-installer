"""Summary page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class SummaryPage(QWizardPage):
    """Summary page of the installer."""

    def __init__(self) -> None:
        """Initialize the summary page."""
        super().__init__()

        self.setTitle("Summary")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your OS will be installed with the following settings:"))
        layout.addWidget(QLabel("Click Next to begin installation."))

        self.setLayout(layout)
