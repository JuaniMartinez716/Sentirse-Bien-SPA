from fastapi import APIRouter, HTTPException, status
from models.turno import TurnoCreate, TurnoOut
from schemas.turno import turno_helper
from pymongo import MongoClient
from bson import ObjectId
import os

# Configuración de MongoDB
MONGO_DB_URL = os.getenv("MONGO_DB_URL", "mongodb://mongo:mFQtqDptPLwZXKwVmnzihaywXxeORPfa@autorack.proxy.rlwy.net:59644")
client = MongoClient(MONGO_DB_URL)
data_base = client.SentirseBienDB
turnos_collection = data_base.turnos

rt = APIRouter(
    prefix="/turnos",
    tags=["Turnos"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@rt.get("/", response_model=list[TurnoOut])
async def obtener_turnos():
    return [turno_helper(turno) for turno in turnos_collection.find({})]

@rt.get("/{id}", response_model=TurnoOut)
async def obtener_turno_por_id(id: str):
    turno = obtener_turno(id)
    
    if turno is None:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    return turno

@rt.post("/", response_model=TurnoOut)
async def crear_nuevo_turno(turno: TurnoCreate):
    nuevo_turno = crear_turno(turno)
    return nuevo_turno

@rt.put("/{id}", response_model=TurnoOut)
async def actualizar_turno(id: str, turno: TurnoCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    turno_dict = turno.dict(exclude_unset=True)  # Solo los campos proporcionados

    updated_turno = turnos_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": turno_dict},
        return_document=True
    )

    if not updated_turno:
        raise HTTPException(status_code=404, detail="No se ha podido actualizar el turno")

    return obtener_turno(id)

@rt.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_turno(id: str):
    found = turnos_collection.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=404, detail="No se ha podido borrar el turno")

def crear_turno(turno_data: TurnoCreate) -> dict:
    turno = turno_data.dict()
    turno["estado"] = "pendiente"
    result = turnos_collection.insert_one(turno)  
    created_turno = turnos_collection.find_one({"_id": result.inserted_id})
    return turno_helper(created_turno)

def obtener_turno(id: str) -> dict:
    if not ObjectId.is_valid(id):
        return None
    
    turno = turnos_collection.find_one({"_id": ObjectId(id)})
    if turno:
        return turno_helper(turno)
    return None
