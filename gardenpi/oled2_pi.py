#!/usr/bin/python3
# -*- coding:utf-8 -*-

# this is a python-adaptation of https://github.com/ladyada/Adafruit_CharacterOLED
#
# Derived from LiquidCrystal by David Mellis
# with portions adapted from Elco Jacobs OLEDFourBit
# Modified for 4-bit operation of the Winstar 16x2 Character OLED
# by W. Earl for Adafruit - 6/30/12
# Initialization sequence fixed by Technobly - 9/22/2013
#
# Ported to Python by argodev - 12/18/2020
#
# On power up, the display is initilaized as:
# 1. Display clear
# 2. Function set:
#    DL="1": 8-bit interface data
#    N="0": 1-line display
#    F="0": 5 x 8 dot character font
# 3. Power turn off
#    PWR="0"
# 4. Display on/off control: D="0": Display off C="0": Cursor off B="0": Blinking off
# 5. Entry mode set
#    I/D="1": Increment by 1
#    S="0": No shift
# 6. Cursor/Display shift/Mode / Pwr
#    S/C="0", R/L="1": Shifts cursor position to the right
#    G/C="0": Character mode
#    Pwr="1": Internal DCDC power on
#
# Note, however, that resetting the Arduino doesn't reset the LCD, so we
# can't assume that its in that state when a sketch starts (and the
# LiquidCrystal constructor is called).
#

import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging

# OLED hardware versions
OLED_V1 = 0x01
OLED_V2 = 0x02

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x28
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_JAPANESE = 0x00
LCD_EUROPEAN_I = 0x01
LCD_RUSSIAN = 0x02
LCD_EUROPEAN_II = 0x03

