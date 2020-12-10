#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import configparser


def load_config(config_file='settings.ini'):
    """
    Loads configuration file from disk
    """
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


def ctof(c):
    """
    Utility function to convert Celcius to Faranheit
    """
    f = ((c*9.0)/5.0) + 32
    return f


def scale_to_percent(val, min, max):
    """
    Utility function to scale a given value to a percentage within a range
    """
    current = val
    
    # first, ensure that current is within our defined min/max
    if val < min:
        current = min
    elif current > max:
        current = max

    # now, we scale it to b/t 0 and 1
    scaled = (current-min)/(max - min)

    return scaled * 100