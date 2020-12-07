#!/usr/bin/python3
# -*- coding:utf-8 -*-

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import logging
import time
from datetime import datetime

def main():
    """Primary entry point for the application"""
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI System Starting **')
    start_time = time.time()

    # init
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
   

    # clear the display
    oled.fill(0)
    oled.show()

    # create an image for drawing
    image = Image.new("1", (oled.width, oled.height))

    # get the drawing object to draw an image
    draw = ImageDraw.Draw(image)

    # draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # draw a smaller inner rectangle
    draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1), outline=0, fill=0)

    # load the default font
    font = ImageFont.load_default()

    # draw some text
    text = "Hello World!"
    (font_width, font_height) = font.getsize(text)
    draw.text((oled.width/2 - font_width/2, oled.height/2 - font_height/2), text, font=font, fill=255)

    oled.image(image)
    oled.show()

    time.sleep(5)

    # clear
    oled.fill(0)
    oled.show()
    
    all_on = False

    while True:
        
        # now, let's try to create something a little closer to what we intend to use
        if all_on:
            text = "Garden Pi v0.1\n" + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + "\n70.02 F    87.54%\nPump: ON   Light: ON"
        else:
            text = "Garden Pi v0.1\n" + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + "\n70.02 F    87.54%\nPump: --   Light: --"

        all_on = not all_on

        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        draw.text((2, 2), text, font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(1)




    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

if __name__ == '__main__':
    main()
