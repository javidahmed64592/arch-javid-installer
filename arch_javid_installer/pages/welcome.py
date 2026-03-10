"""Welcome page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage


class WelcomePage(QWizardPage):
    """Welcome page of the installer."""

    def __init__(self, language_options: list[str]) -> None:
        """Initialize the welcome page."""
        super().__init__()

        self.setTitle("Welcome")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Arch-Javid Installer!"))

        # Language selection
        layout.addWidget(QLabel("Select your language:"))
        self.language_list = QComboBox()

        for language in language_options:
            self.language_list.addItem(language)

        layout.addWidget(self.language_list)

        self.setLayout(layout)
