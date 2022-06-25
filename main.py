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

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

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

    if pasien_login.password == pasien_login.confirm_password:
        pasien_model = db.query(models.Pasien).filter(models.Pasien.email == pasien_login.email and models.Pasien.password == pasien_login.password).first()
        if pasien_model is None :
            raise HTTPException(
                status_code = 404,
                detail = f"Pasien : Does not exist"
            )
    else:
        raise HTTPException(
                status_code = 404,
                detail = f"Password and Confirm Password Doesn't Match"
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

