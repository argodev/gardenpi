# Sesnsors and Devices

This page explains the various settings we make for each of the sensors

## Real-Time Clock 

We start by running `sudo i2cdetect -y 1` to confirm that the device is connected and talking. Amongst others, we should see device `68` appear. If we see `UU`, that means the kernel driver is already configured and we are also good.

Next, we edit `/boot/config.txt` and add `dtoverlay=i2c-rtc,pcf8523` to the end of the file. Reboot the device to apply the changes.

Now, we re-run the detection to confirm that we see `UU` where the device `68` really should be. This means it is set up properly.

Next, we remove support for the fake hardware clock as it causes issue with the real hardware clock

```bash
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock
```

Now, with that disabled, we can enable the actual clock. We edit the file `/lib/udev/hwclock-set`. We comment out the following lines:

```text
if [ -e /run/systemd/system ] ; then
    exit 0
fi

/sbin/hwclock --rtc=$dev --systz --badyear

/sbin/hwclock --rtc=$dev --systz
```

We can read the time from the HW clock via `sudo hwclock -r`. We can compare this to the PI's network time by running `date`. If there is a discrepncy (first time it is connected, the HW clock will likely not have the right time), we can write from the pi to the RTC as follows: `sudo hwclock -w`