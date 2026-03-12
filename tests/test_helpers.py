"""Unit tests for the arch_javid_installer.helpers module."""

from arch_javid_installer.helpers import parse_disk_options, parse_keyboard_options
from arch_javid_installer.models import (
    BlockDevice,
    DiskInfo,
    KeyboardLayoutName,
    KeyboardModelName,
    KeyboardVariantName,
)


class TestKeyboardHelpers:
    """Unit tests for keyboard helper functions."""

    def test_parse_keyboard_options(self) -> None:
        """Test the parse_keyboard_options function."""
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


class TestDiskHelpers:
    """Unit tests for disk helper functions."""

    def test_parse_disk_options(self) -> None:
        """Test the parse_disk_options function."""
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

        disk_info = parse_disk_options(mock_disk_info.model_dump_json())
        assert disk_info == mock_disk_info
