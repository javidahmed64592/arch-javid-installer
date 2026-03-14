"""Keyboard page."""

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWizardPage

from arch_javid_installer.models import KeyboardChoice, KeyboardLayoutName, KeyboardModelName, KeyboardVariantName


class KeyboardPage(QWizardPage):
    """Keyboard page of the installer.

    This page allows the user to select their keyboard model, layout, and variant.
    The available variants depend on the selected layout.

    The available options are retrieved from `/usr/share/X11/xkb/rules/base.lst`.
    """

    def __init__(
        self,
        title: str,
        models: list[KeyboardModelName],
        layouts_dict: dict[KeyboardLayoutName, list[KeyboardVariantName]],
        default_model: KeyboardModelName,
        default_layout: KeyboardLayoutName,
    ) -> None:
        """Initialize the keyboard page."""
        super().__init__()
        self.setTitle(title)
        self._models = models
        self._layouts_dict = layouts_dict
        self._default_model = default_model
        self._default_layout = default_layout

        layout = QVBoxLayout()

        self._add_model_selection(layout)
        self._add_layout_selection(layout)
        self._add_variant_selection(layout)

        self.keyboard_layout_list.currentIndexChanged.connect(self._update_variants)

        self.setLayout(layout)

    def _add_model_selection(self, layout: QVBoxLayout) -> None:
        """Add the model selection to the layout."""
        layout.addWidget(QLabel("Model:"))
        self.keyboard_model_list = QComboBox()

        for model in self._models:
            self.keyboard_model_list.addItem(model.name, model)

        default_model_index = self._models.index(self._default_model)
        self.keyboard_model_list.setCurrentIndex(default_model_index)

        layout.addWidget(self.keyboard_model_list)

    def _add_layout_selection(self, layout: QVBoxLayout) -> None:
        """Add the layout selection to the layout."""
        layout.addWidget(QLabel("Layout:"))
        self.keyboard_layout_list = QComboBox()

        for keyboard_layout in self._layouts_dict.keys():
            self.keyboard_layout_list.addItem(keyboard_layout.name, keyboard_layout)

        default_layout_index = list(self._layouts_dict.keys()).index(self._default_layout)
        self.keyboard_layout_list.setCurrentIndex(default_layout_index)

        layout.addWidget(self.keyboard_layout_list)

    def _add_variant_selection(self, layout: QVBoxLayout) -> None:
        """Add the variant selection to the layout."""
        layout.addWidget(QLabel("Variant:"))
        self.keyboard_variant_list = QComboBox()
        layout.addWidget(self.keyboard_variant_list)

        self._update_variants()
        layout.addWidget(self.keyboard_variant_list)

    def _update_variants(self) -> None:
        """Update the variant list based on the selected layout."""
        self.keyboard_variant_list.clear()

        variants = self._layouts_dict[self.keyboard_layout_list.currentData()]
        for variant in variants:
            self.keyboard_variant_list.addItem(variant.name, variant)

    def get_choice(self) -> KeyboardChoice:
        """Get the selected keyboard choice."""
        selected_model = self.keyboard_model_list.currentData()
        selected_layout = self.keyboard_layout_list.currentData()
        selected_variant = self.keyboard_variant_list.currentData()
        return KeyboardChoice(model=selected_model, layout=selected_layout, variant=selected_variant)
