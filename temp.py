import machine
import utime
from math import log

b25 = 3950
resolution = 65535
tpins = [26,27,4]

led = machine.Pin(25, machine.Pin.OUT)

while True:
    for i in tpins:
        
        reading = machine.ADC(i).read_u16()
        
        if i == 4:
            ts_C = 27 - (((reading * (3.3/resolution)) -0.706)/0.001721)
            print(f"temp {i}: {ts_C}")
        else:
#            log_r = log(reading / (resolution - reading))
#            ts_C = -273.15 + 1/(1/298.15 + log_r/b25)
            ts_C = -273.15 + 1/(0.003354 + log(reading / (resolution - reading))/b25)
            print(f"temp {i}: {ts_C}")
        led.toggle()
        utime.sleep(1)
    
    print("\n")
