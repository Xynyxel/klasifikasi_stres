# import paho.mqtt.client as paho
# import sys

# def write_data(data):
#     with open('test.txt', 'w', encoding='utf-8') as f:
#         f.write(data)
#     print("berhasil")

# def onMessage(client, userdata, msg):
#     data = str(msg.payload.decode())
#     print(msg.topic + ": " + data)
#     write_data(data)
    
#     # print(msg.topic + ": " + type(data))

# client = paho.Client()
# client.on_message = onMessage

# if client.connect("139.59.236.46", 1883, 60) != 0:
#     print("Could not connect to MQTT Broker!")
#     sys.exit(-1)

# # client.subscribe("building/nama")
# # client.subscribe("building/SPO2")
# # client.subscribe("building/SPO2_csv")
# client.subscribe("test/test")

# try:
#     print("Press CTRL+C to exit...")
#     client.loop_forever()
# except:
#     print("Disconnection from broker")
#     client.disconnect()

import paho.mqtt.client as mqtt
import time


def write_data(data):
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(data)
    print("berhasil")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe([("ep_mqtt/test", 1), ("ep_mqtt/topic2", 1), ("ep_mqtt/topic3", 1)])
    client.subscribe("test/test")


def on_message(client, userdata, message):
    data = str(message.payload.decode())
    # print(msg.topic + ": " + data)
    write_data(data)
    # print("Message received: " + message.topic + " : " + str(message.payload))
    # if message.topic == 'ep_mqtt/topic2':
    #     with open('/home/pi/mqtt_update.txt', 'a+') as f:
    #         f.write("received topic2")


broker_address = "139.59.236.46"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
