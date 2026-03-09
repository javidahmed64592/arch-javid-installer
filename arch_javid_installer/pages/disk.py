"""Disk page."""

from PySide6.QtWidgets import QComboBox, QLabel, QRadioButton, QVBoxLayout, QWizardPage


class DiskPage(QWizardPage):
    """Disk page of the installer."""

    def __init__(self) -> None:
        """Initialize the disk page."""
        super().__init__()

        self.setTitle("Disk Selection")

        layout = QVBoxLayout()

        # Disk selection
        self.disk = QComboBox()
        layout.addWidget(QLabel("Target:"))
        layout.addWidget(self.disk)

        disks = [
            "/dev/sda",
            "/dev/sdb",
        ]

        for disk in disks:
            self.disk.addItem(disk)

        layout.addWidget(self.disk)

        # Partitioning mode selection
        layout.addWidget(QLabel("Partitioning Mode:"))
        self.partition_mode_erase = QRadioButton("Erase disk")
        self.partition_mode_manual = QRadioButton("Manual partitioning")
        self.partition_mode_alongside = QRadioButton("Install alongside existing OS")

        layout.addWidget(self.partition_mode_erase)
        layout.addWidget(self.partition_mode_manual)
        layout.addWidget(self.partition_mode_alongside)

        self.setLayout(layout)
