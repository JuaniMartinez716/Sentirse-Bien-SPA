from fastapi import FastAPI
from api.routers import login, users, turnos, comment
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(users.rt)
app.include_router(login.rt)
app.include_router(turnos.rt)
app.include_router(comment.rt)

# Lista de orígenes permitidos
origins = [
    "http://localhost",  # Permitir localhost sin puerto específico
    "http://localhost:3000",  # Si tu frontend corre en localhost:3000 (React u otra app local)
    "https://web-production-69664.up.railway.app",
    "https://lucas-ojeda.github.io/SPAsentirseBien/" ,
    "https://lucas-ojeda.github.io/",
    "https://lucas-ojeda.github.io/SPAsentirseBien/pages/signIn.html"
]

# Agregar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solo localhost y tu backend en Railway
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return "https://sentirsebien.com"