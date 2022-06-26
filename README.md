# rpi_pico --> rpi_zero --> graylog temperature sensors

> based on https://www.circuitbasics.com/arduino-thermistor-temperature-sensor-tutorial/ but modified for raspberry pi pico and pi zero instead of arduino

## Overview

A temprature probe (10k thermistor) is used to measure temprature data. An rpi pico board is used to read the tempratures from the thermistors using one of the three ADC pins (GP26_ADC0,GP27_ACD1, and/or GP28_ADC2), then those tempratures are in turn read by an rpi zero over uart/serial. Micropython is used on the pico and python is used on the zero. The zero sends the data to a graylog server (or any syslog server).

## Parts

- [Raspberry Pi pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) (any of the RPi boards would probably work)
- [10k Thermistor](https://www.adafruit.com/product/372)

## Schematic

![Alt text](circuit.svg)

## Setup

### Pico

#### Micropython

There are various ways to install micropython on the pico. Arguably the easiest way is to use [Thonny](https://thonny.org/) to install micorpython and write our code to the pico.

1. Install [Thonny](https://thonny.org/)
2. Connect pico to computer via microUSB
3. In Thonny, click `Run` --> `Interpreter` --> `Install or update firmware`
4. Follow on-screen instructions to install micropython
5. Copy the pico_read_temp_sensors.py code into the editor window
6. Click the save icon and it should ask you where you want to save the file. Click "R Pi" in the popup.
7. Make sure to name the file main.py so it automatically runs when the pico is powered on.
8. You are done with the pico

#### Pico <--> 10k Thermistors

Refer to the provided schematic. We will be using pin 36 (3v3_OUT) and pin 33 (AGND) - make sure you are using AGND and _not_ GND (pins 3, 18, 13, 18, 23, 28, or 38 as they are not isolated and will not provide accurate reading for the ADC pins). Additionally, we will be using one of the three ADC pins to read voltage changes as the thermisitor warms up or cools down (GP26_ADC0,GP27_ACD1, and/or GP28_ADC2).

You have a few options on wiring the thermistors, but we will be doing the following. Wire a 10k resistor between 3v3 and one of the ADC pins. Next, wire the 10k thermistor between the same ADC pin and AGND. The way this circut works is voltage is divided between the ADC pin and AGND. As the thermistor gets hotter, thermistor resistance drops - meaning more voltage goes through thermistor --> AGND and less voltage goes through resistor --> ADC.

By measuring the voltage at ADC and doing some math (see pico_read_temp_sensors.py), we can translate the ADC voltage to a temperature.

#### Pico <--> Zero

We need to transmit a serial message from the pico to the zero. We can connect the UART Tx pin (Pin 1) on the pico and the UART Rx pin (Pin 16) on the zero to read the temperature readings. Since we are not talking *to* the pico, you don't have to connect the other UART pins, but you can if you want. That's it for reading from the pico (pretty easy, just one wire!).

We will also want to power the pico from the zero for convenience (and we need a common ground for UART anyway). For this, we can connect Pin 1 (3v3) on the zero to Pin 39 (VSYS) on the pico. Then connect any of the GND pins on the zero to any of the GND pins on the pico. Power and communications with just three wires, not bad!

### Zero

Depending on your preferences and needs, you have options here. For my needs, I installed Raspberry OS using the official installer. I flashed an SD card and popped it into the zero. I needed internet connectivity to talk to the graylog server, so I also configured wifi. After getting the zero up and running (and connected to the internet), there is not much else that needs to be done other than set up the python script to read from the pico.

I ssh'd into the zero and copied the zero_read_from_pico.py script over. Then, set it up how you want, but I run the script every 5 minutes using cron. Assuming you connected your UART pin as described above, you should be done.







