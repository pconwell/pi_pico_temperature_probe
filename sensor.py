from machine import ADC, UART, Pin
import utime
from math import log


# two-point calibration factor
a = 1.2
b = -15.2

BETA = 3950  # Beta value from thermistor specs
R0 = 10000   # Resistance at 25 degrees C (in ohms)
T0 = 298.15  # Reference temperature in Kelvin (25 degrees C)
VCC = 3.3    # Voltage of the system (e.g., 3.3V on the Pico)
R_FIXED = 10000  # Fixed resistor value (10K Ohm)
ADC_MAX = 65535  # ADC resolution (16-bit on Pico)


def internal(pin):
    # internal temperature sensor
    
    reading = ADC(pin).read_u16()
    ts_C = 27 - ((reading * (3.3 / (65535))) - 0.706)/0.001721
    
    return round(ts_C,1)

def external(pin):
    # 10k thermistor

    reading = ADC(pin).read_u16()
    ts_C = -273.15 + 1/(0.003354 + log(reading / (65535 - reading))/3950)
    
    return round(a * ts_C + b,1)


if __name__ == "__main__":
    
    print(internal(4))
    print(external(26))
    print(external(27))
