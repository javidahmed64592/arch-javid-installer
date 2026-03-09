"""Keyboard page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage


class KeyboardPage(QWizardPage):
    """Keyboard page of the installer."""

    def __init__(self) -> None:
        """Initialize the keyboard page."""
        super().__init__()

        self.setTitle("Keyboard")

        layout = QVBoxLayout()

        # Model selection
        layout.addWidget(QLabel("Model:"))
        self.keyboard_model_list = QComboBox()

        keyboard_models = [
            "pc105",
            "pc104",
            "pc102",
        ]

        for model in keyboard_models:
            self.keyboard_model_list.addItem(model)

        layout.addWidget(self.keyboard_model_list)

        # Layout selection
        layout.addWidget(QLabel("Layout:"))
        self.keyboard_layout_list = QComboBox()

        keyboard_layouts = [
            "us",
            "uk",
            "de",
        ]

        for layout_option in keyboard_layouts:
            self.keyboard_layout_list.addItem(layout_option)

        layout.addWidget(self.keyboard_layout_list)

        self.setLayout(layout)
