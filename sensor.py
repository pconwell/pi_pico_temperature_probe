from machine import ADC, UART, Pin
import utime
from math import log


b25 = 3950 #resistor beta
resolution = 65535 #microcontroller resolution (pico 65535, arduino 1023)


def internal(pin):
    # internal temperature sensor
    
    reading = ADC(pin).read_u16()
    ts_C = 27 - ((reading * (3.3 / (65535))) - 0.706)/0.001721
    
    return(ts_C)

def external(pin):
    # 10k thermistor

    reading = ADC(pin).read_u16()
    ts_C = -273.15 + 1/(0.003354 + log(reading / (65535 - reading))/3950)
    
    return(ts_C)
