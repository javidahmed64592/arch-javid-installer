#!/bin/bash
set -euo pipefail

# Script
echo "Running script: $0"

# Enable services and rebuild initramfs
echo "Enabling services..."
systemctl enable NetworkManager
systemctl enable plasmalogin

# Rebuild initramfs to include NVIDIA modules
echo "Rebuilding initramfs..."
mkinitcpio -P linux
