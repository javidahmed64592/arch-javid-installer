#!/bin/bash
set -euo pipefail

# Script
echo "Running script: $0"

# Unmount partitions
echo "Unmounting partitions..."
umount -R /mnt
