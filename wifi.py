import network
import utime

'''
connect to wifi with supplied SSID and PASSWORD

return IP, MASK, GATEWAY, and DNS
'''


def connect(SSID, PASSWORD):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        print("waiting to connect to wifi...")
        utime.sleep(3)
    else:
        print(f"Connected to {SSID}: {wlan.ifconfig()}")
