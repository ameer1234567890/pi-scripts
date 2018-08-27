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
service_name="$service_name.service"

PART1=$(cat <<'END_HEREDOC'
[Unit]
Description=Custom service
After=network.target
[Service]
Environment=VIRTUAL_ENV=/home/pi/pi-scripts/env
WorkingDirectory=/home/pi/pi-scripts
ExecStart=/usr/bin/sudo /home/pi/pi-scripts/env/bin/python3 /home/pi/pi-scripts/
END_HEREDOC
)

PART2=$(cat <<'END_HEREDOC'
# we may not have network yet, so retry until success
Restart=on-failure
RestartSec=3s
[Install]
WantedBy=multi-user.target
END_HEREDOC
)

echo "Installing ${service_name}..."
echo "$PART1$file$PART2" > /etc/systemd/system/"$service_name"
echo "Enabling $service_name..."
systemctl enable "$service_name"
echo "Starting $service_name..."
systemctl start "$service_name"
echo "========================="
