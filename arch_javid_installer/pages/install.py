"""Install page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class InstallPage(QWizardPage):
    """Install page of the installer."""

    def __init__(self, title: str) -> None:
        """Initialize the install page."""
        super().__init__()
        self.setTitle(title)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Installing Arch-Javid..."))

        self.setLayout(layout)
