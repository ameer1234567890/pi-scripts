#!/bin/sh
if [ "$1" = "r" ]; then
  echo "Switching to RCA..."
  new_config="$(< /boot/config.txt sed 's/.*hdmi_ignore_hotplug=.*/hdmi_ignore_hotplug=1/g')"
  echo "$new_config" > /boot/config.txt
  echo "Rebooting..."
  reboot
elif [ "$1" = "h" ]; then
  echo "Switching to HDMI..."
  new_config="$(< /boot/config.txt sed 's/.*hdmi_ignore_hotplug=.*/#hdmi_ignore_hotplug=1/g')"
  echo "$new_config" > /boot/config.txt
  echo "Rebooting...."
  reboot
else
  echo "Usage: d [r|h]"
fi
