"""Helper methods for the installer."""

from babel import Locale
from babel.core import UnknownLocaleError

from arch_javid_installer.models import (
    KeyboardLayoutName,
    KeyboardLayoutSectionMarkers,
    KeyboardModelName,
    KeyboardVariantName,
    RegionOptions,
)
from arch_javid_installer.shell import get_supported_locales, get_zones_for_region


# Pre-installation methods
def get_name_from_language_code(code: str) -> str:
    """Get the display name of a language code."""
    # Remove encoding suffix if present
    locale_code = code.split(maxsplit=1)[0]
    if "." in locale_code:
        locale_code = locale_code.split(".", maxsplit=1)[0]

    try:
        locale = Locale.parse(locale_code, sep="_")
        display_name = locale.get_display_name("en")
    except (UnknownLocaleError, ValueError):
        return locale_code
    else:
        return display_name or locale_code


def get_language_options() -> dict[str, str]:
    """Convert a list of supported locales to a list of language options."""
    language_options: dict[str, str] = {}

    for locale_line in get_supported_locales():
        if not locale_line.strip() or locale_line.startswith("#"):
            continue

        locale_code = locale_line.split(maxsplit=1)[0]
        display_name = get_name_from_language_code(locale_code)

        if display_name in language_options.values():
            continue

        language_options[locale_code] = display_name

    return dict(sorted(language_options.items(), key=lambda item: item[1]))


def get_region_options() -> dict[str, list[str]]:
    """Get a dictionary of regions and their corresponding timezones."""
    return {region: get_zones_for_region(region) for region in RegionOptions}


def _keyboard_layout_parser(func: callable) -> callable:
    """Wrap a keyboard layout parser function."""
    _expected_len_parts = 2

    def wrapper(line: str) -> KeyboardModelName | KeyboardLayoutName | KeyboardVariantName | None:
        parts = line.split(maxsplit=1)
        if len(parts) != _expected_len_parts:
            return None
        return func(parts)

    return wrapper


@_keyboard_layout_parser
def _parse_keyboard_model_line(parts: list[str]) -> KeyboardModelName | None:
    """Parse a keyboard model line."""
    model_code, model_name = parts
    return KeyboardModelName(model=model_code.strip(), name=model_name.strip())


@_keyboard_layout_parser
def _parse_keyboard_layout_line(parts: list[str]) -> KeyboardLayoutName | None:
    """Parse a keyboard layout line."""
    layout_code, layout_name = parts
    return KeyboardLayoutName(layout=layout_code.strip(), name=layout_name.strip())


@_keyboard_layout_parser
def _parse_keyboard_variant_line(parts: list[str]) -> KeyboardVariantName | None:
    """Parse a keyboard variant line."""
    variant_code, rest = parts
    variant_code = parts[0].strip()
    rest = parts[1].strip()
    if ": " not in rest:
        return None
    layout_code, variant_name = rest.split(": ", 1)
    return KeyboardVariantName(variant=variant_code, layout=layout_code.strip(), name=variant_name.strip())


def get_keyboard_options(
    lines: list[str],
) -> tuple[list[KeyboardModelName], list[KeyboardLayoutName], list[KeyboardVariantName]]:
    """Get a list of keyboard models, layouts, and variants."""
    models: list[KeyboardModelName] = []
    layouts: list[KeyboardLayoutName] = []
    variants: list[KeyboardVariantName] = []

    current_section: KeyboardLayoutSectionMarkers | None = None

    for line in lines:
        # Check if this is a section header
        if line.startswith("! "):
            section_name = line[2:].strip()
            try:
                current_section = KeyboardLayoutSectionMarkers(section_name)
            except ValueError:
                current_section = None
            continue

        # Skip empty lines or lines that don't start with whitespace
        if not line or not line.startswith("  "):
            continue

        # Parse the line based on the current section
        match current_section:
            case KeyboardLayoutSectionMarkers.MODEL:
                if model := _parse_keyboard_model_line(line):
                    models.append(model)
            case KeyboardLayoutSectionMarkers.LAYOUT:
                if layout := _parse_keyboard_layout_line(line):
                    layouts.append(layout)
            case KeyboardLayoutSectionMarkers.VARIANT:
                if variant := _parse_keyboard_variant_line(line):
                    variants.append(variant)

    # Create default variants for layouts without variants
    layout_codes_with_variants = {variant.layout for variant in variants}
    for layout in layouts:
        if layout.layout not in layout_codes_with_variants:
            default_variant = KeyboardVariantName(variant="default", layout=layout.layout, name="Default")
            variants.append(default_variant)

    return models, layouts, variants
