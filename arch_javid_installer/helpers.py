"""Helper methods for the installer."""

import json
from collections.abc import Callable

from babel import Locale
from babel.core import UnknownLocaleError

from arch_javid_installer.models import (
    DiskInfo,
    KeyboardLayoutName,
    KeyboardLayoutSectionMarkers,
    KeyboardModelName,
    KeyboardVariantName,
    LocaleInfo,
    RegionInfo,
    RegionOptions,
)
from arch_javid_installer.shell import (
    get_available_keyboard_layouts,
    get_disks_json,
    get_supported_locales,
    get_zones_for_region,
)


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


def get_language_options() -> list[LocaleInfo]:
    """Convert a list of supported locales to a list of language options."""
    language_options: list[LocaleInfo] = []
    for locale_line in get_supported_locales():
        locale_code, encoding = locale_line.split(maxsplit=1)

        if not encoding == "UTF-8":
            continue

        display_name = get_name_from_language_code(locale_code)
        language_options.append(LocaleInfo(code=locale_code, display_name=display_name))

    return sorted(language_options, key=lambda option: option.display_name)


def get_region_options() -> list[RegionInfo]:
    """Get a list of regions and their corresponding timezones."""
    region_options = [RegionInfo(region=region, zones=get_zones_for_region(region)) for region in RegionOptions]
    return sorted(region_options, key=lambda option: option.region)


def _keyboard_layout_parser(func: Callable) -> Callable:
    """Wrap a keyboard layout parser function."""
    _expected_len_parts = 2

    def wrapper(line: str) -> KeyboardModelName | KeyboardLayoutName | KeyboardVariantName | None:
        parts = line.split(maxsplit=1)
        if len(parts) != _expected_len_parts:
            return None
        parsed_line: KeyboardModelName | KeyboardLayoutName | KeyboardVariantName | None = func(parts) or None
        return parsed_line

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


def parse_keyboard_options(
    lines: list[str],
) -> tuple[list[KeyboardModelName], dict[KeyboardLayoutName, list[KeyboardVariantName]]]:
    """Get a list of keyboard models and a dict mapping layouts to their variants."""
    models: list[KeyboardModelName] = []
    layouts_dict: dict[KeyboardLayoutName, list[KeyboardVariantName]] = {}
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
                    layouts_dict[layout] = [
                        KeyboardVariantName(variant="default", layout=layout.layout, name="Default")
                    ]
            case KeyboardLayoutSectionMarkers.VARIANT:
                if variant := _parse_keyboard_variant_line(line):
                    layout = next((layout for layout in layouts_dict.keys() if layout.layout == variant.layout), None)
                    if layout is not None:
                        layouts_dict[layout].append(variant)

    return models, layouts_dict


def get_keyboard_options() -> tuple[list[KeyboardModelName], dict[KeyboardLayoutName, list[KeyboardVariantName]]]:
    """Get a list of keyboard models and a dict mapping layouts to their variants."""
    return parse_keyboard_options(get_available_keyboard_layouts())


def parse_disk_options(disks_json: str) -> DiskInfo:
    """Get a list of available disks and their partitions."""
    return DiskInfo(**json.loads(disks_json))


def get_disk_options() -> DiskInfo:
    """Get a list of available disks and their partitions."""
    return parse_disk_options(get_disks_json())
