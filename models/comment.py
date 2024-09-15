from pydantic import BaseModel
from typing import Optional, List


class Reply(BaseModel):
    content: str
    user_id: Optional[str] = None

class Comment(BaseModel):
    content: str
    post_id: str
    replies: Optional[List[Reply]] = []  # Lista de respuestas por defecto vacía

class User(BaseModel):
    username: str
    
