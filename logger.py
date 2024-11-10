import usocket
import ujson


GRAYLOG_SERVER = "172.24.0.64"
GRAYLOG_PORT = 12201

def send_log_to_graylog_udp(short_message, sensor_internal, sensor_coil, sensor_ambient, hour, day, server=GRAYLOG_SERVER, port=GRAYLOG_PORT, source_name="ac_temp_sensors", level="6"):
    print(short_message)
    log_entry = {
        "version": "1.1",
        "short_message": short_message,
        "level": level,
        "host": source_name,
        "sensor_internal": sensor_internal,
        "sensor_coil": sensor_coil,
        "sensor_ambient": sensor_ambient,
        "hour": hour,
        "day": day
        }
    
    try:
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        sock.sendto(ujson.dumps(log_entry).encode(), (server, port))
        sock.close()
    except Exception as e:

        print("Failed to send log:", e)
        
def send_debug_to_graylog_udp(debug_logging, short_message, server=GRAYLOG_SERVER, port=GRAYLOG_PORT, source_name="ac_temp_debug", level="1"):
    
    if not debug_logging:
        print(f"Debug logging off: {short_message}")
        return None
    
    print(short_message)
    log_entry = {
        "version": "1.1",
        "short_message": short_message,
        "level": level,
        "host": source_name,
        }
    
    try:
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        sock.sendto(ujson.dumps(log_entry).encode(), (server, port))
        sock.close()
    except Exception as e:
        print("Failed to send log:", e)

# Function to log sensor data locally to a file with timestamp
def log_to_file(timestamp, sensor_a, sensor_b, sensor_c):
    try:  
        # Open the log file in append mode
        with open("sensor_log.txt", "a") as file:
            file.write(f"{timestamp} | Sensor A: {str(sensor_a)}, Sensor B: {str(sensor_b)}, Sensor C: {str(sensor_c)}\n")
        
        print(f"Logged to local file at {timestamp}")
    except Exception as e:
        print(f"Failed to log to file: {e}")

# Example usage with a custom source name
if __name__ == "__main__":
    
    # Synchronize time with NTP
#     get_time.sync_time()
#     current_time = get_time.get_current_time()
#     print(current_time)
    
    # Example sensor data
    sensor_a = 10
    sensor_b = 20
    sensor_c = 30
    
    send_debug_to_graylog_udp(True, "This is a test log with custom source name")

    # Log to local file with timestamp
    log_to_file(current_time, sensor_a, sensor_b, sensor_c)
