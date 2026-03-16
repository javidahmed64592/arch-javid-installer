"""Install page."""

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QLabel, QProgressBar, QTextEdit, QVBoxLayout, QWizard, QWizardPage

from arch_javid_installer.installer_engine import InstallerEngine


class InstallPage(QWizardPage):
    """Install page of the installer."""

    def __init__(self, title: str) -> None:
        """Initialize the install page."""
        super().__init__()
        self.setTitle(title)

        # UI Components
        self.status_label = QLabel("Preparing installation...")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setMinimumHeight(300)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Installation Log:"))
        layout.addWidget(self.log_viewer)

        self.setLayout(layout)

        # Thread and engine (initialized in initializePage)
        self.worker_thread: QThread | None = None
        self.installer_engine: InstallerEngine | None = None
        self.installation_success = False

    def initializePage(self) -> None:  # noqa: N802
        """Start the installation when the page is entered."""
        # Disable wizard buttons
        wizard = self.wizard()
        wizard.button(QWizard.WizardButton.BackButton).setEnabled(False)
        wizard.button(QWizard.WizardButton.NextButton).setEnabled(False)
        wizard.button(QWizard.WizardButton.CancelButton).setEnabled(False)

        # Reset UI
        self.status_label.setText("Starting installation...")
        self.progress_bar.setValue(0)
        self.log_viewer.clear()
        self.installation_success = False

        # Create installer engine and thread
        self.worker_thread = QThread()
        self.installer_engine = InstallerEngine(config=wizard.installation_config)  # type: ignore[attr-defined]

        # Move installer to thread
        self.installer_engine.moveToThread(self.worker_thread)

        # Connect signals
        self.worker_thread.started.connect(self.installer_engine.run)
        self.installer_engine.progress_updated.connect(self._on_progress_updated)
        self.installer_engine.log_message.connect(self._on_log_message)
        self.installer_engine.installation_complete.connect(self._on_installation_complete)
        self.installer_engine.installation_complete.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self._cleanup_thread)

        # Start installation
        self.worker_thread.start()

    def _on_progress_updated(self, progress: int) -> None:
        """Update progress bar when progress changes."""
        self.progress_bar.setValue(progress)

    def _on_log_message(self, message: str) -> None:
        """Append log message to the log viewer."""
        self.log_viewer.append(message)
        self.status_label.setText(message)

    def _on_installation_complete(self, success: bool) -> None:  # noqa: FBT001
        """Handle installation completion."""
        self.installation_success = success

        wizard = self.wizard()
        if success:
            self.status_label.setText("Installation completed successfully!")
            wizard.button(QWizard.WizardButton.NextButton).setEnabled(True)
        else:
            self.status_label.setText("Installation failed. Please check the logs.")
            wizard.button(QWizard.WizardButton.CancelButton).setEnabled(True)

    def _cleanup_thread(self) -> None:
        """Clean up the worker thread."""
        if self.worker_thread:
            self.worker_thread.deleteLater()
            self.worker_thread = None
        if self.installer_engine:
            self.installer_engine.deleteLater()
            self.installer_engine = None

    def isComplete(self) -> bool:  # noqa: N802
        """Return True when installation is successfully completed."""
        return self.installation_success
