"""User page."""

from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox, QRadioButton, QVBoxLayout, QWizardPage

from arch_javid_installer.models import UserChoice


class UserPage(QWizardPage):
    """User page of the installer."""

    def __init__(self, title: str) -> None:
        """Initialize the user page."""
        super().__init__()
        self.setTitle(title)

        layout = QVBoxLayout()

        self._add_computer_name_field(layout)
        self._add_username_field(layout)
        self._add_password_fields(layout)
        self._add_root_password_radio_button(layout)
        self._add_root_password_fields(layout)

        self.setLayout(layout)

    def _add_computer_name_field(self, layout: QVBoxLayout) -> None:
        """Add the computer name field to the layout."""
        self.computer_name = QLineEdit()
        layout.addWidget(QLabel("Computer Name:"))
        layout.addWidget(self.computer_name)

    def _add_username_field(self, layout: QVBoxLayout) -> None:
        """Add the username field to the layout."""
        self.username = QLineEdit()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)

    def _add_password_fields(self, layout: QVBoxLayout) -> None:
        """Add the password fields to the layout."""
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.confirm_password)

    def _add_root_password_radio_button(self, layout: QVBoxLayout) -> None:
        """Add the root password radio button to the layout."""
        self.root_same_password = QRadioButton("Use the same password for the root user.")
        layout.addWidget(self.root_same_password)
        self.root_same_password.toggled.connect(self._toggle_root_password_fields)

    def _add_root_password_fields(self, layout: QVBoxLayout) -> None:
        """Add the root password fields to the layout."""
        self.root_password = QLineEdit()
        self.root_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Root Password:"))
        layout.addWidget(self.root_password)

        self.confirm_root_password = QLineEdit()
        self.confirm_root_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Confirm Root Password:"))
        layout.addWidget(self.confirm_root_password)

    def _toggle_root_password_fields(self, checked: bool) -> None:  # noqa: FBT001
        """Toggle the root password fields based on the state of the radio button."""
        self.root_password.setEnabled(not checked)
        self.confirm_root_password.setEnabled(not checked)

    def validatePage(self) -> bool:  # noqa: N802, PLR0911
        """Validate that all required fields are filled and passwords match."""
        # Check all fields are filled
        if not self.computer_name.text().strip():
            QMessageBox.warning(self, "Error", "Please enter a computer name.")
            return False

        if not self.username.text().strip():
            QMessageBox.warning(self, "Error", "Please enter a username.")
            return False

        if not self.password.text():
            QMessageBox.warning(self, "Error", "Please enter a password.")
            return False

        if not self.confirm_password.text():
            QMessageBox.warning(self, "Error", "Please confirm your password.")
            return False

        # Check passwords match
        if self.password.text() != self.confirm_password.text():
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return False

        # Check root password if not using same password
        if not self.root_same_password.isChecked():
            if not self.root_password.text():
                QMessageBox.warning(self, "Error", "Please enter a root password.")
                return False

            if not self.confirm_root_password.text():
                QMessageBox.warning(self, "Error", "Please confirm the root password.")
                return False

            if self.root_password.text() != self.confirm_root_password.text():
                QMessageBox.warning(self, "Error", "Root passwords do not match.")
                return False

        return True

    def get_choice(self) -> UserChoice:
        """Get the user choice."""
        root_password = self.password.text() if self.root_same_password.isChecked() else self.root_password.text()

        return UserChoice(
            computer_name=self.computer_name.text().strip(),
            username=self.username.text().strip(),
            password=self.password.text(),
            root_password=root_password,
        )
