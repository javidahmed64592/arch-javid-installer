#!/bin/bash
set -euo pipefail

# Variables
HOSTNAME=
USERNAME=
PASSWORD=
ROOT_PASSWORD=

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --hostname) HOSTNAME="$2"; shift 2 ;;
    --username) USERNAME="$2"; shift 2 ;;
    --password) PASSWORD="$2"; shift 2 ;;
    --root-password) ROOT_PASSWORD="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Validate required variables
if [[ -z "$HOSTNAME" || -z "$USERNAME" || -z "$PASSWORD" || -z "$ROOT_PASSWORD" ]]; then
  echo "Usage: $0 --hostname <hostname> --username <username> --password <password> --root-password <root_password>"
  exit 1
fi


echo ${HOSTNAME} > /etc/hostname
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers
echo "root:${ROOT_PASSWORD}" | chpasswd

useradd -m -G wheel -s /bin/bash ${USERNAME}
echo "${USERNAME}:${PASSWORD}" | chpasswd
