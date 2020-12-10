#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import logging
import requests
import configparser

# standard loop delay is 1 minute
LOOP_DELAY = 60

#GPIO.setmode(GPIO.BCM)

def load_config(config_file='settings.ini'):
    logging.info("Loading Configuration Information")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def dump_config(config):
    """
    Utility function to dump the configuration information
    """
    for section in config.sections():
        logging.info("** %s **" % section)

        for key in config[section]:
            logging.info("   %s  -  %s" % (key, config[section][key]))


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI Config Tests **')
    start_time = time.time()

    config = load_config()
    dump_config(config)


    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))


if __name__ == '__main__':
    main()
