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

sed -i '/^#\[multilib\]/{s/^#//;n;s/^#//}' "$PACMAN_CONF_FILEPATH"
pacman -Sy --noconfirm

PACKAGES=$(grep -v '^\s*#' "$PACKAGES_FILEPATH" | grep -v '^\s*$' | tr '\n' ' ')
pacstrap /mnt $PACKAGES
