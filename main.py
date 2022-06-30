from fastapi import FastAPI, HTTPException, Depends

import xgboost as xgb
import pandas as pd

# Import from another class
from labelStres import *
from schemas import *

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Load model 
model = xgb.XGBClassifier()
model.load_model("model.json")

@app.get("/hallo")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test(db: Session = Depends(get_db)):
    data = {'GSR_label': [2], 'HR_label': [2], 'BP_label': [2], 'SUHU_label':[2], 'RESPIRASI_label':[2]}
    # # Create DataFrame.
    df = pd.DataFrame(data)
    result = model.predict(df)
    result = result.tolist()
    result = ceklabelstres(result)
    return result

@app.get("/")
def get_data_pasien(db: Session = Depends(get_db)):
    return db.query(models.Pasien).all()

# Sama dengan register
@app.post("/")
def create_data_pasien(pasien: Pasien, db:Session = Depends(get_db)):
    pasien_model = models.Pasien()
    pasien_model.name = pasien.name
    pasien_model.email = pasien.email
    pasien_model.password = pasien.password

    db.add(pasien_model)
    db.commit()
    return pasien

@app.post("/login")
def create_login_data_pasien(pasien_login : Pasien_Login, db:Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.email == pasien_login.email and models.Pasien.password == pasien_login.password).first()
    if pasien_model is None :
            raise HTTPException(
                status_code = 404,
                detail = f"Pasien : Does not exist"
            )
    return pasien_model


@app.put("/{pasien_id}")
def update_data_pasien(pasien_id: int, pasien: Pasien, db : Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien ID {pasien_id} : Does not exist"
        )
    pasien_model.name = pasien.name
    pasien_model.email = pasien.email
    pasien_model.password = pasien.password
    db.add(pasien_model)
    db.commit()
    return f"Pasien with id : {pasien_id} : Successfuly updated"

@app.put("/nama/{pasien_id}")
def update_data_nama_pasien(pasien_id: int, pasien: Pasien_Name, db : Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien ID {pasien_id} : Does not exist"
        )
    pasien_model.name = pasien.name
    db.add(pasien_model)
    db.commit()
    
    return f"Pasien with id : {pasien_id} : Successfuly updated."

@app.delete("/{pasien_id}")
def delete_data_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    
    if pasien_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien with id : {pasien_id} : Does not exist"
        )
    
    db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).delete()
    db.commit()
    return f"Pasien with id : {pasien_id} deleted"


@app.get("/kriteria_pasien")
def get_data_kriteria_pasien(db: Session = Depends(get_db)):
    return db.query(models.Kriteria).all()

@app.post("/kriteria_pasien")
def create_data_kriteria_pasien(pasien_kriteria: Kriteria, db:Session = Depends(get_db)):
    
    pasien_kriteria_model = models.Kriteria()


    pasien_kriteria_model.gsr = pasien_kriteria.gsr
    pasien_kriteria_model.hr = pasien_kriteria.hr
    pasien_kriteria_model.bp = pasien_kriteria.bp
    pasien_kriteria_model.suhu = pasien_kriteria.suhu
    pasien_kriteria_model.respirasi = pasien_kriteria.respirasi
    pasien_kriteria_model.id_pasien = pasien_kriteria.id_pasien

    data = {'GSR_label': [int(pasien_kriteria.gsr)], 
            'HR_label': [int(pasien_kriteria.hr)], 
            'BP_label': [int(pasien_kriteria.bp)], 
            'SUHU_label':[int(pasien_kriteria.suhu)], 
            'RESPIRASI_label':[int(pasien_kriteria.respirasi)]}

    # # Create DataFrame.
    df = pd.DataFrame(data)
    result = model.predict(df)
    result = result.tolist()
    result = ceklabelstres(result)

    pasien_kriteria_model.tingkat_stress = result[0]

    db.add(pasien_kriteria_model)
    db.commit()
    return pasien_kriteria_model

@app.put("/kriteria_pasien/{kriteria_id}")
def update_data_kriteria_pasien(kriteria_id: int, pasien_kriteria: Kriteria, db : Session = Depends(get_db)):
    pasien_kriteria_model = db.query(models.Kriteria).filter(models.Kriteria.id_kriteria == kriteria_id).first()
    if pasien_kriteria_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria ID {kriteria_id} : Does not exist"
        )
    pasien_kriteria_model.gsr = pasien_kriteria.gsr
    pasien_kriteria_model.hr = pasien_kriteria.hr
    pasien_kriteria_model.bp = pasien_kriteria.bp
    pasien_kriteria_model.suhu = pasien_kriteria.suhu
    pasien_kriteria_model.respirasi = pasien_kriteria.respirasi
    pasien_kriteria_model.id_pasien = pasien_kriteria.id_pasien
    pasien_kriteria_model.tanggal_cek = pasien_kriteria.tanggal_cek
    db.add(pasien_kriteria_model)
    db.commit()
    return f"Kriteria Pasien with id : {kriteria_id} : Successfuly updated"

@app.delete("/kriteria_pasien/{kriteria_id}")
def delete_data_kriteria_pasien(kriteria_id: int, db: Session = Depends(get_db)):
    pasien_kriteria_model = db.query(models.Kriteria).filter(models.Kriteria.id_kriteria == kriteria_id).first()
    
    if pasien_kriteria_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria Pasien with id : {kriteria_id} : Does not exist"
        )
    
    db.query(models.Kriteria).filter(models.Kriteria.id_kriteria == kriteria_id).delete()
    db.commit()
    return f"Kriteria Pasien with id : {kriteria_id} deleted"


import paho.mqtt.client as paho
import sys

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

# client.subscribe("building/nama")
# client.subscribe("building/SPO2")
# client.subscribe("building/SPO2_csv")
client.subscribe("test/test")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnection from broker")

client.disconnect()

