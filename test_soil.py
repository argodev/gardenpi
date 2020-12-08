#!/usr/bin/python3
# -*- coding:utf-8 -*-

import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
import logging
import time
from datetime import datetime

def ctof(c):
    f = ((c*9.0)/5.0) + 32
    return f

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    # NOTE: 200 == very dry; 2000 == very wet
    i2c = board.I2C()
    ss = Seesaw(i2c, addr=0x36)

    while True:
       
        touch = ss.moisture_read()
        temp = ss.get_temp()
        #print("temp: " + str(temp) + " moisture: " + str(touch))
        print("Temp: {:.1f} *F \t Moisture: {}".format(ctof(temp), touch))
        time.sleep(2)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
