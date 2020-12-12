#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import logging
import gardenpi.utils as utils
from datetime import datetime
import board
from adafruit_seesaw.seesaw import Seesaw

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI Soil Moisture Test Utility Starting **')
    start_time = time.time()
    i2c = board.I2C()
    sensors = []
    mins = []
    maxs = []

    # load the config
    config = utils.load_config()

    if config['General'].getboolean('UseShelf1'):
        sensors.append(Seesaw(i2c, addr=int(config['Shelf1'].get('SSAddr', 0x0), 16)))
        mins.append(int(config['Shelf1'].get('SSMin', 200)))
        maxs.append(int(config['Shelf1'].get('SSMax', 2000)))
    if config['General'].getboolean('UseShelf2'):
        sensors.append(Seesaw(i2c, addr=int(config['Shelf2'].get('SSAddr', 0x0), 16)))
        mins.append(int(config['Shelf2'].get('SSMin', 200)))
        maxs.append(int(config['Shelf2'].get('SSMax', 2000)))
    if config['General'].getboolean('UseShelf3'):
        sensors.append(Seesaw(i2c, addr=int(config['Shelf3'].get('SSAddr', 0x0), 16)))
        mins.append(int(config['Shelf3'].get('SSMin', 200)))
        maxs.append(int(config['Shelf3'].get('SSMax', 2000)))

    # NOTE: 200 == very dry; 2000 == very wet
    while True:
        for idx, ss in enumerate(sensors):
            try:
                temp = utils.ctof(ss.get_temp())
                touch = ss.moisture_read()
                scaled = utils.scale_to_percent(touch, mins[idx], maxs[idx])
                print("Device: {}\tTemp: {:.1f} *F\tRaw: {}\tScaled: {:.2f}%".format(idx, temp, touch, scaled))
            except RuntimeError as e:
                print("Reading from SS failure: ", e.args)

        time.sleep(2)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
