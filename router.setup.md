#### Technical Details
* Router Model: ZBT WR8305RT
* SOC: MediaTek MT7620N
* OpenWRT Page: https://wiki.openwrt.org/toh/zbt/wr8305rt

#### Notify on router startup (via IFTTT)
Add below line to `/etc/rc.local` or under **_Local Startup_** in **_System > Startup_** in LuCI

```shell
sleep 14
wget -O - http://maker.ifttt.com/trigger/router-reboot/with/key/hAVKuiLxTZFFNyiGtd1FubyVsOwTOHzWzJocBA0dCJs
```

#### Important Links
* Replace Dropbear by openssh-server: https://wiki.openwrt.org/inbox/replacingdropbearbyopensshserver
* SFTP Server: https://wiki.openwrt.org/doc/howto/sftp.server
* Configure a guest WLAN: https://wiki.openwrt.org/doc/recipes/guest-wlan-webinterface
* Attach functions to a push button: https://wiki.openwrt.org/doc/howto/hardware.button
* Enabling remote SSH access: http://blog.differentpla.net/blog/2015/05/27/openwrt-ssh-wan
* Enabling remote management: https://aiotutorials.wordpress.com/2016/06/28/openwrt-remote-access/
