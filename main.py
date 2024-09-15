from fastapi import FastAPI
from api.routers import login, users, turnos, comment
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(users.rt)
app.include_router(login.rt)
app.include_router(turnos.rt)
app.include_router(comment.rt)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return "https://sentirsebien.com"