import paho.mqtt.client as paho
import sys

def onMessage(client, userdata, msg):
    
    print(msg.topic + ": " + msg.payload.decode())

client = paho.Client()
client.on_message = onMessage

if client.connect("139.59.236.46", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

client.subscribe("building/nama")
client.subscribe("building/SP02")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnection from broker")

client.disconnect()