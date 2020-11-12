import json
import time
import board
import neopixel
import paho.mqtt.client as mqtt


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

ROWS = 8
COLS = 32


MQTT_TOPIC = "ledtest/#"
MQTT_HOST = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TIMEOUT = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, ROWS * COLS, brightness=1, auto_write=False, pixel_order=ORDER
)


def update_display(pic):
    for col in range(0, COLS):
        for row in range(0, ROWS):
            if col % 2 == 1:
                led = (col * ROWS + (ROWS - row)) - 1
                try:
                    pixels[led] = pic[row][col]
                except IndexError:
                    pixels[led] = (0, 0, 0)
            else:
                led = col * ROWS + row
                try:
                    pixels[led] = pic[row][col]
                except IndexError:
                    pixels[led] = (0, 0, 0)

    pixels.show()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(msg.payload)
    try:
        update_display(json.loads(msg.payload))
    except:
        print('error')


# update_display(json.loads("[[[255,255,255]]]"))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, MQTT_TIMEOUT)
client.loop_forever()
