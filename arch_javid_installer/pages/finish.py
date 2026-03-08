"""Finish page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class FinishPage(QWizardPage):
    """Finish page of the installer."""

    def __init__(self) -> None:
        """Initialize the finish page."""
        super().__init__()

        self.setTitle("Complete")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Arch-Javid has finished installing! Click Finish to exit the installer."))

        self.setLayout(layout)
