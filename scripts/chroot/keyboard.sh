#!/bin/bash
set -euo pipefail

# Variables
MODEL=
LAYOUT=
VARIANT=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --layout) LAYOUT="$2"; shift 2 ;;
    --variant) VARIANT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "$MODEL" || -z "$LAYOUT" || -z "$VARIANT" ]]; then
  echo "Usage: $0 --model <model> --layout <layout> --variant <variant>"
  exit 1
fi

# Script
echo "Running script: $0"
echo "Args: --model $MODEL --layout $LAYOUT --variant $VARIANT"

# Set keyboard layout
echo "Setting keyboard layout..."

# Set console keyboard layout
echo "KEYMAP=${LAYOUT}" > /etc/vconsole.conf

# Set X11 keyboard layout
args="${LAYOUT} ${MODEL}"
if [[ "$VARIANT" != "default" ]]; then
  args+=" ${VARIANT}"
fi
localectl set-x11-keymap ${args}
