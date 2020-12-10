#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import logging
import configparser
import gardenpi.utils as utils

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI Configuration Test Utility **')
    start_time = time.time()

    config = utils.load_config()
    utils.dump_config(config)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))


if __name__ == '__main__':
    main()
