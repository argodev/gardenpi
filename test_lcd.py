#!/usr/bin/python3
# -*- coding:utf-8 -*-

import board
import digitalio
import logging
import time
from datetime import datetime
import adafruit_character_lcd.character_lcd as characterlcd



def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI LCD Test **')
    start_time = time.time()

    rows = 2
    cols = 16

    lcd_rs = digitalio.DigitalInOut(board.D0)
    lcd_en = digitalio.DigitalInOut(board.D5)
    lcd_d4 = digitalio.DigitalInOut(board.D6)
    lcd_d5 = digitalio.DigitalInOut(board.D13)
    lcd_d6 = digitalio.DigitalInOut(board.D19)
    lcd_d7 = digitalio.DigitalInOut(board.D26)

    lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, cols, rows)

    lcd.clear()

    #lcd.message = "Hello\nWorld!!!"

    while True:
        lcd_line_1 = datetime.now().strftime('%b %d     %H:%M\n')
        lcd_line_2 = "74.3* 54.04% - +"
        lcd.message = lcd_line_1 + lcd_line_2
        time.sleep(2)

    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
