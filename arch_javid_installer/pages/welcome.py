"""Welcome page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage


class WelcomePage(QWizardPage):
    """Welcome page of the installer.

    This page allows the user to select their language, which determines the system locale and language settings.

    The language options are derived from the supported locales on the system, which are read from
    `/usr/share/i18n/SUPPORTED`.

    The chosen locale gets uncommented in `/etc/locale.gen`, and `locale-gen` is run to generate the locale.
    It also gets assigned to the following environment variables in `/etc/locale.conf`:

    [`LANG`, `LC_ADDRESS`, `LC_IDENTIFICATION`, `LC_MEASUREMENT`, `LC_MONETARY`, `LC_NAME`, `LC_NUMERIC`, `LC_PAPER`,
    `LC_TELEPHONE`, `LC_TIME`]
    """

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
