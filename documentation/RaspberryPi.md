# Configuring the Raspberry Pi

It is likely that any modern Raspberry Pi would work for this project (it is not particularly compute intensive), but I happened to have a v3 B+ lying around and decided to use it. I grabbed the latest version of [Rasberry Pi OS](https://www.raspberrypi.org/software/). I used the "normal" desktop version (not Full), released 12/02/2020. I also used the Raspberry Pi Imager utility to "burn" the image to a 64 GB SD card (again, this is what I had lying around... an 8 GB card would have been fine).

After installation and configuration (WiFi, etc.), I updated the software to ensure it had the latest versions. 

I also installed some packages I knew I would need or find helpful:

```bash
sudo apt install vim htop tmux build-essential git tree i2c-tools
```

### Protocol/Interface Support

The next step is to enable the various protocols/kernel modules we will need to communicate with our collection of sensors. There are a few ways to do this, but using the in-build `raspi-config` utility is pretty easy. You can launch it by typing `sudo raspi-config` in a terminal. Specifically, I needed to enable:

* SSH
* VNC (not really needed, but I was experimenting with it)
* I2C

### WiFi Issues

One of the problems I had was that the Pi kept "disappearing" from the network. I am running it "headless", so this presents a problem. Each time, rebooting would immediately fix the issue. Doing some reasearch, it appears to be tied to the power management features enabled for the built-in WiFi adapter. The information online is contradictory (e.g. "this was fixed a few years ago"), but in my tests, it was still enabled and causing issues. I was able to confirm that power saving features were enabled by running the following command:

```bash
$ iw wlan0 get power_save
Power save: on
```

I then added the line `/sbin/iwconfig wlan0 power off` to my `/etc/rc.local` file (just prior to the last line that said `exit 0`) and rebooted. After reboot, I can confirm that power saving for the WiFi is disabled:

```bash
$ iw wlan0 get power_save
Power save: off
```

