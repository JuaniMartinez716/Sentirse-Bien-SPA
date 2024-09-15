from fastapi import APIRouter, HTTPException, status
from models.turno import TurnoCreate, TurnoOut
from schemas.turno import turno_helper
from api.dependencies import data_base
from bson import ObjectId


rt = APIRouter(
    prefix="/turnos",
    tags=["Turnos"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

turnos_collection = data_base.turnos


@rt.get("/", response_model=list[TurnoOut])
async def turno():
    return [turno_helper(turno) for turno in turnos_collection.find({})]


@rt.get("/{id}", response_model=TurnoOut)
async def turno(id: str):
    turno = obtener_turno(id)
    
    if turno is None:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    return turno


@rt.post("/", response_model=TurnoOut)
async def turno(turno: TurnoCreate):
    nuevo_turno = crear_turno(turno)
    return nuevo_turno

@rt.put("/{id}", response_model=TurnoOut)
async def turno(id: str, turno: TurnoCreate):
    # Verificamos si el id es un ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Convertimos el turno en un diccionario
    turno_dict = turno.dict(exclude_unset=True)  # Solo los campos proporcionados

    # Usamos find_one_and_update para actualizar solo los campos especificados
    updated_turno = turnos_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": turno_dict},
        return_document=True
    )

    if not updated_turno:
        raise HTTPException(status_code=404, detail="No se ha podido actualizar el turno")

    return obtener_turno(id)
       
    
@rt.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def turno(id: str):
    
    found = data_base.turnos.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha podido borrar el turno")


def crear_turno(turno_data: TurnoCreate) -> dict:
    turno = turno_data.dict()
    turno["estado"] = "pendiente"
    result = turnos_collection.insert_one(turno)  
    created_turno = turnos_collection.find_one({"_id": result.inserted_id})
    return turno_helper(created_turno)


def obtener_turno(id: str) -> dict:
    # Verificamos si el id es un ObjectId válido
    if not ObjectId.is_valid(id):
        return None
    
    # Buscar el turno con el ObjectId
    turno = turnos_collection.find_one({"_id": ObjectId(id)})
    if turno:
        return turno_helper(turno)
    return None

