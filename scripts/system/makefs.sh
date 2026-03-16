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

# Make filesystems
echo "Creating FAT32 filesystem on EFI partition..."
mkfs.fat -F32 $EFI_PART

echo "Creating Btrfs filesystem on root partition..."
mkfs.btrfs $ROOT_PART
