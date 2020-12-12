#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import configparser
import requests

import gardenpi.utils as utils
import gardenpi.shelf as shelf

from influxdb import InfluxDBClient

import board
import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO

import oled_pi

GPIO.setmode(GPIO.BCM)


class GardenPi():

    def __init__(self, config):
        if config['General'].getboolean('UseOLED'):
            self._oled = oled_pi.oled_pi(config['OLED'])
        else:
            self._oled = None
        self._i2c = board.I2C()
        self._shelves = []
        self._primary_delay = int(config['General'].get('PrimaryLoopDelay', 60))
        self._status_delay = int(config['General'].get('StatusLoopDelay', 10))

        if config['General'].getboolean('UseShelf1'):
            self._shelves.append(shelf.GardenShelf(config['Shelf1'], self._i2c))
            
        if config['General'].getboolean('UseShelf2'):
            self._shelves.append(shelf.GardenShelf(config['Shelf2'], self._i2c))

        if config['General'].getboolean('UseShelf3'):
            self._shelves.append(shelf.GardenShelf(config['Shelf3'], self._i2c))


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
        """
        This is the primary logic procesing loop for the garden controller
        This loop is run approximately every 1 minute
        """
        while True:
            now = datetime.now()
            # check the sensors
            for shelf in self._shelves:
                shelf.major_loop(now)

            try:
                readings = {
                    'timestamp' : str(datetime.utcnow().isoformat())
                }

                for shelf in self._shelves:
                    readings.update(shelf.get_state())

                # DEBUG
                print(readings)
                self._send_to_influxdb(readings)
                # TODO: send to adafruit.io!!!
            except Exception as err:
                logging.error("Unable to send data to InfluxDB")
                logging.error(err)

            # build the display
            if self._oled:
                # if we are using the display, our primary delay is made up
                # of some number of smaller status_delays
                remaining = self._primary_delay

                # build the screen/screens we are going to switch amongst
                while remaining > 0:
                    # each iteration should alternate between one of the
                    # generated sets
                    # lcd_line_1 = "{:.1f}/{:.1f}% ".format(self._ctof(soil_temp), self._scale_moisture(touch)) + now.strftime('%H:%M')
                    # lcd_line_2 = "{:.1f} *F  {:.2f}%".format(self._ctof(temperature), humidity)        
                    # self._lcd.write_message(lcd_line_1, lcd_line_2)

                    remaining -= self._status_delay
                    time.sleep(self._status_delay)
            else:
                # pause for awhile
                time.sleep(self._primary_delay)

    def cleanup(self):
        if self._oled:
            self._oled.clear_screen()


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    config = utils.load_config()

    garden = GardenPi(config)
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
