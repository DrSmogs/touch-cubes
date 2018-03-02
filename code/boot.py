# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import neopixel
import machine
import config
np = neopixel.NeoPixel(machine.Pin(4), 1)
#import webrepl
#webrepl.start()
gc.collect()
cfg = config.load_config

#start with red lights
np[0] = (125,0,0)
np.write()

def wifi_connect(cfg['wifi_credentials'][0]['WIFI_SSID'],cfg['wifi_credentials'][0]['WIFI_PASS']):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():

        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            #flash blue led while connecting

            np[0] = (0,0,125)
            np.write()
            time.sleep_ms(50)
            np[0] = (0,0,0)
            np.write()
            time.sleep_ms(50)

    print('network config:', sta_if.ifconfig())

    #change led to green once Connected
    np[0] = (0,125,0)
    np.write()
