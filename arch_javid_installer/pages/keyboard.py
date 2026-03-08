"""Keyboard page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWizardPage


class KeyboardPage(QWizardPage):
    """Keyboard page of the installer."""

    def __init__(self) -> None:
        """Initialize the keyboard page."""
        super().__init__()

        self.setTitle("Keyboard Layout")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select your keyboard layout."))

        self.setLayout(layout)
