import requests
import time
import csv
import array
from w1thermsensor import W1ThermSensor
import Adafruit_ADS1x15
import subprocess
import RPi.GPIO as GPIO

# Taking input from the user
name = input("Enter your name: ")
filename = name 
# Output
print("Hello, " + name)

#cek gsr
ceklooping = 0
while True:
    data = input("Apakah Sudah siap untuk melakukan pengukuran gsr? ")
    if data == 'y' and ceklooping > 0:
        break
    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    GAIN = 1

    sum1 = 0.000
    gsr_average = 0.000
    volt = 0.000
    ard = 0.000
    R_skin = 0.000

    list_rskin = []
    list_gsrs = []
    list_raw = []

    save_file = "/home/jepri1508/Program/CSV/CSV_GSR/" + filename + "_GSR.csv"

    t_end = time.time() + 5 * 1

    print("Baca data GSR")
    while time.time() < t_end:
        sum1 = 0
        for i in range(10):
            result = adc.start_adc(1, gain=GAIN)
            volt = ((result/32767)*4.096) - 0.2
            ard = (volt/4.096)*1023
            sum1 += ard
            #print(volt)
        
        #perhitungan Rata-rata pembacaan GSR, Resistansi Kulit, Konduktansi kulit
        gsr_average = sum1/10
        R_skin = ((1024 + 2 * gsr_average)*10000)/(512-gsr_average)
        GSR_Siemens = 1/R_skin
        
        #input data ke array
        list_rskin.append(R_skin)
        list_gsrs.append(GSR_Siemens)
        list_raw.append(gsr_average)
        
        #print("ADC = %d"%volt , "   ADC_AVERAGE = %d" %gsr_average)
        #print(R_skin)
        print(GSR_Siemens)
        time.sleep(0.1)

    #perhitungan Rata-Rata Resistansi Kulit dan Konduktansi Kulit
    average_RK = sum(list_rskin)/len(list_rskin)
    average_GSRS = sum(list_gsrs)/len(list_gsrs)
    Serial_GSR = sum(list_raw)/len(list_raw)
    print("")
    print("RATA-RATA DATA SERIAL = %d" %Serial_GSR)
    print("RATA-RATA RESISTANSI KULIT = ",round(average_RK,2))
    print("RATA-RATA KONDUKTANSI KULIT = ",average_GSRS)

    with open(save_file,'w',newline='') as csv_file:
        wr = csv.writer(csv_file,delimiter="\n")
        wr.writerow(list_raw)

    print("Data gsr Terekam")
    ceklooping=ceklooping+1

#cek suhu
ceklooping = 0
while True:
    data = input("Apakah Sudah siap untuk melakukan pengukuran suhu? ")
    if data == 'y' and ceklooping > 0:
        break
    sensor = W1ThermSensor()
    suhu_csv= []
    save_file = "/home/jepri1508/Program/CSV/CSV_Suhu/" + filename + ".csv"
    t_end = time.time() + 60 * 1
    temperature = 0

    while time.time() < t_end:
        temperature = sensor.get_temperature()
        print("Suhu Terdeteksi = ",round (temperature,2),'Cesius')
        suhu_csv.append(str(temperature))
        time.sleep(1)

    #Input data ke CSV
    with open(save_file,'w',newline='') as csv_file:
        wr = csv.writer(csv_file,delimiter="\n")
        wr.writerow(suhu_csv)
        
    print("Data suhu Terekam")
    ceklooping=ceklooping+1