class oled2_pi():
    
    def __init__(self, ver, rs, rw, en, d4, d5, d6, d7):
        logging.info("Initializing OLED")
        # Configure the GPIO to drive the LCD display correctly
        GPIO.setmode(GPIO.BCM)             # Use BCM GPIO numbers

        # OLED_V1 == older, OLED_V2 == newer hardware version
        self._oled_ver = ver
        if (self._oled_ver != OLED_V1 and self._oled_ver != OLED_V2):
            #if error, default to newer version
            self._oled_ver = OLED_V2
        # LOW: command. HIGH: character.
        self._rs_pin = rs
        # LOW: write to LCD. HIGH: read from LCD.
        self._rw_pin = rw
        # activated by a HIGH pulse
        self._enable_pin = enable

        self._data_pins = []
        self._data_pins.append(d4)
        self._data_pins.append(d5)
        self._data_pins.append(d6)
        self._data_pins.append(d7)
        # HIGH means not ready for next command
        self._busy_pin = d7

        GPIO.setup(self._rs_pin, GPIO.OUT)
        GPIO.setup(self._rw_pin, GPIO.OUT)
        GPIO.setup(self._enable_pin, GPIO.OUT)
        
        self._displayfunction = LCD_FUNCTIONSET | LCD_4BITMODE
        self._numlines = 16
        self._currline = 0
        self._initialized = False
        self._displaycontrol = 0
        self._displaymode = -1

        self.begin(self._numlines, 2)


    def begin(self, cols, rows, character_set=LCD_JAPANESE):
        self._numlines = lines
        self._currline = 0

        GPIO.setup(self._rs_pin, GPIO.OUT)
        GPIO.setup(self._rw_pin, GPIO.OUT)
        GPIO.setup(self._enable_pin, GPIO.OUT)

        # now we pull both RS and R/W low to begin commands
        GPIO.output(self._rs_pin, GPIO.LOW)
        GPIO.output(self._enable_pin, GPIO.LOW)
        GPIO.output(self._rw_pin, GPIO.LOW)

        # give it some time to power up
        time.sleep(0.05)
        
        for i in range(4):
            GPIO.setup(self._data_pins[i], GPIO.OUT)
            GPIO.output(self._data_pins[i], GPIO.LOW)

        # initialization sequence is not quite as documented by Winstar.
        # Documented sequence only works on initial power-up.
        # An additional step of putting back into 8-bit mode first is
        # required to hand a warm-restart
        #
        # In the data sheet, the timing specs are all zeros(!). These have been tested to
        # reliably handle both warm & colde starts

        # 4-Bit initialization sequence from Technobly
        self._write4bits(0x03)  # put back into 8-bit mode
        time.sleep(0.005)

        if self._oled_ver == OLED_V2:
            # only run extra command for newer displays
            self._write4bits(0x08)
            time.sleep(0.005)
        self._write4bits(0x02)  # put into 4-bit mode
        time.sleep(0.005)
        self._write4bits(0x02)
        time.sleep(0.005)
        self._write4bits(0x08 | character_set)
        time.sleep(0.005)

        self.command(LCD_DISPLAYCONTROL)    # turn off
        time.sleep(0.005)
        self.command(LCD_CLEARDISPLAY)      # clear display
        time.sleep(0.005)
        self.command(0x06)                  # set entry mode
        time.sleep(0.005)
        self.command(LCD_RETURNHOME)        # home cursor
        time.sleep(0.005)
        self.command(0x0C)                  # Turn On - enable cursor & blink
        time.sleep(0.005)


    def clear(self):
        # clear display, set cursor position to zero
        self.command(LCD_CLEARDISPLAY)
        # this command takes a long time!
        # time.sleep(0.002)


    def home(self):
        # set cursor position to zero
        self.command(LCD_RETURNHOME)
        # this command takes a long time!
        # time.sleep(0.002)

    # Turn the display on/off (quickly)
    def noDisplay(self):
        self._displaycontrol &= ~LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    def display(self):
        self._displaycontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    # turns the underline cursor on/off
    def noBlink(self):
        self._displaycontrol &= ~LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    def blink(self):
        self._displaycontrol |= LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    # turn on and off the blinking cursor
    def noCursor(self):
        self._displaycontrol &= ~LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    def cursor(self):
        self._displaycontrol |= LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    # these commands scroll the display without changing the RAM
    def scrollDisplayLeft(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)


    def scrollDisplayRight(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)


    # this is for text that flows left to right
    def leftToRight(self):
        self._displaymode |= LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)


    # this is for text that flows right to left
    def rightToLeft(self):
        self._displaymode &= ~LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)


    # this will 'right justify' text from the cursor
    def autoscroll(self):
        self._displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)


    # this will 'left justify' text from the cursor
    def noAutoScroll(self):
        self._displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)


    # allows us to fill the first 8 CGRAM locations
    # with custom characters
    def createChar(self, location, charmap):
        location &= 0x7 # we only have 8 locations, 0-7
        self.command(LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self.write(charmap[i])


    def setCursor(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row >= self._numlines:
            # write to the first line if out of bounds
            row = 0
        self.command(LCD_SETDDRAMADDR | (col + row_offsets[row]))


    #---- mid-level commands for sending data/cmds

    def command(self, value):
        self._send(value, GPIO.LOW)
        self._waitForReady()


    def write(self, value):
        self._send(value, GPIO.HIGH)
        self._waitForReady()


    #---- low-level data pushing commands

    # write either command or data
    def _send(self, value, mode):
        GPIO.output(self._rs_pin, mode)
        GPIO.setup(self._rw_pin, GPIO.OUT)
        GPIO.output(self._rw_pin, GPIO.LOW)

        self._write4bits(value >> 4)
        self._write4bits(value)


    def _pulseEnable(self):
        GPIO.output(self._enable_pin, GPIO.HIGH)
        time.sleep(0.00005)     # timing spec???
        GPIO.output(self._enable_pin, GPIO.LOW)


    def _write4bits(self):
        for i in range(4):
            GPIO.setup(self._data_pins[i], GPIO.OUT)
            GPIO.output(self._data_pins[i], (value >> i) & 0x01)
        time.sleep(0.00005)     # timing spec???
        self._pulseEnable()


    # poll the busy bit until it goes LOW
    def _waitForReady(self):
        busy = 1
        GPIO.setup(self._busy_pin, GPIO.IN)
        GPIO.output(self._rs_pin, GPIO.LOW)
        GPIO.output(slef._rw_pin, GPIO.HIGH)
        while busy:
            GPIO.output(self._enable_pin, GPIO.LOW)
            GPIO.output(self._enable_pin, GPIO.HIGH)

            time.sleep(0.00001)
            busy = GPIO.input(self._busy_pin)
            GPIO.output(self._enable_pin, GPIO.LOW)

            self._pulseEnable()     # get remaining 4 bits, which are not used

        GPIO.setup(self._busy_pin, GPIO.OUT)
        GPIO.output(self._rw_pin, LOW)


def main():
    """
    If we aren't being used as a library, run a 
    little test program
    """
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI OLED2 Test **')
    start_time = time.time()


    lcd = oled2_pi()
    lcd.begin(16, 2)
    lcd.print("hello OLED World")

    try:
        while True:
            lcd.setCursor(0, 1)
            lcd_line_1 = datetime.now().strftime('%b %d     %H:%M\n')
            lcd_line_2 = "75.3* 54.04% - +"
            lcd.print(lcd_line_1 + lcd_line_2)
          
            #lcd.write_message(lcd_line_1, lcd_line_2)
            time.sleep(2)
    finally:
        pass
      #lcd.clear_screen()
    
    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
