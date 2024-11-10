# rpi_pico --> rpi_zero --> graylog temperature sensors

> based on https://www.circuitbasics.com/arduino-thermistor-temperature-sensor-tutorial/ but modified for raspberry pi pico w. I'm also using two temperatures probes, but this should work exactly the same with one.
> also, my original instructions used a pico instead of a pico w. With the pico w, I was able to remove the pico zero w.

## Overview

A temprature probe (10k thermistor) is used to measure temprature data. An rpi pico w board is used to read the tempratures from the thermistors using one of the three ADC pins (GP26_ADC0,GP27_ACD1, and/or GP28_ADC2). Micropython is used on the pico, which reads and sends the data to a syslog server (graylog for me) and an mqtt broker (home assistant + mosquitto for me).

## Parts

- [Raspberry Pi pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [10k Thermistor](https://www.adafruit.com/product/372)

## Schematic
> this is still the old schematic for the pico + zero. The wiring is basically the same, just no pi zero.

![Alt text](circuit.svg)

## Setup

### Pico W

#### Micropython

There are various ways to install micropython on the pico. Arguably the easiest way is to use [Thonny](https://thonny.org/) to install micorpython and write our code to the pico.

1. Install [Thonny](https://thonny.org/)
2. Connect pico to computer via microUSB
3. In Thonny, click `Run` --> `Interpreter` --> `Install or update firmware`
4. Follow on-screen instructions to install micropython
5. Copy all the `____.py` files to the pico.

#### Pico <--> 10k Thermistors
> This section needs to be confirmed/updated with the correct wiring. It should be mostly correct, but I need to re-create the schematic and make sure it is all correct.

Refer to the provided schematic. We will be using 3v3, AGND, GP27_A1, and GP26_A0 - make sure you are using AGND and _not_ GND.

You have a few options on wiring the thermistors, but we will be doing the following. Wire a 10k resistor between 3v3 and one of the ADC pins. Next, wire the 10k thermistor between the same ADC pin and AGND. The way this circut works is voltage is divided between the ADC pin and AGND. As the thermistor gets hotter, thermistor resistance drops - meaning more voltage goes through thermistor --> AGND and less voltage goes through resistor --> ADC.

By measuring the voltage at ADC and doing some math (see pico_read_temp_sensors.py), we can translate the ADC voltage to a temperature.





