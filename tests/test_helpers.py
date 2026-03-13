"""Unit tests for the arch_javid_installer.helpers module."""

from unittest.mock import patch

import pytest

from arch_javid_installer.helpers import (
    get_disk_options,
    get_keyboard_options,
    get_language_options,
    get_name_from_language_code,
    get_region_options,
    parse_disk_options,
    parse_keyboard_options,
)
from arch_javid_installer.models import (
    BlockDevice,
    DiskInfo,
    KeyboardLayoutName,
    KeyboardModelName,
    KeyboardVariantName,
    RegionOptions,
)


class TestLanguageHelpers:
    """Unit tests for language helper functions."""

    def test_get_name_from_language_code(self) -> None:
        """Test the get_name_from_language_code function."""
        assert get_name_from_language_code("en_GB.UTF-8") == "English (United Kingdom)"
        assert get_name_from_language_code("invalid_code") == "invalid_code"

    def test_get_language_options(self) -> None:
        """Test the get_language_options function."""
        mock_locales = [
            "en_GB.UTF-8 UTF-8",
            "en_GB ISO-8859-1",
            "en_US.UTF-8 UTF-8",
            "en_US ISO-8859-1",
        ]
        with patch("arch_javid_installer.helpers.get_supported_locales", return_value=mock_locales):
            language_options = get_language_options()
            assert len(language_options) == len(mock_locales) // 2
            assert language_options[0].code == "en_GB.UTF-8"
            assert language_options[0].display_name == "English (United Kingdom)"
            assert language_options[1].code == "en_US.UTF-8"
            assert language_options[1].display_name == "English (United States)"


class TestRegionHelpers:
    """Unit tests for region helper functions."""

    def test_get_region_options(self) -> None:
        """Test the get_region_options function."""
        mock_zones_for_region = {region: [f"{region.value}/Zone{i}" for i in range(1, 4)] for region in RegionOptions}
        with patch(
            "arch_javid_installer.helpers.get_zones_for_region",
            side_effect=lambda region: mock_zones_for_region[region],
        ):
            region_options = get_region_options()
            assert len(region_options) == len(mock_zones_for_region)
            for region_info in region_options:
                assert region_info.region.value in mock_zones_for_region
                assert region_info.zones == mock_zones_for_region[region_info.region.value]


class TestKeyboardHelpers:
    """Unit tests for keyboard helper functions."""

    @pytest.fixture
    def mock_keyboard_data(self) -> tuple[list[KeyboardModelName], list[KeyboardLayoutName], list[KeyboardVariantName]]:
        """Fixture for mock keyboard data."""
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
        return mock_models, mock_layouts, mock_variants

    @pytest.fixture
    def mock_layouts_file_content(
        self, mock_keyboard_data: tuple[list[KeyboardModelName], list[KeyboardLayoutName], list[KeyboardVariantName]]
    ) -> list[str]:
        """Fixture for mock keyboard layouts file content."""
        mock_models, mock_layouts, mock_variants = mock_keyboard_data

        def _mock_model_line(model: KeyboardModelName) -> str:
            return f"  {model.model}            {model.name}\n"

        def _mock_layout_line(layout: KeyboardLayoutName) -> str:
            return f"  {layout.layout}              {layout.name}\n"

        def _mock_variant_line(variant: KeyboardVariantName) -> str:
            return f"  {variant.variant}            {variant.layout}: {variant.name}\n"

        return [
            "! model\n",
            *[_mock_model_line(model) for model in mock_models],
            "\n",
            "! layout\n",
            *[_mock_layout_line(layout) for layout in mock_layouts],
            "\n",
            "! variant\n",
            *[_mock_variant_line(variant) for variant in mock_variants],
        ]

    def test_parse_keyboard_options(
        self,
        mock_keyboard_data: tuple[list[KeyboardModelName], list[KeyboardLayoutName], list[KeyboardVariantName]],
        mock_layouts_file_content: list[str],
    ) -> None:
        """Test the parse_keyboard_options function."""
        mock_models, mock_layouts, mock_variants = mock_keyboard_data

        models, layouts_dict = parse_keyboard_options(mock_layouts_file_content)
        assert models == mock_models
        assert list(layouts_dict.keys()) == mock_layouts
        assert layouts_dict[mock_layouts[0]] == [
            KeyboardVariantName(variant="default", layout=mock_layouts[0].layout, name="Default"),
            *mock_variants,
        ]
        assert layouts_dict[mock_layouts[1]] == [
            KeyboardVariantName(variant="default", layout=mock_layouts[1].layout, name="Default")
        ]

    def test_get_keyboard_options(self, mock_layouts_file_content: list[str]) -> None:
        """Test the get_keyboard_options function."""
        models, layouts_dict = parse_keyboard_options(mock_layouts_file_content)

        with patch(
            "arch_javid_installer.helpers.get_available_keyboard_layouts", return_value=mock_layouts_file_content
        ):
            assert get_keyboard_options() == (models, layouts_dict)


class TestDiskHelpers:
    """Unit tests for disk helper functions."""

    @pytest.fixture
    def mock_disks_json(self) -> str:
        """Fixture for mock disks JSON."""
        mock_blockdevices = [
            BlockDevice(
                name="sda",
                size="100G",
                model="Mock Disk 1",
                label=None,
                fstype=None,
                mountpoint=None,
                children=[
                    BlockDevice(
                        name="sda1",
                        size="2G",
                        model=None,
                        label=None,
                        fstype="vfat",
                        mountpoint="/boot",
                    ),
                    BlockDevice(
                        name="sda2",
                        size="98G",
                        model=None,
                        label=None,
                        fstype="btrfs",
                        mountpoint="/mock/var/tmp",
                    ),
                ],
            ),
            BlockDevice(
                name="sdb",
                size="200G",
                model="Mock Disk 2",
                label="MockDisk2",
                fstype="ext4",
                mountpoint="/home/mockdisk2",
            ),
        ]
        mock_disk_info = DiskInfo(blockdevices=mock_blockdevices)
        return mock_disk_info.model_dump_json()

    def test_parse_disk_options(self, mock_disks_json: str) -> None:
        """Test the parse_disk_options function."""
        disk_info = parse_disk_options(mock_disks_json)
        assert isinstance(disk_info, DiskInfo)
        assert disk_info == DiskInfo.model_validate_json(mock_disks_json)

    def test_get_disk_options(self, mock_disks_json: str) -> None:
        """Test the get_disk_options function."""
        disk_info = parse_disk_options(mock_disks_json)
        with patch("arch_javid_installer.helpers.get_disks_json", return_value=mock_disks_json):
            assert get_disk_options() == disk_info
