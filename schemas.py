from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from typing import List


class Pasien(BaseModel):
    name: str 
    email: str 
    password: str

    class Config:
        orm_mode = True

class Pasien_Login(BaseModel):
    email: str 
    password: str 

    class Config:
        orm_mode = True

class Kriteria(BaseModel):
    gsr: int 
    hr: int
    bp: str 
    suhu: int
    respirasi: int 
    tanggal_cek: Optional[datetime] = None 
    id_pasien: int = Field(default=None, foreign_key="pasien.id")

    class Config:
        orm_mode = True

class Pasien_Name(BaseModel):
    name: str

    class Config:
        orm_mode = True

