from machine import ADC, UART, Pin
import utime
from math import log

b25 = 3950
resolution = 65535
tpins = [26,27,4]

led = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)

while True:
    t = {}
    for i in tpins:
        
        reading = ADC(i).read_u16()
        
        if i == 4:
            ts_C = 27 - (((reading * (3.3/resolution)) -0.706)/0.001721)
            t[i] = ts_C
            #print(f"temp {i}: {ts_C}")
        else:
            ts_C = -273.15 + 1/(0.003354 + log(reading / (resolution - reading))/b25)
            #print(f"temp {i}: {ts_C}")
            t[i] = ts_C

    print(t)
    uart.write(f"{t}\n")
    led.toggle()
    utime.sleep(1)
