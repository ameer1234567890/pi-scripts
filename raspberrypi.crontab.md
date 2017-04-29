@reboot /usr/bin/weavedstart.sh
*/5 * * * * sudo python3 /home/pi/pi-scripts/speedtest.py >> /tmp/speedtest.log 2>&1
* * * * * sudo python3 /home/pi/pi-scripts/pitemp.py >> /tmp/pitemp.log 2>&1
* * * * * sudo python3 /home/pi/pi-scripts/roomtemp.py >> /tmp/roomtemp.log 2>&1
* * * * * sudo python3 /home/pi/pi-scripts/light-sensor.py >> /tmp/light-sensor.log 2>&1
* * * * * sudo python /home/pi/pi-scripts/pistats.py >> /tmp/pistats.log 2>&1
