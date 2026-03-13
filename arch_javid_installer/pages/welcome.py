"""Welcome page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage

from arch_javid_installer.models import LanguageChoice, LocaleInfo


class WelcomePage(QWizardPage):
    """Welcome page of the installer.

    This page allows the user to select their language, which determines the system locale and language settings.

    The language options are derived from the supported locales on the system, which are read from
    `/usr/share/i18n/SUPPORTED`.
    """

    def __init__(self, title: str, language_options: list[LocaleInfo], default_locale: str) -> None:
        """Initialize the welcome page."""
        super().__init__()
        self.setTitle(title)
        self._language_options = language_options
        self._default_locale = default_locale

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to the Arch-Javid Installer!"))
        self._add_language_selection(layout)

        self.setLayout(layout)

    def _add_language_selection(self, layout: QVBoxLayout) -> None:
        """Add the language selection to the layout."""
        layout.addWidget(QLabel("Select your language:"))
        self.language_list = QComboBox()

        for locale_info in self._language_options:
            self.language_list.addItem(locale_info.display_name)

        default_index = next(
            (i for i, locale in enumerate(self._language_options) if locale.code == self._default_locale), 0
        )
        self.language_list.setCurrentIndex(default_index)

        layout.addWidget(self.language_list)

    def get_choice(self) -> LanguageChoice:
        """Get the selected language choice."""
        current_index = self.language_list.currentIndex()
        selected_locale = self._language_options[current_index]
        return LanguageChoice(locale=selected_locale)
