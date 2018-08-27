#!/bin/sh

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root (use sudo)"
  exit 1
fi

if [ "$1" = "" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "Usage: sudo ${0} filename.py"
  exit 0
fi

file="$1"

if [ ! -f "$file" ]; then
  echo "Error: $file not found!"
  exit 1
fi

service_name="$(echo "$file" | cut -d '.' -f 1)"
service_name="${service_name}.service"

echo "Stopping $service_name..."
sudo systemctl stop "$service_name"
echo "Disabling $service_name..."
sudo systemctl disable "$service_name"
echo "Removing $service_name..."
sudo rm /etc/systemd/system/"$service_name"
echo "========================="
