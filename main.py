from utime import sleep
import sensor
import wifi
import graylog

# connect to wifi
wifi.connect("alfheim", "#IOTwifipassword!")

# log to graylog
while True:
    url = 'http://192.168.10.101:12202/gelf'
    graylog.log(url, sensor.internal(4),sensor.external(26),sensor.external(27))
    sleep(300)
