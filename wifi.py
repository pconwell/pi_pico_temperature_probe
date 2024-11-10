import network
import utime
import logger

''' return SSID, IP, MASK, GATEWAY, DNS '''

SSID = "YOUR_SSID"
PASSWORD = "YOUR_PASSWORD"

debug_logging = True

def connect(SSID=SSID, PASSWORD=PASSWORD):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    attempt = 0
    while not wlan.isconnected():
        print("waiting to connect to wifi...")
        utime.sleep(min(3 + attempt, 30))
        attempt += 3
    else:
        logger.send_debug_to_graylog_udp(debug_logging, f"{(SSID,) + wlan.ifconfig()}")
        return (SSID,) + wlan.ifconfig()
        
if __name__ == "__main__":
    #print(connect("alfheim", "#IOTwifipassword!"))
    ssid, ip, mask, gateway, dns = connect(SSID, PASSWORD)
    print(f"Connected!\n  SSID: {ssid}\n  IP: {ip}\n  Mask: {mask}\n  Gateway: {gateway}\n  DNS: {dns}")



