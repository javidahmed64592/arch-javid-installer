#!/bin/bash
set -euo pipefail

# Script
echo "Running script: $0"

# Generate fstab
echo "Generating fstab..."
genfstab -U /mnt >> /mnt/etc/fstab
