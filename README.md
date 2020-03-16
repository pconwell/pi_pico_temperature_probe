# AC_to_UNO_to_RPI_to_GoogSheet

based off https://www.circuitbasics.com/arduino-thermistor-temperature-sensor-tutorial/

## Overview

A temprature probe (thermistor) is used to measure temprature data. A UNO board is used to read the tempratures, then those tempratures are read by a Raspberry Pi over serial. Pyhon is used on the RPi to read the serial input from the UNO board, then sends the temprature readings to a google spreadsheet.

The python script is run by a cronjob every 5 minutes.

## Parts

- [Uno Board](https://store.arduino.cc/usa/arduino-uno-rev3) (any ATmega328P or similar should work)
- [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) (any of the RPi boards would probably work)
- [Thermistor](https://www.adafruit.com/product/372)

## Schematic

![Alt text](circuit.svg)

## Setup

The thermistor is connected to the UNO board as shown. The UNO board is running the read_temp.ino script which sends a serial output of the temprature in F and C every 3 seconds. This could pretty easily be cleaned up (for example, there is not much point in outputting to F and C), but it works for our purposes.

Using a USB cable, the UNO is attached to the Raspberry Pi. The Raspberry Pi runs a python script temp_to_googlesheets.py to read the serial input from the UNO board. This python script is run once every 5 minutes from a cronjob.

The python script is a little wonky because it may start reading the serial output mid-stream, meaning it might only get half (or a quarter or 1/10th or 7/8th or whatever) of the serial output which will lead to some interesting outputs. So, we will check to make sure the output starts with a full line (in this case, the first full line should start with the word "Temperature").

If the python script sees a full line of data, it will send the temprature readings to a Google Spreadsheet.

To authenticate to the Google Spreadsheet, it will probably be easier to run this script once on a non-headless computer so you can authenticate (it will open in a browser window to let you sign in to your Google Account). Once you have generated the necessary token.pickle file, you can copy everything over to a headless Raspberry Pi to let it run.
