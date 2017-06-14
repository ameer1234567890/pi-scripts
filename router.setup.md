#### Technical Details
* Router Model: ZBT WR8305RT
* SOC: MediaTek MT7620N
* OpenWRT Page: https://wiki.openwrt.org/toh/zbt/wr8305rt

#### Notify on router startup (via IFTTT)
Add below line to `/etc/rc.local` or under Local Startup at System / Startup in LuCI
```shell
sleep 14
wget -O - http://maker.ifttt.com/trigger/router-reboot/with/key/hAVKuiLxTZFFNyiGtd1FubyVsOwTOHzWzJocBA0dCJs
```

#### Install the openssh-sftp-server package to install support for the SFTP protocol which SSHFS uses
```shell
opkg update
opkg install openssh-sftp-server
```

#### Enabling remote SSH access
1. Go to the System / Administration page.
2. Under “SSH Access”, for the default “Dropbear instance”, set “Interface” to “unspecified”.
3. Go to the Network / Firewall / Traffic Rules.
4. Scroll down to the “Open ports on router” section.
5. Enter a name for this rule, e.g. “Allow-SSH-WAN”.
6. Set “Protocol” to “TCP”.
7. Enter “22” as the “External Port”.
8. Click “Add”.
9. Click “Save and Apply”.

#### Enabling remote management
1. Go to the Network / Firewall / Port Forwards.
2. Scroll down to the “New port forward” section.
3. Enter a name for this rule, e.g. “luci-remote”.
4. Set “Protocol” to “TCP”.
5. Set “External zone” to “wan”
6. Set “External port” to “9999”
7. Enter “22” as the “External Port”.
8. Leave “Internal IP address” blank.
9. Enter “80” as the “Internal Port”.
10. Click “Add”.
11. Click “Save and Apply”.

#### Important Links
* Configure a guest WLAN: https://wiki.openwrt.org/doc/recipes/guest-wlan-webinterface
* Enabling remote management: https://aiotutorials.wordpress.com/2016/06/28/openwrt-remote-access/
