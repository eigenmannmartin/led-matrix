## General

The led-matrix will update its state according to the mqtt messages it receives. It is by default configured to use hivemq (any other mqtt server would work) and listen on topic `ledtest/#`
You can have a look at this topic with the web [online client](http://www.hivemq.com/demos/websocket-client/)
```
| LED-Matrix |<--| HiveMQ-MQTT |<--| Python Server |
```

The messages need to be valid json. It is an array or arrays of arrays. (row => col => [r, g, b])
See the server implementation for details.


## RPI setup
### Install dependencies

Install the required dependencies on the raspberry pi. The raspberry py needs to be connected to the internet. The neopixel led matrix needs to be connected to pin D21.

```bash
sudo apt-get install -y python3 git python3-pip
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel paho-mqtt
```

### Run client

It has to be run as root

```bash
sudo python3 matrix.py
```

## Server setup
### Install dependencies
I used pipenv for dep management. You can install all deps manually with pip. See Pipfile.

```bash
pipenv install
```

### Run server
Run the server. This is the dev mode for convenience.

```bash
pipenv shell
export FLASK_APP=server.py
export FLASK_ENV=development
python -m flask run
```




