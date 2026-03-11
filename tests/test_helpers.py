"""Unit tests for the arch_javid_installer.helpers module."""

from arch_javid_installer.helpers import get_keyboard_options
from arch_javid_installer.models import KeyboardLayoutName, KeyboardModelName, KeyboardVariantName


class TestKeyboardHelpers:
    """Unit tests for keyboard helper functions."""

    def test_get_keyboard_options(self) -> None:
        """Test the get_keyboard_options function."""
        mock_models = [
            KeyboardModelName(model="pc86", name="Generic 86-key PC"),
            KeyboardModelName(model="pc101", name="Generic 101-key PC"),
            KeyboardModelName(model="pc102", name="Generic 102-key PC"),
        ]
        mock_layouts = [
            KeyboardLayoutName(layout="gb", name="English (UK)"),
            KeyboardLayoutName(layout="us", name="English (US)"),
        ]
        mock_variants = [
            KeyboardVariantName(variant="extd", layout="gb", name="English (UK, extended, Windows)"),
            KeyboardVariantName(variant="intl", layout="gb", name="English (UK, intl., with dead keys)"),
        ]

        def _mock_model_line(model: KeyboardModelName) -> str:
            return f"  {model.model}            {model.name}\n"

        def _mock_layout_line(layout: KeyboardLayoutName) -> str:
            return f"  {layout.layout}              {layout.name}\n"

        def _mock_variant_line(variant: KeyboardVariantName) -> str:
            return f"  {variant.variant}            {variant.layout}: {variant.name}\n"

        mock_layouts_file_content = [
            "! model\n",
            *[_mock_model_line(model) for model in mock_models],
            "\n",
            "! layout\n",
            *[_mock_layout_line(layout) for layout in mock_layouts],
            "\n",
            "! variant\n",
            *[_mock_variant_line(variant) for variant in mock_variants],
        ]

        models, layouts, variants = get_keyboard_options(mock_layouts_file_content)
        assert models == mock_models
        assert layouts == mock_layouts
        assert variants == [*mock_variants, KeyboardVariantName(variant="default", layout="us", name="Default")]
