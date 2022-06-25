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

@app.get("/")
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

