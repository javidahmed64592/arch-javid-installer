"""Keyboard page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage

from arch_javid_installer.models import KeyboardLayoutName, KeyboardModelName, KeyboardVariantName


class KeyboardPage(QWizardPage):
    """Keyboard page of the installer.

    This page allows the user to select their keyboard model, layout, and variant.
    The available variants depend on the selected layout.
    """

    def __init__(
        self,
        models: list[KeyboardModelName],
        layouts_dict: dict[KeyboardLayoutName, list[KeyboardVariantName]],
        default_model: KeyboardModelName,
        default_layout: KeyboardLayoutName,
    ) -> None:
        """Initialize the keyboard page."""
        super().__init__()
        self._models = models
        self._layouts_dict = layouts_dict
        self._default_model = default_model
        self._default_layout = default_layout

        self.setTitle("Keyboard")

        layout = QVBoxLayout()

        # Model selection
        layout.addWidget(QLabel("Model:"))
        self.keyboard_model_list = QComboBox()

        for model in self._models:
            self.keyboard_model_list.addItem(f"{model.name} ({model.model})", model)

        # Set the default model
        default_model_index = self._models.index(self._default_model)
        self.keyboard_model_list.setCurrentIndex(default_model_index)

        layout.addWidget(self.keyboard_model_list)

        # Layout selection
        layout.addWidget(QLabel("Layout:"))
        self.keyboard_layout_list = QComboBox()

        for keyboard_layout in self._layouts_dict.keys():
            self.keyboard_layout_list.addItem(f"{keyboard_layout.name} ({keyboard_layout.layout})", keyboard_layout)

        # Set the default layout
        default_layout_index = list(self._layouts_dict.keys()).index(self._default_layout)
        self.keyboard_layout_list.setCurrentIndex(default_layout_index)

        layout.addWidget(self.keyboard_layout_list)

        # Variant selection
        layout.addWidget(QLabel("Variant:"))
        self.keyboard_variant_list = QComboBox()
        layout.addWidget(self.keyboard_variant_list)

        # Populate initial variants
        self._update_variants()

        # Connect signal to update variants when layout changes
        self.keyboard_layout_list.currentIndexChanged.connect(self._update_variants)

        layout.addWidget(self.keyboard_variant_list)

        self.setLayout(layout)

    def _update_variants(self) -> None:
        """Update the variant list based on the selected layout."""
        # Get the selected layout
        selected_layout = self.keyboard_layout_list.currentData()

        # Clear existing variants
        self.keyboard_variant_list.clear()

        # Add variants for the selected layout
        variants = self._layouts_dict[selected_layout]
        for variant in variants:
            self.keyboard_variant_list.addItem(f"{variant.name} ({variant.variant})", variant)
