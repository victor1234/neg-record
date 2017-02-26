import paho.mqtt.client as paho
import os
import time
import gi


gi.require_version("Gst", "1.0")

from gi.repository import Gst

Gst.init(None)



def startRecord():
    print("starting record")

    recordName = time.strftime("%Y-%m-%d-%H:%M") + ".ogg"

    global pipeline
    pipeline = Gst.parse_launch("autoaudiosrc ! audioconvert ! queue ! vorbisenc ! oggmux ! filesink location={}".format(recordName))
    pipeline.set_state(Gst.State.PLAYING)

def stopRecord():
    print("stop record")

    global pipeline
    pipeline.set_state(Gst.State.NULL)


# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    if msg.payload == "start":
        startRecord()

    if msg.payload == "stop":
        stopRecord()

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = paho.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Connect
mqttc.connect("localhost")

# Start subscribe, with QoS level 0
mqttc.subscribe("neg-record/pipeline", 0)

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()

print("rc: " + str(rc))
