from umqtt.simple import MQTTClient
from utime import sleep
import sensor
import wifi
import logger
from get_time import get_time_data

debug_logging = True

SECONDS_DELAY = 600

INTERNAL_SENSOR = sensor.internal(4)
COIL_SENSOR = sensor.external(27)
AMBIENT_SENSOR = sensor.external(26)


def next_run_in_seconds(SECONDS_DELAY, current_time):
    """Calculate the next runtime based on the delay and current time."""
    if current_time is None:
        logger.send_debug_to_graylog_udp(debug_logging, f"Could not fetch time data, defaulting to {SECONDS_DELAY} seconds.")
        return SECONDS_DELAY
    
    next_run_in = SECONDS_DELAY - ((int(current_time.minute) % (SECONDS_DELAY / 60) * 60) + int(current_time.second))
    logger.send_debug_to_graylog_udp(debug_logging, f"Next run in {next_run_in} seconds.")
    return next_run_in

def send_mqtt_data():
    client = MQTTClient("pico", "172.24.0.100", user="YOUR_HA_USER", password="YOUR_HA_PASSWORD", keepalive=30)
    client.connect()
    client.publish(f"home/pico/ac_coil", str(COIL_SENSOR))
    client.publish(f"home/pico/ac_ambient", str(AMBIENT_SENSOR))

# Initial bootup
wifi_connection = wifi.connect()
    
send_mqtt_data()

current_time = get_time_data()
sleep(next_run_in_seconds(SECONDS_DELAY, current_time))


while True:
    # Fetch current time
    current_time = get_time_data()
    
    # Check if Wi-Fi is connected (i.e. has an IP address)
    if not not wifi_connection[1]:
        wifi_connection = wifi.connect()
    
    # Send logs to Graylog
    logger.send_log_to_graylog_udp(
        f"Temperature Sensor Readings from {wifi_connection[1]} - Coil: {COIL_SENSOR}; Ambient: {AMBIENT_SENSOR}",
        INTERNAL_SENSOR,
        COIL_SENSOR,
        AMBIENT_SENSOR,
        current_time.hour if current_time else None,
        current_time.day_of_week if current_time else None
    )
    
    # send mqtt data to home assistant
    send_mqtt_data()
    
    # Sleep until the next run
    sleep(next_run_in_seconds(SECONDS_DELAY, current_time))

