#!/bin/bash
set -euo pipefail

# Variables
LOCALE=
REGION=
ZONE=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --locale) LOCALE="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --zone) ZONE="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "$LOCALE" || -z "$REGION" || -z "$ZONE" ]]; then
  echo "Usage: $0 --locale <locale> --region <region> --zone <zone>"
  exit 1
fi

ln -sf /usr/share/zoneinfo/${REGION}/${ZONE} /etc/localtime
hwclock --systohc

sed -i "s/^#${LOCALE}/${LOCALE}/" /etc/locale.gen
locale-gen
echo "LANG=${LOCALE}" > /etc/locale.conf
