#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import RPi.GPIO as GPIO
import gpiozero
import oled_pi
import board
import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw

# 120-VAC Relays
RELAY_120_01=14
RELAY_120_02=15
RELAY_120_03=18
RELAY_120_04=23

LIGHT_ON_HOUR=6
LIGHT_OFF_HOUR=21

# standard loop delay is 1 minute
LOOP_DELAY = 60

class GardenPi():

    def __init__(self):
        self._lcd = oled_pi.oled_pi()
        self._dht = adafruit_dht.DHT22(board.D24)
        self._i2c = board.I2C()
        self._ss = Seesaw(self._i2c, addr=0x36)
        self._min_soil = 330.0
        self._max_soil = 578.0
        #self.grow_light = gpiozero.OutputDevice(RELAY_120_01, active_high=False, initial_value=False)
        #self.grow_light_status = False

    # def _set_grow_light(self, status):
    #     if (status) and (not self.grow_light_status):
    #         logging.info("Turning on grow light")
    #         self.grow_light.on()
    #         self.grow_light_status = True
    #     elif (not status) and (self.grow_light_status):
    #         logging.info("Turning grow light off")
    #         self.grow_light.off()
    #         self.grow_light_status = False

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
                temperature = prev_temperature
                humidity = prev_humidity

            try:
                touch = self._ss.moisture_read()
                soil_temp = self._ss.get_temp()
            except:
                touch = prev_touch
                soil_temp = prev_soil_temp

            # TODO: should probably indicate if there was a sensor read error

            # build the display
            lcd_line_1 = "{:.1f}/{:.1f}% ".format(self._ctof(soil_temp), self._scale_moisture(touch)) + now.strftime('%H:%M')
            lcd_line_2 = "{:.1f} *F  {:.2f}%".format(self._ctof(temperature), humidity)        
            self._lcd.write_message(lcd_line_1, lcd_line_2)


        #     # control the grow light
        #     if (now.hour >= LIGHT_ON_HOUR) and (now.hour < LIGHT_OFF_HOUR):
        #         self._set_grow_light(True)
        #     else:
        #         self._set_grow_light(False)
            
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


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

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
