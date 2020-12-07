#!/usr/bin/python3
# -*- coding:utf-8 -*-

import board
import adafruit_dht
import time

def ctof(c):
    f = ((c*9.0)/5.0) + 32
    return f


dht = adafruit_dht.DHT22(board.D24)
#dht = Adafruit_DHT.DHT22

while True:
    try:
        #humidity, temperature = Adafruit_DHT.read_retry(dht, 24)

        temperature = dht.temperature
        humidity = dht.humidity
        # Print what we got to the REPL
        print("Temp: {:.1f} *F \t Humidity: {:.2f}%".format(ctof(temperature), humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)
 
    time.sleep(2)
