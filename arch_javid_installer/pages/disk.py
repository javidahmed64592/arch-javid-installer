"""Disk page."""

from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWizardPage


class DiskPage(QWizardPage):
    """Disk page of the installer."""

    def __init__(self) -> None:
        """Initialize the disk page."""
        super().__init__()

        self.setTitle("Disk Selection")

        layout = QVBoxLayout()

        self.disk = QLineEdit("/dev/nvme0n1")
        layout.addWidget(QLabel("Target Disk:"))
        layout.addWidget(self.disk)

        self.setLayout(layout)
