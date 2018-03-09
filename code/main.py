import time
import ubinascii
import machine
from mqtt import MQTTClient
from machine import Pin
import ujson



# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)


# Default MQTT server to connect to

SERVER = cfg['mqtt_server']
PORT = cfg['mqtt_port']
USERNAME = cfg['mqtt_user']
PASSWORD = cfg['mqtt_pass']
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
PUB_TOPIC =  b"touch_cube/status"
COLOUR_TOPIC = b"touch_cube/colour"
TEST_TOPIC = b"touch_cube/test"
colour=(0,0,0)


state = 1

def sub_cb(topic, msg):
    global state
    global colour
    if topic == TEST_TOPIC:
        state = 2
    if topic == COLOUR_TOPIC:
        state = 1
        data = ujson.loads(msg)
        colour= (data['red'],data['green'],data['blue'])
        np[0] = (colour)
        np.write()


def main():
    global colour
    global connected_wifi
    c = MQTTClient(CLIENT_ID, SERVER, user=USERNAME, password=PASSWORD, port=PORT)
    c.set_callback(sub_cb)
    c.connect()
    np[0] = (100,100,100)
    np.write()
    c.subscribe(COLOUR_TOPIC)
    c.subscribe(TEST_TOPIC)
    c.publish(PUB_TOPIC,  "I have connected to "+connected_wifi+" and waiting for a colour code!")


    while True:

        c.check_msg()
        if state ==1:
            if button.value() == 0:
                time.sleep_ms(20)
                while button.value() == 0:
                    for x in range(0, 125):
                        if button.value() == 0:
                            colour = (125,x,0)
                            np[0] = colour
                            np.write()
                            time.sleep_ms(10)


                    for x in range(125, -1, -1):
                        if button.value() == 0:
                            colour = (x,125,0)
                            np[0] = colour
                            np.write()
                            time.sleep_ms


                    for x in range(0, 125):
                        if button.value() == 0:
                            colour = (0,125,x)
                            np[0] = colour
                            np.write()
                            time.sleep_ms(10)

                    for x in range(125, -1, -1):
                        if button.value() == 0:
                            colour = (0,x,125)
                            np[0] = colour
                            np.write()
                            time.sleep_ms(10)


                    for x in range(0, 125):
                        if button.value() == 0:
                            colour = (x,0,125)
                            np[0] = colour
                            np.write()
                            time.sleep_ms(10)


                    for x in range(125, -1, -1):
                        if button.value() == 0:
                            colour = (125,0,x)
                            np[0] = colour
                            np.write()
                            time.sleep_ms(10)

                message = "{\"red\":" +str(colour[0]) + ", \"green\": " + str(colour[1]) + ",\"blue\": " + str(colour[2])+"}"
                c.publish(COLOUR_TOPIC, message)
            time.sleep_ms(50)

        if state ==2:
            rainbow()

    c.disconnect()
    np[0] = (0,0,0)
    np.write()

def rainbow():

    for x in range(0, 125):
        np[0] = (125,x,0)
        np.write()
        time.sleep_ms(10)

    for x in range(125, -1, -1):
        np[0] = (x,125,0)
        np.write()
        time.sleep_ms

    for x in range(0, 125):
        np[0] = (0,125,x)
        np.write()
        time.sleep_ms(10)

    for x in range(125, -1, -1):
        np[0] = (0,x,125)
        np.write()
        time.sleep_ms(10)

    for x in range(0, 125):
        np[0] = (x,0,125)
        np.write()
        time.sleep_ms(10)

    for x in range(125, -1, -1):
        np[0] = (125,0,x)
        np.write()
        time.sleep_ms(10)



if __name__ == "__main__":
    wifi_connect()
    main()
