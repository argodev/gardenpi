#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import logging
import RPi.GPIO as GPIO
import gardenpi.utils as utils

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI Relay Test Utility **')
    start_time = time.time()

    relay_sections = ['120VAC_Relay', '12VDC_Relay']
    pin_names = ['Port1', 'Port2', 'Port3', 'Port4']
    relay_pins = [17]

    # load the config
    #config = utils.load_config()

    #for section in relay_sections:
    #    for pin_name in pin_names:
    #        relay_pins.append(int(config[section][pin_name]))
    
    # initialize the pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pins, GPIO.OUT, initial=GPIO.HIGH)

    # infinite loop testing pins
    while True:
        for relay_pin in relay_pins:
            GPIO.output(relay_pin, GPIO.LOW)
            time.sleep(1)        
            GPIO.output(relay_pin, GPIO.HIGH)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
