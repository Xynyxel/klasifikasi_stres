import paho.mqtt.client as paho
import sys
from datetime import datetime

client = paho.Client()

if client.connect("139.59.236.46", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)
else:
    print("MQTT Broker! berhasil connect")

tanggalcek = datetime.utcnow()
tanggalcek = datetime.strptime(tanggalcek, '%Y-%m-%d %H:%M:%S.%f')


client.publish("deteksi/gsr", "3", 0)
client.publish("deteksi/hr", "60", 0)
client.publish("deteksi/bp", "100/70", 0)
client.publish("deteksi/suhu", "36", 0)
client.publish("deteksi/respirasi", "16", 0)
client.publish("deteksi/tanggal_cek", tanggalcek, 0)
client.publish("deteksi/id_pasien", "1", 0)

client.disconnect()