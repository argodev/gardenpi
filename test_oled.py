#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import logging
import gardenpi.utils as utils
import gardenpi.oled_pi as oled_pi
from datetime import datetime


def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI OLED Test **')
    start_time = time.time()

    # load the config
    config = utils.load_config()

    if config['General'].getboolean('UseOLED'):
        lcd = oled_pi.oled_pi(config['OLED'])

        try:
            while True:
                lcd_line_1 = datetime.now().strftime('%b %d     %H:%M\n')
                lcd_line_2 = "75.3* 54.04% - +"
                
                lcd.write_message(lcd_line_1, lcd_line_2)
                time.sleep(2)
        finally:
            lcd.clear_screen()
    else:
        logging.error("Not configured to use OLED. Exiting now")

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
