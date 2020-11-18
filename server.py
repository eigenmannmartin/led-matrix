from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
app = Flask(__name__)


def get_empty_display():
    return [
        [[255, 255, 255] for y in range(32)] for x in range(8)
    ]


DISPLAY = get_empty_display()

MQTT_TOPIC = "ledtest/1"
MQTT_HOST = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TIMEOUT = 60
client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, MQTT_TIMEOUT)
client.loop_start()


@app.route('/')
def index():
    global DISPLAY
    return jsonify(DISPLAY)


@app.route('/set',  methods=['POST'])
def set():
    global DISPLAY
    req_data = request.get_json()
    DISPLAY = get_empty_display()  # Set display to all zero. If we want to keep the state, comment this line

    if len(req_data):

        for entry in req_data:
            x = entry['x']
            y = entry['y']
            c = entry['c']

            DISPLAY[y][x] = c
    else:
        DISPLAY = get_empty_display()

    client.publish(MQTT_TOPIC, str(DISPLAY))
    return "ok"
