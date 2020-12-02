#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import gpiozero

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
        self.grow_light = gpiozero.OutputDevice(RELAY_120_01, active_high=False, initial_value=False)
        self.grow_light_status = False

    def _set_grow_light(self, status):
        if (status) and (not self.grow_light_status):
            logging.info("Turning on grow light")
            self.grow_light.on()
            self.grow_light_status = True
        elif (not status) and (self.grow_light_status):
            logging.info("Turning grow light off")
            self.grow_light.off()
            self.grow_light_status = False

    def normal_loop(self):
        while True:
            now = datetime.now()

            # control the grow light
            if (now.hour >= LIGHT_ON_HOUR) and (now.hour < LIGHT_OFF_HOUR):
                self._set_grow_light(True)
            else:
                self._set_grow_light(False)
            
            # standard delay
            time.sleep(LOOP_DELAY)

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    garden = GardenPi()
    garden.normal_loop()

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
