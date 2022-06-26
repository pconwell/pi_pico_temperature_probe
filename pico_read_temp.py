from machine import ADC, UART, Pin
import utime
from math import log

b25 = 3950 #resistor beta
resolution = 65535 #microcontroller resolution (pico 65535, arduino 1023)
tpins = [26,27,4] #pins to read

led = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)

while True:
    t = {}
    for i in tpins:
        
        reading = ADC(i).read_u16()
        
        if i == 4:
            # internal temperature sensor:
            ts_C = 27 - (((reading * (3.3/resolution)) -0.706)/0.001721)
            t[i] = ts_C
        else:
            # 10k thermistors:
            ts_C = -273.15 + 1/(0.003354 + log(reading / (resolution - reading))/b25)
            t[i] = ts_C

    print(t)
    uart.write(f"{t}\n")
    led.toggle() # so we can see if pico is powered/working
    utime.sleep(1)
