import paho.mqtt.client as mqtt
# import time
import requests
from datetime import datetime
# import json

data_json = {
  "gsr": 0,
  "hr": 0,
  "bp": "",
  "suhu": 0,
  "respirasi": 0,
  "tanggal_cek": "",
  "id_pasien": 0
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("deteksi/gsr")
    client.subscribe("deteksi/hr")
    client.subscribe("deteksi/bp")
    client.subscribe("deteksi/suhu")
    client.subscribe("deteksi/respirasi")
    client.subscribe("deteksi/tanggal_cek")
    client.subscribe("deteksi/id_pasien")


def on_message(client, userdata, message):
    print(message.topic+ ": "+message.payload.decode())
    
    
    if message.topic == 'deteksi/gsr':
        data_json['gsr'] = int(message.payload.decode())
    if message.topic == 'deteksi/hr':
        data_json['hr'] = int(message.payload.decode())
    if message.topic == 'deteksi/bp':
        data_json['bp'] = message.payload.decode()
    if message.topic == 'deteksi/suhu':
        data_json['suhu'] = int(message.payload.decode())
    if message.topic == 'deteksi/respirasi':
        data_json['respirasi'] = int(message.payload.decode())
    if message.topic == 'deteksi/tanggal_cek':
        data_json['tanggal_cek'] = message.payload.decode()
    if message.topic == 'deteksi/id_pasien': 
        data_json['id_pasien'] = int(message.payload.decode())
                        
        # print(data_json)
        url = 'http://139.59.236.46/kriteria_pasien'
        header = {"charset": "utf-8", "Content-Type": "application/json"}
        response = requests.post(url, json = data_json, headers=header)

        if(response.status_code == 200):
            print("response berhasil")
        # print(response.json())


broker_address = "139.59.236.46"  # Broker address
port = 1883  # Broker port

client = mqtt.Client()  # create new instance
client.on_connect = on_connect  
client.on_message = on_message  


client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
