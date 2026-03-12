"""Disk page."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QRadioButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWizardPage,
)

from arch_javid_installer.models import BlockDevice, DiskInfo


class DiskPage(QWizardPage):
    """Disk page of the installer."""

    _na = "—"

    def __init__(self, disk_options: DiskInfo) -> None:
        """Initialize the disk page."""
        super().__init__()
        self._disk_options = disk_options

        self.setTitle("Disk Selection")

        layout = QVBoxLayout()

        # Disk selection
        layout.addWidget(QLabel("Target:"))
        self.disk = QComboBox()
        for device in self._disk_options.blockdevices:
            display = f"/dev/{device.name}  —  {device.size}"
            if device.model:
                display += f"  ({device.model})"
            self.disk.addItem(display, device)
        layout.addWidget(self.disk)

        # Disk details group
        self._details_group = QGroupBox("Disk Details")
        details_layout = QGridLayout()
        details_layout.setColumnStretch(1, 1)
        details_layout.setHorizontalSpacing(12)
        details_layout.setVerticalSpacing(4)

        self._model_value = DiskPage._value_label("")
        self._size_value = DiskPage._value_label("")
        self._label_value = DiskPage._value_label("")
        self._fstype_value = DiskPage._value_label("")
        self._mount_value = DiskPage._value_label("")

        row = 0
        for key, widget in [
            ("Model:", self._model_value),
            ("Size:", self._size_value),
            ("Label:", self._label_value),
            ("Filesystem:", self._fstype_value),
            ("Mount Point:", self._mount_value),
        ]:
            details_layout.addWidget(DiskPage._detail_label(key), row, 0)
            details_layout.addWidget(widget, row, 1)
            row += 1

        self._details_group.setLayout(details_layout)
        layout.addWidget(self._details_group)

        # Partition table
        self._partitions_group = QGroupBox("Partitions")
        partitions_layout = QVBoxLayout()

        self._partition_tree = QTreeWidget()
        self._partition_tree.setHeaderLabels(["Device", "Size", "FS Type", "Label", "Mount Point"])
        self._partition_tree.setRootIsDecorated(False)
        self._partition_tree.setAlternatingRowColors(True)
        self._partition_tree.setMaximumHeight(150)

        header = self._partition_tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        partitions_layout.addWidget(self._partition_tree)
        self._partitions_group.setLayout(partitions_layout)
        layout.addWidget(self._partitions_group)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # Partitioning mode selection
        layout.addWidget(QLabel("Partitioning Mode:"))
        self.partition_mode_erase = QRadioButton("Erase disk")
        self.partition_mode_manual = QRadioButton("Manual partitioning")
        self.partition_mode_alongside = QRadioButton("Install alongside existing OS")

        layout.addWidget(self.partition_mode_erase)
        layout.addWidget(self.partition_mode_manual)
        layout.addWidget(self.partition_mode_alongside)

        self.setLayout(layout)

        # Connect signal and show initial disk
        self.disk.currentIndexChanged.connect(self._on_disk_changed)
        if self._disk_options.blockdevices:
            self._on_disk_changed(0)

    def _on_disk_changed(self, index: int) -> None:
        """Update the detail panel when the selected disk changes."""
        device: BlockDevice = self.disk.itemData(index)
        if device is None:
            return

        self._model_value.setText(device.model or self._na)
        self._size_value.setText(device.size)
        self._label_value.setText(device.label or self._na)
        self._fstype_value.setText(device.fstype or self._na)
        self._mount_value.setText(device.mountpoint or self._na)

        has_partitions = bool(device.children)
        self._partitions_group.setVisible(has_partitions)
        if has_partitions:
            DiskPage._populate_partition_tree(self._partition_tree, device)

    @staticmethod
    def _format_device_path(name: str) -> str:
        """Format a block device name as a /dev/ path."""
        return f"/dev/{name}"

    @staticmethod
    def _detail_label(text: str) -> QLabel:
        """Create a right-aligned bold label for detail keys."""
        label = QLabel(f"<b>{text}</b>")
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label

    @staticmethod
    def _value_label(text: str) -> QLabel:
        """Create a left-aligned label for detail values."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label

    @staticmethod
    def _populate_partition_tree(tree: QTreeWidget, device: BlockDevice) -> None:
        """Populate the partition tree widget with the children of a block device."""
        tree.clear()
        for child in device.children:
            item = QTreeWidgetItem(
                [
                    DiskPage._format_device_path(child.name),
                    child.size,
                    child.fstype or "—",
                    child.label or "—",
                    child.mountpoint or "—",
                ]
            )
            tree.addTopLevelItem(item)
