#!/usr/bin/python3
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import logging
import time
from datetime import datetime
from subprocess import *


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI LCD Test **')
    start_time = time.time()

    rows = 2
    cols = 16

    OLED_D4 = 6
    OLED_D5 = 13
    OLED_D6 = 19
    OLED_D7 = 26
    OLED_RW = 12
    OLED_E = 5
    OLED_RS = 0

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(OLED_D4, GPIO.OUT)
    GPIO.setup(OLED_D5, GPIO.OUT)
    GPIO.setup(OLED_D6, GPIO.OUT)
    GPIO.setup(OLED_D7, GPIO.OUT)
    GPIO.setup(OLED_E, GPIO.OUT)
    GPIO.setup(OLED_RW, GPIO.OUT)
    GPIO.setup(OLED_RS, GPIO.OUT)

    GPIO.output(OLED_RW, False)






    while True:
        lcd_line_1 = datetime.now().strftime('%b %d     %H:%M\n')
        lcd_line_2 = "74.3* 54.04% - +"
        lcd.message = lcd_line_1 + lcd_line_2
        time.sleep(2)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
