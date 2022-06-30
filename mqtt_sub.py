import paho.mqtt.client as paho
import sys

# quote = '成功を収める人とは人が投げてきたレンガでしっかりした基盤を築くことができる人のことである。'

# with open('test.txt', 'w', encoding='utf-8') as f:
#     f.write(quote)
def write_data(data):
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(data)
    print("berhasil")

def onMessage(client, userdata, msg):
    data = str(msg.payload.decode())
    print(msg.topic + ": " + data)
    write_data(data)
    
    # print(msg.topic + ": " + type(data))

client = paho.Client()
client.on_message = onMessage

if client.connect("139.59.236.46", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

client.subscribe("building/nama")
client.subscribe("building/SPO2")
client.subscribe("building/SPO2_csv")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnection from broker")

client.disconnect()