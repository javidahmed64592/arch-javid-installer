#!/bin/bash
set -euo pipefail

# Configure NVIDIA DRM modesetting + fbdev for Wayland/KDE (required on Linux 6.11+)
mkdir -p /etc/modprobe.d
echo "options nvidia_drm modeset=1 fbdev=1" > /etc/modprobe.d/nvidia.conf

# Preserve video memory across suspend/resume (required for Wayland suspend support)
echo "options nvidia NVreg_PreserveVideoMemoryAllocations=1" > /etc/modprobe.d/nvidia-power.conf

# Add NVIDIA modules to mkinitcpio for early loading
sed -i 's/^MODULES=.*/MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)/' /etc/mkinitcpio.conf