#cek bpm
ceklooping = 0
while True:
    data = input("Apakah Sudah siap untuk melakukan pengukuran Heart Rate? ")  
    if data == 'y' and ceklooping > 0:
        break
    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    BPM_CSV = []
    GAIN = 1
    ard = 0
    bpm=0
    ls=0
    print("Baca data BPM")
    save_file = "/home/jepri1508/Program/CSV/CSV_Pulse/" + filename + "_Pulse.csv"
    #save file CSV
    t_end = time.time() + 60 * 1

    while time.time() < t_end:
        sum1 = 0
        for i in range(9):
            result = adc.start_adc(0, gain=GAIN)
            volt = (result/32767)*4.096
            ard = (volt/4.096)*1023
            sum1 += ard
        #print("Data analog "+str(ard))  
        if ard>650 and ls == 0:
            ls = 1;
            bpm+=1
            print("BPM="+str(bpm))
        
        if ard<650 and ls == 1:
            ls = 0
        BPM_CSV.append(str(bpm))
        time.sleep(0.1)

        
    with open(save_file,'w',newline='') as csv_file:
        wr = csv.writer(csv_file,delimiter="\n")
        wr.writerow(BPM_CSV)
        print ("File CVS is Ready")


    print("Data heart rate Terekam")
    ceklooping=ceklooping+1

#cek respirasi
ceklooping = 0
while True:
    data =  input("Apakah Sudah siap untuk melakukan pengukuran Respirasi? ")
    if data == 'y' and ceklooping > 0:
        break
    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    GAIN = 8
    ls = 0
    threshold = 70
    RESPIRASI_CSV = []
    ard = 0
    Respirasi=0
    print("Baca data BPM")
    save_file = "/home/jepri1508/Program/CSV/CSV_Respirasi/" + filename + "_Respirasi.csv"
    #save file CSVa
    t_end = time.time() + 60 * 1

    while time.time() < t_end:
        result = adc.start_adc(2, gain=GAIN)
        volt = (result/32767)*4.096
        ard = (volt/4.096)*1023
        #print("Data analog "+str(ard))  
        if ard>100 and ls == 0:
            ls = 1;
            Respirasi+=1
            print("Respirasi="+str(Respirasi))
        
        if ard<100 and ls == 1:
            ls = 0
        RESPIRASI_CSV.append(str(ard))
        time.sleep(0.1)

    print("RESPIRASI RATE Per Minutes : %d" %Respirasi)

    with open(save_file,'w',newline='') as csv_file:
        wr = csv.writer(csv_file,delimiter="\n")
        wr.writerow(RESPIRASI_CSV)
        print ("File CVS is Ready")
        
    print("Data Respirasi Terekam")
    ceklooping=ceklooping+1

