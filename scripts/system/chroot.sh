#!/bin/bash
set -euo pipefail

# Variables
SCRIPT_DIRECTORY=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --script-directory) SCRIPT_DIRECTORY="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "${SCRIPT_DIRECTORY}" ]]; then
  echo "Usage: $0 --script-directory <path to chroot scripts>"
  exit 1
fi

# Script
echo "Running script: $0"
echo "Args: --script-directory ${SCRIPT_DIRECTORY}"

# Copy chroot scripts to mounted root partition
echo "Copying chroot scripts to mounted root partition..."
mkdir -p "/mnt${SCRIPT_DIRECTORY}"
cp "${SCRIPT_DIRECTORY}/"*.sh "/mnt${SCRIPT_DIRECTORY}/"
