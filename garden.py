#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import requests
import configparser
from influxdb import InfluxDBClient

#import gpiozero
import board
import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO

import oled_pi

# 120-VAC Relays
RELAY_120_01=17
RELAY_120_02=27
RELAY_120_03=22
RELAY_120_04=23

# 12-VDC Relays
RELAY_12_01=10
RELAY_12_02=9
RELAY_12_03=11
RELAY_12_04=8

# standard loop delay is 1 minute
LOOP_DELAY = 60

GPIO.setmode(GPIO.BCM)

class GardenPi():

    def __init__(self):
        self._lcd = oled_pi.oled_pi()
        self._dht = adafruit_dht.DHT22(board.D24)
        self._i2c = board.I2C()
        self._ss = Seesaw(self._i2c, addr=0x36)
        self._min_soil = 330.0
        self._max_soil = 578.0
        #self._grow_light = gpiozero.OutputDevice(RELAY_120_01, active_high=False, initial_value=False)
        GPIO.setup(RELAY_120_01, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(RELAY_12_01, GPIO.OUT, initial=GPIO.HIGH)
        self._grow_light_on = False
        self._water_on = False
        self._start_light_hour = 6
        self._stop_light_hour = 21

    def _set_grow_light(self, status):
        # control the device (always set, regardless of logging or not)
        if (status):
            GPIO.output(RELAY_120_01, GPIO.LOW) 
            # self._grow_light.on()
        else:
            GPIO.output(RELAY_120_01, GPIO.HIGH) 
            # self._grow_light.off()

        # log the info but guard with flag so we don't go overboard
        if (status and not self._grow_light_on):
            logging.info("Turning grow light on")
            self._grow_light_on = True
        elif (not status and self._grow_light_on):
            logging.info("Turning grow light off")
            self._grow_light_on = False


    def _set_water_pump(self, status):
        # control the device (always set, regardless of logging or not)
        if (status):
            GPIO.output(RELAY_12_01, GPIO.LOW) 
        else:
            GPIO.output(RELAY_12_01, GPIO.HIGH) 

        # log the info but guard with flag so we don't go overboard
        if (status and not self._water_on):
            logging.info("Turning water pump on")
            self._water_on = True
        elif (not status and self._water_on):
            logging.info("Turning water pump off")
            self._water_on = False


    def _scale_moisture(self, current):
        # first, ensure that current is within our defined min/max
        if current < self._min_soil:
            current = self._min_soil
        elif current > self._max_soil:
            current = self._max_soil

        # now, we scale it to b/t 0 and 1
        scaled = (current-self._min_soil)/(self._max_soil - self._min_soil)

        return scaled * 100


    def _ctof(self, c):
        f = ((c*9.0)/5.0) + 32
        return f

    def _send_to_influxdb(self, data):
        """Helper to package and send to influxdb"""
        user = ''
        password = ''
        dbname = ''
        host = ''
        port = 8086

        json_body = [{
            "measurement": "gardenpi",
            "time": datetime.utcnow().isoformat(),
        }]

        json_body[0]['fields'] = data

        try:
            client = InfluxDBClient(host, port, user, password, dbname)
            client.write_points(json_body)
            client.close()
        except requests.exceptions.ConnectionError as err:
            logging.warning("Unable to post to InfluxDB")
            logging.warning(err)


    def normal_loop(self):
        prev_temperature = 0
        prev_humidity = 0
        prev_touch = 0
        prev_soil_temp = 0

        while True:

            # check the sensors
            now = datetime.now()
            try:
                temperature = self._dht.temperature
                humidity = self._dht.humidity
            except:
                logging.error("Unable to read temp/humidity sensor")
                temperature = prev_temperature
                humidity = prev_humidity

            try:
                touch = self._ss.moisture_read()
                soil_temp = self._ss.get_temp()
            except:
                logging.error("Unable to read soil moisture sensor")
                touch = prev_touch
                soil_temp = prev_soil_temp

            # TODO: read the water flow sensor

            # TODO: should probably indicate if there was a sensor read error


            # control the grow light
            if (now.hour >= self._start_light_hour) and (now.hour < self._stop_light_hour):
                self._set_grow_light(True)
                light = 1
            else:
                self._set_grow_light(False)
                light = 0

            # control the water pump
            if self._scale_moisture(touch) < 25:
                self._set_water_pump(True)
                water = 1
            elif self._scale_moisture(touch) > 75:
                self._set_water_pump(False)
                water = 0
            else:
                water = 1 if self._water_on else 0

            # build the display
            lcd_line_1 = "{:.1f}/{:.1f}% ".format(self._ctof(soil_temp), self._scale_moisture(touch)) + now.strftime('%H:%M')
            lcd_line_2 = "{:.1f} *F  {:.2f}%".format(self._ctof(temperature), humidity)        
            self._lcd.write_message(lcd_line_1, lcd_line_2)

            try:
                readings = {
                    'timestamp' : str(datetime.utcnow().isoformat()),
                    'bay_2_temp': temperature,
                    'bay_2_humidity': humidity,
                    'bay_2_soil_temp': soil_temp,
                    'bay_2_moisture': touch,
                    'bay_2_water': water,
                    'bay_2_light': light
                }

                self._send_to_influxdb(readings)
            except Exception as err:
                logging.error("Unable to send data to InfluxDB")
                logging.error(err)


            
            # store values for next loop
            prev_temperature = temperature
            prev_humidity = humidity
            prev_touch = touch
            prev_soil_temp = soil_temp


            # pause for awhile
            time.sleep(LOOP_DELAY)

    def cleanup(self):
        if self._lcd:
            self._lcd.clear_screen()


def load_config(config_file='settings.ini'):
    logging.info("Loading Configuration Information")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def dump_config(config):
    """
    Utility function to dump the configuration information
    """


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    config = load_config()
    dump_config(config)

    # for test/debug!
    return

    garden = GardenPi()
    try:
        garden.normal_loop()
    finally:
        garden.cleanup()

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
