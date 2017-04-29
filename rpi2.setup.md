#### Initial Setup
* Enter `sudo raspi-config`
* Change User Password
* Change hostname
* Change Boot Options to Console Autologin
* Change Locale > Add `en_US.UTF8`
* Change Timezone to `Indian Ocean > Maldives`
* Change Keyoard Layout to `Dell > Other > English (US) > English (US)`
* Interfacing Options > enable SSH and i2c
* Overclock to `Turbo`
* Advanced Options > Expand Filesystem
* Add network configuration at `/etc/wpa_supplicant/wpa_supplicant.conf` as below:
```
network={
    ssid="Tenda_5408C0"
    psk="password"
}
```
* Add `consoleblank=0` to the end of `/boot/cmdline.txt`
* Uncomment `LEDS=+num` in `/etc/kbd/config`
* `mkdir ~/.ssh`
* `sudo mkdir /root/.ssh`
* Add ssh keys to `~/.ssh/authorized_keys`
* Add ssh keys to `/root/.ssh/authorized_keys`
* Add `Acquire::http::Proxy "http://raspberrypi.local:3142";` to `/etc/apt/apt.conf.d/00proxy`
* `sudo apt-get autoremove --purge wolfram* sonic-pi libreoffice*`
* `sudo apt-get autoremove --purge`
* `sudo apt update`
* `sudo apt upgrade`
* `sudo apt dist-upgrade`
* `sudo apt install screen aria2 python-dev`
* `wget https://bootstrap.pypa.io/get-pip.py`
* `sudo python3 get-pip.py`
* `sudo python2 get-pip.py`
* `rm get-pip.py`
* `sudo pip3 uninstall -y chardet codebug-i2c-tether codebug-tether colorama Flask gpiozero html5lib itsdangerous Jinja2 MarkupSafe mcpi numpy pgzero picamera picraft pifacecommon pifacedigitalio pigpio Pillow pygame pygobject pyinotify pyOpenSSL pyserial python-apt python-debian RTIMULib sense-emu sense-hat smbus spidev twython urllib3 Werkzeug`
* `sudo pip2 uninstall -y blinker chardet colorama Flask gpiozero html5lib itsdangerous Jinja2 lxkeymap MarkupSafe mcpi ndg-httpsclient numpy picamera picraft pifacecommon pifacedigitalio pigpio Pillow pyasn1 pygame pygobject pyinotify pyOpenSSL pyserial python-apt RTIMULib sense-emu sense-hat smbus spidev twython urllib3 Werkzeug`
