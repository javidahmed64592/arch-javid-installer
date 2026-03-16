#!/bin/bash
set -euo pipefail

# Script
echo "Running script: $0"

# Configure NVIDIA DRM modesetting + fbdev for Wayland/KDE
echo "Configuring NVIDIA DRM modesetting and framebuffer support..."
mkdir -p /etc/modprobe.d
echo "options nvidia_drm modeset=1 fbdev=1" > /etc/modprobe.d/nvidia.conf

# Preserve video memory across suspend/resume
echo "Configuring NVIDIA power management..."
echo "options nvidia NVreg_PreserveVideoMemoryAllocations=1" > /etc/modprobe.d/nvidia-power.conf

# Add NVIDIA modules to mkinitcpio for early loading
echo "Adding NVIDIA modules to initramfs..."
sed -i 's/^MODULES=.*/MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)/' /etc/mkinitcpio.conf
