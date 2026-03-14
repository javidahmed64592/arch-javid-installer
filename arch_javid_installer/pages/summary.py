"""Summary page."""

from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWizardPage

from arch_javid_installer.models import InstallationConfig, PagesEnum


class SummaryPage(QWizardPage):
    """Summary page of the installer."""

    def __init__(self, title: str) -> None:
        """Initialize the summary page."""
        super().__init__()
        self.setTitle(title)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your OS will be installed with the following settings:"))

        # Create a scroll area for the summary content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.summary_content = QLabel()
        self.summary_content.setWordWrap(True)
        self.summary_content.setTextInteractionFlags(
            self.summary_content.textInteractionFlags() | self.summary_content.textInteractionFlags()
        )

        self.scroll_area.setWidget(self.summary_content)
        layout.addWidget(self.scroll_area)

        layout.addWidget(QLabel("Click Next to begin installation."))

        self.setLayout(layout)

    def initializePage(self) -> None:  # noqa: N802
        """Update the summary with the latest configuration when the page is entered."""
        # Get the wizard and collect choices from all pages
        wizard = self.wizard()

        welcome_page = wizard.page(PagesEnum.WELCOME.page_id)
        location_page = wizard.page(PagesEnum.LOCATION.page_id)
        keyboard_page = wizard.page(PagesEnum.KEYBOARD.page_id)
        disk_page = wizard.page(PagesEnum.DISK.page_id)
        user_page = wizard.page(PagesEnum.USER.page_id)

        language_choice = welcome_page.get_choice()
        location_choice = location_page.get_choice()
        keyboard_choice = keyboard_page.get_choice()
        disk_choice = disk_page.get_choice()
        user_choice = user_page.get_choice()

        # Create the configuration
        config = InstallationConfig(
            language=language_choice,
            location=location_choice,
            keyboard=keyboard_choice,
            disk=disk_choice,
            user=user_choice,
        )

        # Store the configuration in the wizard for later use
        wizard.installation_config = config

        # Format the summary
        summary_text = self._format_summary(config)
        self.summary_content.setText(summary_text)

    def _format_summary(self, config: InstallationConfig) -> str:
        """Format the installation configuration as HTML for display."""
        html = "<html><body>"
        html += "<h3>Language & Location</h3>"
        html += f"<p><b>Locale:</b> {config.language.locale.display_name}</p>"
        html += f"<p><b>Region:</b> {config.location.region.value}</p>"
        html += f"<p><b>Timezone:</b> {config.location.zone}</p>"

        html += "<h3>Keyboard</h3>"
        html += f"<p><b>Model:</b> {config.keyboard.model.name}</p>"
        html += f"<p><b>Layout:</b> {config.keyboard.layout.name}</p>"
        html += f"<p><b>Variant:</b> {config.keyboard.variant.name}</p>"

        html += "<h3>Disk Configuration</h3>"
        html += f"<p><b>Disk:</b> /dev/{config.disk.disk_to_use.name} ({config.disk.disk_to_use.size})</p>"
        if config.disk.disk_to_use.model:
            html += f"<p><b>Model:</b> {config.disk.disk_to_use.model}</p>"
        html += f"<p><b>Partition Mode:</b> {config.disk.partition_mode.value.capitalize()}</p>"

        html += "<h3>User Account</h3>"
        html += f"<p><b>Computer Name:</b> {config.user.computer_name}</p>"
        html += f"<p><b>Username:</b> {config.user.username}</p>"
        html += f"<p><b>Root Password:</b> {
            'Same as user password' if config.user.password == config.user.root_password else 'Different password'
        }</p>"

        html += "</body></html>"

        return html
