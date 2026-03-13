"""Unit tests for the arch_javid_installer.main module."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication

from arch_javid_installer.installer_wizard import InstallerWizard
from arch_javid_installer.main import main


@pytest.fixture
def mock_q_application() -> Generator[QApplication]:
    """Mock the QApplication to prevent actual GUI from launching during tests."""
    with patch("arch_javid_installer.main.QApplication", autospec=True) as mock_app:
        yield mock_app


@pytest.fixture
def mock_installer_wizard() -> Generator[InstallerWizard]:
    """Mock the InstallerWizard to prevent actual GUI from launching during tests."""
    with patch("arch_javid_installer.main.InstallerWizard", autospec=True) as mock_wizard:
        yield mock_wizard


class TestMain:
    """Tests for the main function."""

    def test_main_runs_without_errors(
        self, mock_q_application: QApplication, mock_installer_wizard: InstallerWizard
    ) -> None:
        """Test that the main function runs without raising exceptions."""
        main()

        mock_installer_wizard.return_value.show.assert_called_once()
        mock_q_application.return_value.exec.assert_called_once()
