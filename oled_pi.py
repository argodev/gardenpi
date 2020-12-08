#!/usr/bin/python3
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging

# CONSTANTS
LCD_WIDTH = 16                     # Max line char width
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80                      # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0                      # LCD RAM address for the 2nd line

# Timing constants for low level write operations
# NOTE: Enable cycle time must be at least 1 microsecond
# NOTE2: Actually, these can be zero and the LCD will typically still work OK
EDEL_TAS =  0.00001                 # Address setup time (TAS)
EDEL_PWEH = 0.00001                 # Pulse width of enable (PWEH)
EDEL_TAH =  0.00001                 # Address hold time (TAH)

# Timing constraints for initialisation steps - IMPORTANT!
# Note that post clear display must be at least 6.2ms for OLEDs, as opposed
# to only 1.4ms for HD44780 LCDs. This has caused confusion in the past.
DEL_INITMID = 0.01                  # middle of initial write (min 4.1ms)
DEL_INITNEXT = 0.0002               # post ssecond initial write (min 100ns)
DEL_POSTCLEAR = 0.01                # post clear display step (busy, min 6.2ms)

class oled_pi():
  """
  Class for manipulating and supporting the Winstar 16x2 OLED 
  screen with a Raspberry PI.

  This code is heavily influenced by the sample code provided here:
  https://xdevs.com/guide/lcd-pi/. Any credit for how well this works
  should go to that author. Any bugs should be assumed to be mine.
  """

  def __init__(self):
    logging.info("Creating OLED object")
    self.d4 = 6
    self.d5 = 13
    self.d6 = 19
    self.d7 = 26
    self.rw = 12
    self.rs = 0
    self.e = 5
    self._initialized = False
  
  def _initialize_oled(self):
    """
    LCD Initialisation to setup the two line display using the 4 bit interface
    """
    logging.info("Initializing OLED")
    # Configure the GPIO to drive the LCD display correctly
    GPIO.setmode(GPIO.BCM)             # Use BCM GPIO numbers

    # setup all output pins for driving LCD display
    GPIO.setup(self.d4, GPIO.OUT)
    GPIO.setup(self.d5, GPIO.OUT)
    GPIO.setup(self.d6, GPIO.OUT)
    GPIO.setup(self.d7, GPIO.OUT)
    GPIO.setup(self.e, GPIO.OUT)
    GPIO.setup(self.rw, GPIO.OUT)
    GPIO.setup(self.rs, GPIO.OUT)
    GPIO.output(self.rw, False)       # Write only mode

    # Initialise display into 4 bit mode, using recommended delays
    self._lcd_byte(0x33, LCD_CMD, DEL_INITNEXT, DEL_INITMID)
    self._lcd_byte(0x32, LCD_CMD, DEL_INITNEXT)
  
    # Now perform remainder of display init in 4 bit mode - IMPORTANT!
    # These steps MUST be exactly as follows, as OLEDs in particular are rather fussy
    self._lcd_byte(0x28, LCD_CMD, DEL_INITNEXT)    # two lines and correct font
    self._lcd_byte(0x08, LCD_CMD, DEL_INITNEXT)    # display OFF, cursor/blink off
    self._lcd_byte(0x01, LCD_CMD, DEL_POSTCLEAR)   # clear display, waiting for longer delay
    self._lcd_byte(0x06, LCD_CMD, DEL_INITNEXT)    # entry mode set

    # Extra steps required for OLED initialisation (no effect on LCD)
    self._lcd_byte(0x17, LCD_CMD, DEL_INITNEXT)    # character mode, power on

    # Now turn on the display, ready for use - IMPORTANT!
    self._lcd_byte(0x0C, LCD_CMD, DEL_INITNEXT)    # display on, cursor/blink off

    self._initialized = True

  def _lcd_byte(self, byteVal, mode, post_delay = 0, mid_delay = 0):
    """
    Low level routine to output a byte of data to the LCD display
    over the 4 bit interface. Two nybbles are sent, one after the other.
    The post_delay specifies optional delay to cover busy periods
    The mid_delay specifies optional delay between the 4  bit nibbles (special case)
    """

    # convert incoming value into 8 bit array, padding as required
    bits = bin(byteVal)[2:].zfill(8)
  
    # generate an array of pin numbers to write out
    lcdPins = [self.d7, self.d6, self.d5, self.d4]

    # set mode = True  for character, False for command
    GPIO.output(self.rs, mode) # RS

    # Output the four High bits
    for i in range(4):
      GPIO.output(lcdPins[i], int(bits[i]))

    # Toggle 'Enable' pin, wrapping with minimum delays
    time.sleep(EDEL_TAS)   
    GPIO.output(self.e, True) 
    time.sleep(EDEL_PWEH)
    GPIO.output(self.e, False) 
    time.sleep(EDEL_TAH)     

    # Wait for extra mid delay if specified (special case)
    if mid_delay > 0:
      time.sleep(mid_delay)

    # Output the four Low bits
    for i in range(4,8):
      GPIO.output(lcdPins[i-4], int(bits[i]))

    # Toggle 'Enable' pin, wrapping with minimum delays
    time.sleep(EDEL_TAS)   
    GPIO.output(self.e, True) 
    time.sleep(EDEL_PWEH)
    GPIO.output(self.e, False) 
    time.sleep(EDEL_TAH)   

    # Wait for extra post delay if specified (covers busy period)
    if post_delay > 0:
      time.sleep(post_delay)


  def _lcd_string(self, message):
    """
    Outputs string to the LCD display line, padding as required
    """
    # Send string to display
    message = message.ljust(LCD_WIDTH," ") 

    for i in range(LCD_WIDTH):
      self._lcd_byte(ord(message[i]),LCD_CHR)


  def write_message(self, line1, line2):
    if not self._initialized:
      self._initialize_oled()
    
    self._lcd_byte(LCD_LINE_1, LCD_CMD)
    self._lcd_string(line1)
    self._lcd_byte(LCD_LINE_2, LCD_CMD)
    self._lcd_string(line2)


  def clear_screen(self):
    self.write_message("", "")


def main():
    """
    If we aren't being used as a library, run a 
    little test program
    """
    log_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)
    logging.info('** GardenPI OLED Test **')
    start_time = time.time()
    lcd = oled_pi()

    try:
      while True:
          lcd_line_1 = datetime.now().strftime('%b %d     %H:%M\n')
          lcd_line_2 = "75.3* 54.04% - +"
          
          lcd.write_message(lcd_line_1, lcd_line_2)
          time.sleep(2)
    finally:
      lcd.clear_screen()
    
    logging.info("Script Finished")
    logging.info("Elapsed Time: %s seconds ", (time.time() - start_time))

# ==============================================================================
# Ensure that the GPIO is cleaned up whichever way the program exits
# This avoids all those annoying "channel already in use" errors
if __name__ == '__main__':
  try:
    main()
  finally:
    GPIO.cleanup()
