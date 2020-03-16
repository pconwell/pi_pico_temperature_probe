import serial
import re
from datetime import datetime
import csv


ser = serial.Serial('/dev/ttyACM0', 9600)

with open("./test.csv", mode="w") as temprature_file:
    temprature_writer = csv.writer(temprature_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    while True:
        line = re.split(r'[:;,\s]\s*', ser.readline().decode("utf-8".rstrip()))
        temprature_writer.writerow([datetime.now(), line[1], line[3]])
        print(line)

#while True:
#    if(ser.in_waiting > 0):
#        line = ser.readline()
#        line = line.decode("utf-8").rstrip()
#        line = re.split(r'[:;,\s]\s*', line)
#        print(datetime.now(), line)
