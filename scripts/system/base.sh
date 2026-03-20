#!/bin/bash
set -euo pipefail

# Variables
PACMAN_CONF_FILEPATH=
PACKAGES_FILEPATH=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --pacman-conf)      PACMAN_CONF_FILEPATH="$2";     shift 2 ;;
    --packages)  PACKAGES_FILEPATH="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "$PACMAN_CONF_FILEPATH" || -z "$PACKAGES_FILEPATH" ]]; then
  echo "Usage: $0 --pacman-conf <path> --packages <path>"
  exit 1
fi

# Script
echo "Running script: $0"
echo "Args: --pacman-conf $PACMAN_CONF_FILEPATH --packages $PACKAGES_FILEPATH"

# Enable multilib repository and update package database
echo "Enabling multilib repository..."
sed -i '/^#\[multilib\]/{s/^#//;n;s/^#//}' "$PACMAN_CONF_FILEPATH"
pacman -Sy --noconfirm

# Install packages
echo "Installing packages..."
PACKAGES=$(grep -v '^\s*#' "$PACKAGES_FILEPATH" | grep -v '^\s*$' | tr '\n' ' ')
pacstrap /mnt $PACKAGES
