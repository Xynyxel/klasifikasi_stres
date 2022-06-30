import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("139.59.236.46", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

test = [1,2,3,4]
listTostr = ' '.join(str(elem) for elem in test)
client.publish("test/test", listTostr, 0)

client.disconnect()