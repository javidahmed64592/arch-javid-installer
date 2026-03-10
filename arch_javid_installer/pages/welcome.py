"""Welcome page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage


class WelcomePage(QWizardPage):
    """Welcome page of the installer."""

    def __init__(self, language_options: dict[str, str], default_locale: str) -> None:
        """Initialize the welcome page."""
        super().__init__()
        self._language_options = language_options
        self._default_locale = default_locale

        self.setTitle("Welcome")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Arch-Javid Installer!"))

        # Language selection
        layout.addWidget(QLabel("Select your language:"))
        self.language_list = QComboBox()

        for language in language_options.values():
            self.language_list.addItem(language)

        # Set the default language
        default_index = list(language_options.keys()).index(self._default_locale)
        self.language_list.setCurrentIndex(default_index)

        layout.addWidget(self.language_list)

        self.setLayout(layout)
