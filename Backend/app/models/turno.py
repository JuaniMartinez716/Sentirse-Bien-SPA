from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TurnoCreate(BaseModel):
    cliente_id: int
    fecha: datetime
    hora: str
    servicio: str
    notas: Optional[str] = None

class TurnoOut(BaseModel):
    id: str
    cliente_id: int
    fecha: str
    hora: str
    servicio: str
    estado: str
    notas: Optional[str] = None

    class Config:
        orm_mode = True
