from fastapi import APIRouter, Request, Form, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta
from api.dependencies import data_base
from api.templates import *

ALGORITHM = "HS256"
SECRET = "82816efa859efc154fd964bv4a0fcc4b416d8c55bd890ab118fc54dacba2886a"
EXPIRE_TIME = 20

db_users = data_base.users

rt = APIRouter()

jinja2Template = Jinja2Templates(directory="api/templates")

def get_user(username: str, db: list):
    return db.find_one({"username": username})
    
def auth_user(password: str, password_plane: str):
    password_clean = password.split("#")[0]
    if password_clean == password_plane:
        return True
    else:
        return False
    
def create_token(data: dict):
    data_token = data.copy()
    data_token["expire"] = (datetime.utcnow() + timedelta(seconds=EXPIRE_TIME)).isoformat()
    token_jwt = jwt.encode(data_token, key=SECRET, algorithm="HS256")
    return token_jwt


@rt.get("/users/login", response_class=HTMLResponse)
async def root(request: Request):
    return jinja2Template.TemplateResponse("index.html", {"request": request})

@rt.get("/users/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, access_token: Annotated[str | None, Cookie()] = None):
    
    if access_token is None:
        return RedirectResponse("/users/login", status_code=302)
    
    try:
        data_user = jwt.decode(access_token, key=SECRET, algorithms=["HS256"])
        if get_user(data_user["username"], db_users) is None:
            return RedirectResponse("/users/login", status_code=302)
        return jinja2Template.TemplateResponse("dashboard.html", {"request": request})
    except:
        return RedirectResponse("/users/login", status_code=302)


@rt.post("/users/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = get_user(username, db_users)
    
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not auth_user(user_data["password"], password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    token = create_token({"username": user_data["username"]})
    
    return RedirectResponse(
        "/users/dashboard", 
        status_code=302,
        headers={"set-cookie": f"access_token={token}; Max-Age={EXPIRE_TIME}"}
    )
    

@rt.get("/users/logout")
async def logout():
    return RedirectResponse("/users/login", status_code=302, headers={"set-cookie": "access_token=; Max-Age=0"})