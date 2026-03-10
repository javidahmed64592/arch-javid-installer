"""Helper methods for the installer."""

from babel import Locale
from babel.core import UnknownLocaleError


# Pre-installation methods
def language_code_to_name(code: str) -> str:
    """Get the display name of a language code.

    Args:
        code: Locale code (e.g., 'en_US.UTF-8', 'en_US', or 'en').

    Returns:
        Human-readable language name (e.g., 'English (United States)').
        Returns the original code if parsing fails.
    """
    # Remove encoding suffix if present (e.g., 'en_US.UTF-8' -> 'en_US')
    locale_code = code.split(maxsplit=1)[0]
    if "." in locale_code:
        locale_code = locale_code.split(".", maxsplit=1)[0]

    try:
        locale = Locale.parse(locale_code, sep="_")
        # Get display name in English
        display_name = locale.get_display_name("en")
    except (UnknownLocaleError, ValueError):
        return locale_code
    else:
        return display_name if display_name else locale_code


def supported_locales_to_language_options(locales: list[str]) -> list[str]:
    """Convert a list of supported locales to a list of language options.

    Args:
        locales: List of locale strings from the supported locales file.
                Each line contains locale code and encoding (e.g., 'en_US.UTF-8 UTF-8').

    Returns:
        Sorted list of unique human-readable language names.
    """
    language_names = set()

    for locale_line in locales:
        # Skip empty lines and comments
        if not locale_line.strip() or locale_line.startswith("#"):
            continue

        # Extract locale code (first part before space)
        locale_code = locale_line.split(maxsplit=1)[0]

        # Convert to display name and add to set (automatically deduplicates)
        display_name = language_code_to_name(locale_code)
        language_names.add(display_name)

    # Return sorted list
    return sorted(language_names)
