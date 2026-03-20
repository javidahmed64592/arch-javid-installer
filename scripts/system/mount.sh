#!/bin/bash
set -euo pipefail

# Variables
EFI_PART=
ROOT_PART=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --efi-part) EFI_PART="$2"; shift 2 ;;
    --root-part) ROOT_PART="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "$EFI_PART" || -z "$ROOT_PART" ]]; then
  echo "Usage: $0 --efi-part <efi partition> --root-part <root partition>"
  exit 1
fi

# Script
echo "Running script: $0"
echo "Args: --efi-part $EFI_PART --root-part $ROOT_PART"

# Mount partitions
echo "Mounting root partition..."
mount "/dev/$ROOT_PART" /mnt

echo "Mounting EFI partition..."
mkdir /mnt/boot
mount "/dev/$EFI_PART" /mnt/boot
