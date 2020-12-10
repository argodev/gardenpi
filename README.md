# GardenPI

General Scripts supporting my indoor automated garden.

This will start off quite simple, and hopefully get a little more complex as we go on. As it stands currently, I have a RaspberryPi 3 B+ connected to a 4-port relay board that will control a lamp. There is also a camera installed that will take a picture once per day to help support a time-lapse view of the plants growing. I have a handful of sensors on the way and once they arrive, the system will begin to be more intelligent/automated.


## Parts List

| Part Number | Description                     |
|-------------|---------------------------------|
| [3775](http://adafru.it/3775)| Rasbperry Pi 3 B+ |
| [1995](http://adafru.it/1995) | 5V 2.5A Switching Power Supply |
| [PCF8523](http://adafru.it/3386) | Adafruit PiRTC - Real Time Clock for Raspberry Pi |
| [DHT22](http://adafru.it/385) | DHT22 temperature-humidity sensor + extras |
| [4026](http://adafru.it/4026) | Adafruit STEMMA Soil Sensor - I2C Capacitive Moisture Sensor |
| [101-70-101](https://amzn.to/3lCWbi3) | SainSmart 4-Channel Relay Module |
| [828](http://adafru.it/828) | Liquid Flow Meter - Plastic 1/2" NPS Threaded |
| [997](http://adafru.it/997) | Plastic Water Solenoid Valve - 12V - 1/2" Nominal |
| [Pi-SPi-PROTO](https://widgetlords.com/products/pi-spi-proto-raspberry-pi-prototyping-interface) | Pi-SPi-PROTO Raspberry Pi Prototyping Interface |
| [3099](http://adafru.it/3099) | Raspberry Pi Camera Board v2 - 8 Megapixels |


## PI Setup

In general, the software installation on the Raspberry Pi is fairly generic. However, there are a number of packges we install, as well as some important configuration changes we made in order to make things work as they should

### Base Installation

Grabbed the latest version of [Rasberry Pi OS](https://www.raspberrypi.org/software/). I used the "normal" desktop version (not Full), released 12/02/2020. I also used the Raspberry Pi Imager utility to "burn" the image to a 64 GB SD card.

After installation and configuration (WiFi, etc.), I updated the software to ensure it had the latest versions. I also installed some basic packages:

```bash
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install vim htop tmux build-essential git python-smbus i2c-tools
```

### Protocol/Interface Support

The next step is to enable the various protocols/kernel modules we will need to communicate with our collection of sensors. There are a few ways to do this, but using the in-build `raspi-config` utility is pretty easy. You can launch it by typing `sudo raspi-config` in a terminal. I then selected `Interface Options` (option 3). Here I stepped through and ensured that the following were all enabled:

* Camera
* SSH
* VNC
* I2C

You may choose to enable/disable different interfaces as fits your setup. In general, you want to enable only those you know you are going to need, and disable all of the rest. With this done, its a good idea to reboot and ensure the settings have been applied.

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


## TODO

Running list of items I still need to work on

1. make settings available via config/ini file
1. provide sample ini file in repo, make sure primary is excluded so it doesn't put secrets in src control
1. make simple service for linux + instructions on installation, start/stop/restart
1. make read water flow
1. integate with water valve
1. actually install on garden rack
1. clean up test scripts (LCD/OLED)
1. make screen/LCD optional via config file
1. work on documentation
1. set up requirements.txt and show installation


## Test Operation

Before you configure the garden code to run all the time, you will want to test it with different sensors and configuration information. You start by creating and configuring a `settings.ini` file (a sample file, `settings.sample.ini` is provided). Once this is done, you can run the various test scripts to ensure that your devices are connected properly and reporting data as intended.

### Settings

While this sounds somewhat redundant given the above, you can run the `test_config.py` script to confirm that your `settings.ini` file is where it needs to be, and that it can be read. This test simply reads the settings file and dumps all of the settings to the screen. The following is an excerpt of what you should see:

```bash
$ ./test_config.py 
[2020-12-10 16:18:31,507] INFO ** GardenPI Configuration Test Utility **
[2020-12-10 16:18:31,507] INFO Loading Configuration Information
[2020-12-10 16:18:31,510] INFO ** General **
[2020-12-10 16:18:31,510] INFO    statusloopdelay  -  10
[2020-12-10 16:18:31,511] INFO    primaryloopdelay  -  60
[2020-12-10 16:18:31,511] INFO    useinfluxdb  -  no
[2020-12-10 16:18:31,511] INFO    usemoisturesensor  -  Yes
[2020-12-10 16:18:31,512] INFO    usebay1  -  No
```

### Relays

Here, you simply test the relays and ensure that they are running as they should be. What this script does is read the relay info from the configuration file and then begin an infinite loop that simply walks through each relay turning each on for 1 second before turning it off and turning the next on. You terminate this script via `Ctrl+c`

```bash
$ ./test_relays.py 
[2020-12-10 16:56:02,430] INFO ** GardenPI Relay Test Utility **
[2020-12-10 16:56:02,431] INFO Loading Configuration Information
```

### Temperature/Humidity Sensors

With this test script, we evaluate the operation of our combined temperature/humidity sensor. The script supports up to three different garden bays and consequently three different sensors. The script will loop through and attempt to read each sensor before pausing for two seconds and then repeating.

```bash
$ ./test_temphumid.py 
[2020-12-10 17:19:36,307] INFO ** GardenPI Temperature/Humidity Test Utility **
[2020-12-10 17:19:36,307] INFO Loading Configuration Information
Device: 0       Temp: 60.1 *F   Humidity: 50.40%
Device: 0       Temp: 60.1 *F   Humidity: 50.30%
Device: 0       Temp: 60.1 *F   Humidity: 50.30%
```

### Soil Moisture Sensors
With this test script, we evaluate the operation of our soil mosisture sensors. The script supports up to three different garden bays and consequently three different sensors. The script will loop through and attempt to read each sensor before pausing for two seconds and then repeating. Additionally, it uses the calibration information from the config file to show the scaled measurement value.

```bash
$ ./test_soil.py 
[2020-12-10 17:39:19,204] INFO ** GardenPI Soil Moisture Test Utility Starting **
[2020-12-10 17:39:19,234] INFO Loading Configuration Information
Device: 0       Temp: 62.7 *F   Raw: 670        Scaled: 97.42%
Device: 0       Temp: 63.7 *F   Raw: 672        Scaled: 97.99%
Device: 0       Temp: 63.3 *F   Raw: 673        Scaled: 98.28%
Device: 0       Temp: 63.1 *F   Raw: 663        Scaled: 95.42%
```

## Normal Operation

