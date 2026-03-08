"""Welcome page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class WelcomePage(QWizardPage):
    """Welcome page of the installer."""

    def __init__(self) -> None:
        """Initialize the welcome page."""
        super().__init__()

        self.setTitle("Welcome")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Arch-Javid Installer!"))
        layout.addWidget(QLabel("This installer will guide you through the installation process."))
        layout.addWidget(QLabel("Click Next to continue."))

        self.setLayout(layout)
