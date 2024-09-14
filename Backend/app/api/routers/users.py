from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_schema
from api.dependencies import data_base
from bson import ObjectId

rt = APIRouter(
    prefix = "/user",
    tags = ["Users"],
    responses = {status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@rt.get("/", response_model=list[User])
async def user():
    return [user_schema(user) for user in data_base.users.find()]

@rt.get("/{id}") # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
    
    
@rt.get("/") # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Post

@rt.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=409, detail="Ya existe el usuario")

    user_dict = dict(user)
    del user_dict["id"]

    id = data_base.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(data_base.users.find_one({"_id": id}))
    
    return User(**new_user)

# Put

@rt.put("/",response_model=User ,status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        data_base.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
        
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha podido actualizar el usuario")
    
    
    return search_user("_id", ObjectId(user.id))
    
    
# Delete

@rt.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = data_base.users.find_one_and_delete({"_id": ObjectId(id)})
            
    if not found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha podido borrar el usuario")
            
def search_user(field: str, key):
    
    try:
        user = data_base.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}