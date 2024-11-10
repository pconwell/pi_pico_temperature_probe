import urequests

'''
Format data and send to graylog server

url and temps passed as variables, others default unless overridden
'''


def log(url, a, b, c, message="temperatures from rpi pico w sensor", host="pico_w-temp-sensor", facility="1", level="6"):

    data = f'''{{ "short_message":"{message}",
                  "host":"{host}",
                  "facility":"{facility}",
                  "level":"{level}",
                  "sensor_internal":"{a}",
                  "sensor_ambient":"{b}",
                  "sensor_coil":"{c}" }}'''

    response = urequests.post(url, data=data)
