from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base





class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponce(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Movie(BaseModel):
    title: str
    director: str 
    genre: str
    release_year: int
    watched: bool = False
    rating: int



class MovieResponse(Movie):
    id: int
    rating: int | None
    user_id: int
    created_at: datetime
    

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    