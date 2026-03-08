"""User page."""

from PySide6.QtWidgets import QLabel, QLineEdit, QRadioButton, QVBoxLayout, QWizardPage


class UserPage(QWizardPage):
    """User page of the installer."""

    def __init__(self) -> None:
        """Initialize the user page."""
        super().__init__()

        self.setTitle("User Account")

        layout = QVBoxLayout()

        self.username = QLineEdit()
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Confirm Password"))
        layout.addWidget(self.confirm_password)

        self.root_same_password = QRadioButton("Root password same as user password")
        layout.addWidget(self.root_same_password)

        self.root_password = QLineEdit()
        self.root_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Root Password"))
        layout.addWidget(self.root_password)

        self.confirm_root_password = QLineEdit()
        self.confirm_root_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Confirm Root Password"))
        layout.addWidget(self.confirm_root_password)

        self.setLayout(layout)
