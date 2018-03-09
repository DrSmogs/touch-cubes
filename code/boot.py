# This file is executed on every boot (including wake-boot from deepsleep)
import time
import gc
import neopixel
import machine
import touchcube as tc

np = neopixel.NeoPixel(machine.Pin(4), 1)

gc.collect()

import os
print(os.uname())
cfg = tc.load_config()
connected_wifi = ''
#start with red lights
np[0] = (125,0,0)
np.write()

def wifi_connect():
    global connected_wifi
    import network
    known_wifis = cfg['wifi_credentials']
    time_out_secs=300
    wl = network.WLAN(network.STA_IF)
    if not wl.isconnected():
        wl.active(True)
        available_wifis = wl.scan()
        print("Scanning for known wifi SSIDs")
        for available_wifi in available_wifis:
            for known_wifi in known_wifis:
                if available_wifi[0].decode('UTF-8') == known_wifi['WIFI_SSID']:
                    print("Found a known wifi network: "+known_wifi['WIFI_SSID']+" attempting to connect..")
                    wl.connect(known_wifi['WIFI_SSID'],known_wifi['WIFI_PASS'])

                    while not wl.isconnected():
                        counter=0
                        while counter <time_out_secs:
                            np[0] = (0,0,125)
                            np.write()
                            time.sleep_ms(50)
                            np[0] = (0,0,0)
                            np.write()
                            time.sleep_ms(50)
                            counter=counter+1

                        np[0] = (125,0,0)
                        np.write()
                        time.sleep_ms(50)
                        break

                    if wl.isconnected():
                        connected_wifi = known_wifi['WIFI_SSID']
                        print("Connected to "+known_wifi['WIFI_SSID']+" with IP address:" + wl.ifconfig()[0])
                        np[0] = (0,125,0) # turn led green
                        np.write()
                        break
