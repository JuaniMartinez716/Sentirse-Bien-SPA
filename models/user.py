from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    username: str
    password: str
    email: str
    age: int
    