"""Helper methods for the installer."""

from babel import Locale
from babel.core import UnknownLocaleError

from arch_javid_installer.models import RegionOptions
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


def get_regions_dict() -> dict[str, list[str]]:
    """Get a dictionary of regions and their corresponding timezones."""
    return {region: get_zones_for_region(region) for region in RegionOptions}
