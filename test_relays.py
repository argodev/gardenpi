#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import gpiozero

# 120-VAC Relays
RELAY_120_01=17
RELAY_120_02=27
RELAY_120_03=22
RELAY_120_04=23
RELAY_12_01=10
RELAY_12_02=9
RELAY_12_03=11
RELAY_12_04=8



def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    # init
    r11 = gpiozero.OutputDevice(RELAY_120_01, active_high=False, initial_value=False)
    r12 = gpiozero.OutputDevice(RELAY_120_02, active_high=False, initial_value=False)
    r13 = gpiozero.OutputDevice(RELAY_120_03, active_high=False, initial_value=False)
    r14 = gpiozero.OutputDevice(RELAY_120_04, active_high=False, initial_value=False)
    r21 = gpiozero.OutputDevice(RELAY_12_01, active_high=False, initial_value=False)
    r22 = gpiozero.OutputDevice(RELAY_12_02, active_high=False, initial_value=False)
    r23 = gpiozero.OutputDevice(RELAY_12_03, active_high=False, initial_value=False)
    r24 = gpiozero.OutputDevice(RELAY_12_04, active_high=False, initial_value=False)

    # loop through
    while True:
        r11.on()
        time.sleep(1)
        r11.off()
        r12.on()
        time.sleep(1)
        r12.off()
        r13.on()
        time.sleep(1)
        r13.off()
        r14.on()
        time.sleep(1)
        r14.off()
        r21.on()
        time.sleep(1)
        r21.off()
        r22.on()
        time.sleep(1)
        r22.off()
        r23.on()
        time.sleep(1)
        r23.off()
        r24.on()
        time.sleep(1)
        r24.off()


    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
