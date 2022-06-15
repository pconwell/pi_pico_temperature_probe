# micropython

from machine import Pin, ADC
import utime
from math import log

# r25 = 10000
b25 = 3950
resolution = 65535

sensor_pin = machine.ADC(0)

while True:
    reading = sensor_pin.read_u16()
#     log_r = log(reading / (resolution - reading))
#     ts_C = -273.15 + 1/(1/298.15 + log_r/b25)
    ts_C = -273.15 + 1/(0.003354 + log(reading / (resolution - reading))/b25)
    print(f"temp: {ts_C}")    
    utime.sleep(2)
