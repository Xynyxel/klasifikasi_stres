from fastapi import FastAPI, HTTPException, Depends

import xgboost as xgb
import pandas as pd

# Import from another class
from labelStres import *
from schemas import *

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


# Change format date
from dateutil import parser
from datetime import datetime


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
    data = [
        {
            "gsr": 3,
            "suhu": 37,
            "hr": 70,
            "tanggal_cek": "2022-07-04T16:57:10.414000",
            "id_pasien": 1,
            "id_kriteria": 1,
            "bp": "110/79",
            "respirasi": 18,
            "tingkat_stress": "Tenang"
        },
    ]
    return data[0]['tanggal_cek']

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
    pasien_model = db.query(models.Pasien).filter(models.Pasien.email == pasien_login.email 
    and models.Pasien.password == pasien_login.password).first()
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

@app.put("/password/{pasien_id}")
def update_data_password_pasien(pasien_id: int, pasien_password: Pasien_Password, db : 
    Session = Depends(get_db)):
    pasien_model = db.query(models.Pasien).filter(models.Pasien.id_pasien == pasien_id).first()
    if pasien_model is None :
        raise HTTPException(
            status_code = 404,
            detail = f"Pasien ID {pasien_id} : Does not exist"
        )
    pasien_model.password = pasien_password.password
    db.add(pasien_model)
    db.commit()
    return f"Pasien with id : {pasien_id} : Successfuly updated"

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

@app.get("/kriteria_pasien_last/{pasien_id}")
def get_data_kriteria_pasien_byidpasien_last(pasien_id: int, db: Session = Depends(get_db)):
    kriteria_pasien = db.query(models.Kriteria).filter(
        models.Kriteria.id_pasien == pasien_id).order_by(
            models.Kriteria.id_kriteria.desc()).first()
    if kriteria_pasien is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria Pasien with id : {pasien_id} : Does not exist"
        )
    return kriteria_pasien

@app.get("/kriteria_pasien/{pasien_id}")
def get_data_kriteria_pasien_byidpasien(pasien_id: int, db: Session = Depends(get_db)):
    kriteria_pasien = db.query(models.Kriteria).filter(
        models.Kriteria.id_pasien == pasien_id).all()
    for data in kriteria_pasien:
        # data.tanggal_cek = parser.parse(data.tanggal_cek)
        data.tanggal_cek  = data.tanggal_cek.strftime("%d/%m/%Y %H:%M:%S")
        
    if kriteria_pasien is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Kriteria Pasien with id : {pasien_id} : Does not exist"
        )
    return kriteria_pasien

@app.post("/kriteria_pasien")
def create_data_kriteria_pasien(pasien_kriteria: Kriteria, db:Session = Depends(get_db)):
    
    pasien_kriteria_model = models.Kriteria()
    pasien_kriteria_model.gsr = pasien_kriteria.gsr
    pasien_kriteria_model.hr = pasien_kriteria.hr
    pasien_kriteria_model.bp = pasien_kriteria.bp
    pasien_kriteria_model.suhu = pasien_kriteria.suhu
    pasien_kriteria_model.respirasi = pasien_kriteria.respirasi
    pasien_kriteria_model.id_pasien = pasien_kriteria.id_pasien
    pasien_kriteria_model.tanggal_cek = pasien_kriteria.tanggal_cek

    data = {'GSR_label': [ceklabelGSRintoModel(pasien_kriteria_model.gsr)], 
            'HR_label': [ceklabelHRintoModel(pasien_kriteria_model.hr)], 
            'BP_label': [ceklabelBPintoModel(pasien_kriteria_model.bp)], 
            'SUHU_label':[ceklabelSUHUintoModel(pasien_kriteria_model.suhu)], 
            'RESPIRASI_label':[ceklabelRESPIRASIintoModel(pasien_kriteria_model.respirasi)]}

    # Create DataFrame.
    df = pd.DataFrame(data)
    result = model.predict(df)
    result = result.tolist()
    result = ceklabelstres(result)
   
    pasien_kriteria_model.tingkat_stress = result[0]

    db.add(pasien_kriteria_model)
    db.commit()
    return f"Kriteria Pasien with id : {pasien_kriteria_model.id_pasien} : Successfuly added"


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



