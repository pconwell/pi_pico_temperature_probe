import serial
import logging
import graypy

'''
read data from pico (or arduino with tweaks?) (serial.Serial) and write to graylog server (192.168.10.101)

run every X minutes with cron */X * * * * /usr/bin/python3 /home/pi/zero_read_from_pico.py >/dev/null 2>&1
'''


my_logger = logging.getLogger('attic_temp')
my_logger.setLevel(logging.DEBUG)

handler = graypy.GELFUDPHandler('192.168.10.101', 12201)
my_logger.addHandler(handler)


ser = serial.Serial("/dev/ttyS0", 9600)
print(ser.readline().decode("utf-8".rstrip()))
my_logger.debug(ser.readline().decode("utf-8".rstrip()))
