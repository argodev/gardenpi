# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging

import gardenpi.utils as utils

import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO

class GardenShelf():

    def __init__(self, config, i2c):
        self._name = config.get('Name', '')
        self._dht = adafruit_dht.DHT22(int(config.get('DhtPin', 0)))
        self._light_pin = int(config.get('LightPin', 0))
        self._water_pin = int(config.get('WaterPin', 0))
        if config.getboolean('UseSS'):
            self._useSS = True
            self._soil_sensor = Seesaw(i2c, addr=int(config.get('SSAddr', 0x0), 16))
            self._soil_min = int(config.get('SSMin', 0))
            self._soil_max = int(config.get('SSMax', 0))
        else:
            self._useSS = False
        self._light_on = False
        self._water_on = False
        self._turn_light_on = int(config.get('LightOn', 0))
        self._turn_light_off = int(config.get('LightOff', 0))
        self._water_on_pct = int(config.get('MoistureOnPct',25))
        self._water_off_pct = int(config.get('MoistureOffPct', 75))
        self._prefix = config.get('Prefix', '')

        GPIO.setup(self._light_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self._water_pin, GPIO.OUT, initial=GPIO.HIGH)

        self.temperature = 0.0
        self.humidity = 0.0
        self.soil_temp = 0.0
        self.moisture = 0
        self.prev_temperature = 0.0
        self.prev_humidity = 0.0
        self.prev_moisture = 0.0
        self.prev_soil_temp = 0
        self.water = 0
        self.light = 0


    def _set_grow_light(self, status):
        """
        flips the light status
        """
        # control the device (always set, regardless of logging or not)
        if (status):
            GPIO.output(self._light_pin, GPIO.LOW) 
        else:
            GPIO.output(self._light_pin, GPIO.HIGH) 

        # log the info but guard with flag so we don't go overboard
        if (status and not self._light_on):
            logging.info("Turning grow light on")
            self._light_on = True
        elif (not status and self._light_on):
            logging.info("Turning grow light off")
            self._light_on = False


    def set_water_pump(self, status):
        """
        flips the water pump
        """
        # control the device (always set, regardless of logging or not)
        if (status):
            GPIO.output(self._water_pin, GPIO.LOW) 
        else:
            GPIO.output(self._water_pin, GPIO.HIGH) 

        # log the info but guard with flag so we don't go overboard
        if (status and not self._water_on):
            logging.info("Turning water pump on")
            self._water_on = True
        elif (not status and self._water_on):
            logging.info("Turning water pump off")
            self._water_on = False


    def scale_moisture(self, current):
        return utils.scale_to_percent(current, self._soil_min, self._soil_max)


    def major_loop(self, now):
        # TODO: read the water flow sensor
        # TODO: should probably indicate if there was a sensor read error

        try:
            self.temperature = self._dht.temperature
            self.humidity = self._dht.humidity
        except:
            logging.error("Unable to read temp/humidity sensor")
            self.temperature = self.prev_temperature
            self.humidity = self.prev_humidity

        try:
            if self._useSS:
                self.moisture = self._soil_sensor.moisture_read()
                self.soil_temp = self._soil_sensor.get_temp()
            else:
                self.moisture = 0
                self.soil_temp = 0
        except:
            logging.error("Unable to read soil moisture sensor")
            self.mosisture = self.prev_moisture
            self.soil_temp = self.prev_soil_temp

        # control the grow light
        if (now.hour >= self._turn_light_on) and (now.hour < self._turn_light_off):
            self._set_grow_light(True)
            self.light = 1
        else:
            self._set_grow_light(False)
            self.light = 0

        # control the water pump
        # if self._scale_moisture(self.mosisture) < self._water_on_pct:
        #     self._set_water_pump(True)
        #     self.water = 1
        # elif self._scale_moisture(touch) > self._water_off_pct:
        #     self._set_water_pump(False)
        #     self.water = 0
        # else:
        #     self.water = 1 if self._water_on else 0

        # store values for next loop
        self.prev_temperature = self.temperature
        self.prev_humidity = self.humidity
        self.prev_moisture = self.moisture
        self.prev_soil_temp = self.soil_temp


    def get_state(self):
        """
        returns the current state of the shelf (and sensors)
        based on the last main loop
        """
        state = {
            self._prefix + 'temp': self.temperature,
            self._prefix + 'humidity': self.humidity,
            self._prefix + 'soiltemp': self.soil_temp,
            self._prefix + 'moisture': self.moisture,
            self._prefix + 'water': self.water,
            self._prefix + 'light': self.light
        }

        return state
