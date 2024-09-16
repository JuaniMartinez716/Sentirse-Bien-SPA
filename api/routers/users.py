from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_schema
from bson import ObjectId

# Utiliza la base de datos que has configurado
from pymongo import MongoClient
import os

# Conexión a MongoDB
MONGO_DB_URL = os.getenv("MONGO_DB_URL", "mongodb://mongo:mFQtqDptPLwZXKwVmnzihaywXxeORPfa@autorack.proxy.rlwy.net:59644")
client = MongoClient(MONGO_DB_URL)
db = client.SentirseBienDB

# Definición del router
rt = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@rt.get("/", response_model=list[User])
async def get_users():
    return [user_schema(user) for user in db.users.find()]

@rt.get("/{id}")  # Path
async def get_user_by_id(id: str):
    return search_user("_id", ObjectId(id))

@rt.get("/")  # Query
async def get_user_by_query(id: str):
    return search_user("_id", ObjectId(id))

# Post
@rt.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    if isinstance(search_user("email", user.email), User):
        raise HTTPException(status_code=409, detail="Ya existe el usuario")

    user_dict = dict(user)
    del user_dict["id"]

    # Inserta en la colección `users`
    id = db.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db.users.find_one({"_id": id}))

    return User(**new_user)

# Put
@rt.put("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha podido actualizar el usuario")

    return search_user("_id", ObjectId(user.id))

# Delete
@rt.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha podido borrar el usuario")

def search_user(field: str, key):
    try:
        user = db.users.find_one({field: key})
        if user:
            return User(**user_schema(user))
        else:
            return {"error": "No se ha encontrado el usuario"}
    except:
        return {"error": "No se ha encontrado el usuario"}
