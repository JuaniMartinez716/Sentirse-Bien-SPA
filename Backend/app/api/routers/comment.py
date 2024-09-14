from fastapi import APIRouter, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.comment import Comment, Reply
from api.dependencies import data_base
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional

rt = APIRouter(
    prefix="/comments",
    tags=["Comment"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)


jinja2Template = Jinja2Templates(directory="api/templates")

@rt.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return jinja2Template.TemplateResponse("comments.html", {"request": request})

@rt.get("/all", response_model=list[dict])
async def get_all_comments():
    comments = data_base.comments.find()  # Obtiene todos los comentarios sin filtro
    result = []
    for comment in comments:
        user = None
        if comment.get("user_id"):
            try:
                # Intenta convertir user_id a ObjectId si es válido
                user = data_base.users.find_one({"_id": ObjectId(comment["user_id"])})
            except InvalidId:
                user = None  # Si no es un ObjectId válido, tratamos como anónimo
        
        # Procesar las respuestas asociadas al comentario
        replies = []
        for reply in comment.get("replies", []):
            reply_user = None
            if reply.get("user_id"):
                try:
                    # Intenta convertir el user_id de la respuesta a ObjectId
                    reply_user = data_base.users.find_one({"_id": ObjectId(reply["user_id"])})
                except InvalidId:
                    reply_user = None  # Si no es un ObjectId válido, usuario anónimo
            replies.append({
                "content": reply["content"],
                "username": reply_user["username"] if reply_user else "Anónimo"
            })

        result.append({
            "content": comment["content"],
            "username": user["username"] if user else "Anónimo",
            "post_id": comment["post_id"],
            "comment_id": str(comment["_id"]),
            "replies": replies  # Añade las respuestas al resultado
        })
    
    print("Todos los comentarios encontrados:", result)  # Para depuración
    return result

@rt.post("/")
async def create_comment(comment: Comment, user_id: Optional[str] = None):
    comment_data = {
        "content": comment.content,
        "post_id": comment.post_id,
        "user_id": user_id
    }
    result = data_base.comments.insert_one(comment_data)
    return {"comment_id": str(result.inserted_id), "content": comment.content}

@rt.get("/{post_id}", response_model=list[dict])
async def get_comments(post_id: str):
    comments = data_base.comments.find({"post_id": post_id})
    result = []
    for comment in comments:
        user = None
        if comment.get("user_id"):
            try:
                # Intenta convertir user_id a ObjectId
                user = data_base.users.find_one({"_id": ObjectId(comment["user_id"])})
            except InvalidId:
                user = None  # Si no es un ObjectId válido, se asume que es un usuario anónimo
        
        # Procesar también las respuestas del comentario
        replies = []
        for reply in comment.get("replies", []):
            reply_user = None
            if reply.get("user_id"):
                try:
                    # Intenta convertir el user_id de la respuesta a ObjectId
                    reply_user = data_base.users.find_one({"_id": ObjectId(reply["user_id"])})
                except InvalidId:
                    reply_user = None  # Si no es un ObjectId válido, usuario anónimo
            replies.append({
                "content": reply["content"],
                "username": reply_user["username"] if reply_user else "Anónimo"
            })

        result.append({
            "content": comment["content"],
            "username": user["username"] if user else "Anónimo",
            "replies": replies  # Añade las respuestas en el resultado
        })
    
    return result

@rt.post("/{comment_id}/reply")
async def reply_to_comment(comment_id: str, reply: Reply):
    # Buscar el comentario por su ID
    comment = data_base.comments.find_one({"_id": ObjectId(comment_id)})
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    # Agregar la nueva respuesta a la lista de respuestas del comentario
    new_reply = {
        "content": reply.content,
        "user_id": reply.user_id
    }
    data_base.comments.update_one(
        {"_id": ObjectId(comment_id)},
        {"$push": {"replies": new_reply}}  # Utiliza $push para añadir la respuesta
    )

    return {"message": "Respuesta añadida correctamente"}