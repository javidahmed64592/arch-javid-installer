#!/bin/bash
set -euo pipefail

# Variables
DISK=
EFI_PART=
ROOT_PART=
EFI_SIZE=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --disk)      DISK="$2";      shift 2 ;;
    --efi-part)  EFI_PART="$2";  shift 2 ;;
    --root-part) ROOT_PART="$2"; shift 2 ;;
    --efi-size)  EFI_SIZE="$2";  shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "${DISK}" || -z "${EFI_PART}" || -z "${ROOT_PART}" || -z "${EFI_SIZE}" ]]; then
  echo "Usage: $0 --disk <disk> --efi-part <efi partition> --root-part <root partition> --efi-size <MiB>"
  exit 1
fi

# Script
echo "Running script: $0"
echo "Args: --disk ${DISK} --efi-part ${EFI_PART} --root-part ${ROOT_PART} --efi-size ${EFI_SIZE}"

# Calculate partition start/end in MiB
EFI_START=1
EFI_END=$((EFI_START + EFI_SIZE))
ROOT_START=$EFI_END
ROOT_END=100%
echo "Calculated partition layout:"
echo "EFI partition:  ${EFI_PART}, ${EFI_START}MiB - ${EFI_END}MiB"
echo "Root partition: ${ROOT_PART}, ${ROOT_START}MiB - ${ROOT_END}"

# Create GPT partition table and partitions
echo "Creating GPT partition table..."
parted "/dev/${DISK}" --script mklabel gpt

# EFI system partition
echo "Creating EFI system partition..."
parted "/dev/${DISK}" --script mkpart primary fat32 ${EFI_START}MiB ${EFI_END}MiB
parted "/dev/${DISK}" --script set 1 esp on

# Root partition
echo "Creating root partition..."
parted "/dev/${DISK}" --script mkpart primary btrfs ${ROOT_START}MiB ${ROOT_END}