#cek blood preasure
ceklooping = 0
while True:
    data = input("Apakah Sudah siap untuk melakukan pengukuran Blood Preasure? ")
    if data == 'y' and ceklooping > 0:
        break
    pump = 18
    valve = 15

    volt = 0.00
    kpa = 0.00
    mmhg = 0.00
    state = 0

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pump,GPIO.OUT)
    GPIO.setup(valve,GPIO.OUT)

    GPIO.output(pump,GPIO.HIGH)
    GPIO.output(valve,GPIO.LOW)

    nama_subjek = name
    save_file = "/home/jepri1508/Program/CSV/CSV_Tensi/" + nama_subjek + "_Tensi.csv"

    GPIO.output(pump,GPIO.LOW)
    GPIO.output(valve,GPIO.HIGH)
    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    GAIN = 1

    list_mmhg = []

    time.time()
    while True:
        sensor = adc.start_adc(3, gain=GAIN)
        volt = (sensor/32767)*4.096
        kpa = ((volt/5.00)-0.04)/0.018
        mmhg = kpa*7.50
        print("MMHG = %f"%mmhg)
        list_mmhg.append(mmhg)
        if mmhg > 170:
            state = 1
        
        if state == 1:
            GPIO.output(pump,GPIO.HIGH)
            state = 2
        
        if state == 2:
            if mmhg < 35:
                GPIO.output(valve,GPIO.LOW)
                state = 3
        
        if state == 3:
            if mmhg < 0:
                break
        time.sleep(0.001)

    with open(save_file,'w',newline='') as csv_file:
        wr = csv.writer(csv_file,delimiter="\n")
        wr.writerow(list_mmhg)
        
    time.time()

    fmap = []
    rows = []
    osilasi_data = []
    temp_osilasi_data = []

    sd_1 = 0.0
    old_sd1 = 0.0
    s_map = 0.0
    fmap_on = 0.0
    MAP_Value = 0.0
    old_value = 0.0
    old_dataset = 0.0
    fmap_on = 0.0
    i = 0.0

    nama_subjek = name
    with open("/home/jepri1508/Program/CSV/CSV_Tensi/%s_Tensi.csv" %nama_subjek ,'r', newline = '') as file:
        csvreader = csv.reader(file,delimiter=',')
        for row in csvreader:
            rows.append(row)
    print('Find Max Data....')

    #mencari data tertinggi
    for x in range (0, len(rows)):
        for x1 in rows[x]:
            dataset = float(x1)
            #print(dataset)
            if dataset > old_value:
                old_value = dataset

    print("Data Maks = %d" %old_value)
    time.sleep(0.01)

    #mencari osilasi tekanan darah
    for x in range (0, len(rows)):
        for x1 in rows[x]:
            dataset = float(x1)
            #print(dataset,"     ", old_value)
            if dataset == old_value and fmap_on == 0:
                fmap_on = 1
                print('Pembacaan Sedang Dilakukan')
                time.sleep(1)

            if fmap_on == 1:
                if dataset > old_dataset:
                    if dataset != old_dataset:
                        sd_1 += 1
                    #print('Data_Now = %f '%dataset, 'Data_Before = %f '%old_dataset)
                else:
                    fmap.append([])
                    if sd_1 > 0 and dataset >60 and dataset < 115:
                        #print(sd_1)
                        i += 1
                        if sd_1 > old_sd1:
                            old_sd1 = sd_1
                            MAP_Value = dataset
                            print(old_sd1)
                            #print('Map = %d ' %MAP_Value, 'Lonjakan = %d '%old_sd1)
                        temp_osilasi_data.append(sd_1)
                        temp_osilasi_data.append(dataset)
                        osilasi_data.append(temp_osilasi_data)
                    #print(sd_1)
                    sd_1 = 0
            old_dataset = dataset
            temp_osilasi_data = []


    diastolyc = MAP_Value * 0.85
    systolic = MAP_Value * 1.33

    #print(osilasi_data)
    print('Tinggi Lonjakan = %f ' %old_sd1, 'pada Tekanan = %f MMHG' %MAP_Value)
    print('Map Value = %f '%MAP_Value, 'Systolic = %f ' %systolic, 'Diastolyc = %f ' %diastolyc)
    data_bp = str(int(systolic)) + "/"+str(int(diastolyc))

    print("Data Blood Preasure Terekam")
    ceklooping=ceklooping+1


# get id_pasien
url = 'http://139.59.236.46/id_pasien/'+name
header = {"charset": "utf-8", "Content-Type": "application/json"}
response = requests.get(url, headers=header)

id_pasien = response.json()
# untuk memanggil idpasien id_pasien['id_pasien']

import paho.mqtt.client as paho
import sys
from datetime import datetime

client = paho.Client()
if(client.connect("139.59.236.46", 1883, 60)) != 0:
	print("Could not connect to                                                                                                                             MQTT Broker!")
	sys.exit(-1)
else:
	print("MQTT Broker! Berhasil connect")

tanggalcek = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

client.publish("deteksi/gsr",str(int(average_GSRS*100000)), 0)
client.publish("deteksi/hr",str(bpm), 0)
client.publish("deteksi/bp",data_bp, 0)
client.publish("deteksi/suhu",str(round(temperature)), 0)
client.publish("deteksi/respirasi",str(Respirasi), 0)
client.publish("deteksi/tanggal_cek",tanggalcek , 0)
client.publish("deteksi/id_pasien", id_pasien['id_pasien'], 0)
client.disconnect()



