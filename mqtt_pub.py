import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("139.59.236.46", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)


client.publish("test/test", "test", 0)

client.disconnect()