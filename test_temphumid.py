#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import logging
import gardenpi.utils as utils
import board
import adafruit_dht


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI Temperature/Humidity Test Utility **')
    start_time = time.time()
    dhts = []

    # load the config
    config = utils.load_config()

    if config['General'].getboolean('UseBay1'):
        dhts.append(adafruit_dht.DHT22(int(config['Bay1'].get('DhtPin', 0))))
    if config['General'].getboolean('UseBay2'):
        dhts.append(adafruit_dht.DHT22(int(config['Bay2'].get('DhtPin', 0))))
    if config['General'].getboolean('UseBay3'):
        dhts.append(adafruit_dht.DHT22(int(config['Bay3'].get('DhtPin', 0))))

    while True:
        for idx, dht in enumerate(dhts):
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                print("Device: {}\tTemp: {:.1f} *F\tHumidity: {:.2f}%".format(idx, utils.ctof(temperature), humidity))
            except RuntimeError as e:
                # Reading doesn't always work! Just print error and we'll try again
                print("Reading from DHT failure: ", e.args)
    
        time.sleep(2)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))


if __name__ == '__main__':
    main()
