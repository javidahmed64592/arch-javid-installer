"""Pydantic models for the installer."""

from __future__ import annotations

from enum import StrEnum, auto

from pydantic import BaseModel, Field


# Pre-installation models
class PagesEnum(StrEnum):
    """Enum for installer pages."""

    WELCOME = auto()
    LOCATION = auto()
    KEYBOARD = auto()
    DISK = auto()
    USER = auto()
    SUMMARY = auto()
    INSTALL = auto()
    FINISH = auto()

    @property
    def page_id(self) -> int:
        """Get the page ID for a given page enum."""
        return list(PagesEnum).index(self)


# Language model
class LocaleInfo(BaseModel):
    """Model for locale information."""

    code: str = Field(..., description="The locale code (e.g., 'en_GB.UTF-8').")
    display_name: str = Field(..., description="The display name of the locale (e.g., 'English (United Kingdom)').")


class LanguageChoice(BaseModel):
    """Model for language choice."""

    locale: LocaleInfo = Field(..., description="The locale information for the selected language.")


# Location models
class RegionOptions(StrEnum):
    """Enum for region options."""

    AFRICA = "Africa"
    AMERICA = "America"
    ANTARCTICA = "Antarctica"
    ARCTIC = "Arctic"
    ASIA = "Asia"
    ATLANTIC = "Atlantic"
    AUSTRALIA = "Australia"
    EUROPE = "Europe"
    INDIAN = "Indian"
    PACIFIC = "Pacific"


class RegionInfo(BaseModel):
    """Model for region information."""

    region: RegionOptions = Field(..., description="The name of the region.")
    zones: list[str] = Field(..., description="A list of timezones in the region.")


class LocationChoice(BaseModel):
    """Model for timezone and location."""

    region: RegionOptions = Field(..., description="The name of the region.")
    zone: str = Field(..., description="The name of the timezone.")


# Keyboard models
class KeyboardLayoutSectionMarkers(StrEnum):
    """Enum for keyboard layout section markers."""

    MODEL = "model"
    LAYOUT = "layout"
    VARIANT = "variant"


class KeyboardModelName(BaseModel):
    """Model for keyboard model names."""

    model_config = {"frozen": True}

    model: str = Field(..., description="The code of the keyboard model.")
    name: str = Field(..., description="The display name of the keyboard model.")


class KeyboardLayoutName(BaseModel):
    """Model for keyboard layout names."""

    model_config = {"frozen": True}

    layout: str = Field(..., description="The code of the keyboard layout.")
    name: str = Field(..., description="The display name of the keyboard layout.")


class KeyboardVariantName(BaseModel):
    """Model for keyboard variant names."""

    model_config = {"frozen": True}

    variant: str = Field(..., description="The code of the keyboard variant.")
    layout: str = Field(..., description="The code of the keyboard layout this variant belongs to.")
    name: str = Field(..., description="The display name of the keyboard variant.")


class KeyboardChoice(BaseModel):
    """Model for keyboard layout."""

    model: KeyboardModelName = Field(..., description="The name of the keyboard model.")
    layout: KeyboardLayoutName = Field(..., description="The name of the keyboard layout.")
    variant: KeyboardVariantName = Field(..., description="The name of the keyboard variant.")


# Disk models
class BlockDevice(BaseModel):
    """Model for a block device."""

    name: str = Field(..., description="The name of the block device.")
    size: str = Field(..., description="The size of the block device.")
    model: str | None = Field(None, description="The model of the disk.")
    label: str | None = Field(None, description="The label of the block device.")
    fstype: str | None = Field(None, description="The filesystem type of the block device.")
    mountpoint: str | None = Field(None, description="The mount point of the block device.")
    children: list[BlockDevice] = Field(default_factory=list, description="The partitions of the block device.")


class DiskInfo(BaseModel):
    """Model for disk information."""

    blockdevices: list[BlockDevice] = Field(..., description="A list of block devices and their partitions.")


class PartitionMode(StrEnum):
    """Enum for partitioning modes."""

    ERASE = auto()
    MANUAL = auto()
    ALONGSIDE = auto()


class DiskChoice(BaseModel):
    """Model for disk choice."""

    disk_to_use: BlockDevice = Field(..., description="The block device to use for installation.")
    partition_mode: PartitionMode = Field(..., description="The partitioning mode to use.")


# User models
class UserChoice(BaseModel):
    """Model for user choice."""

    computer_name: str = Field(..., description="The name of the computer.")
    username: str = Field(..., description="The name of the user.")
    password: str = Field(..., description="The password for the user.")
    root_password: str = Field(..., description="The password for the root user.")


# Installation configuration model
class InstallationConfig(BaseModel):
    """Model for the installation configuration."""

    language: LanguageChoice = Field(..., description="The language choice.")
    location: LocationChoice = Field(..., description="The timezone and location choice.")
    keyboard: KeyboardChoice = Field(..., description="The keyboard layout choice.")
    disk: DiskChoice = Field(..., description="The disk choice.")
    user: UserChoice = Field(..., description="The user choice.")
