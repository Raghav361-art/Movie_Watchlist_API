from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base

class Movie(BaseModel):
    title: str
    director: str 
    genre: str
    release_year: int
    watched: bool = False
    rating: int
    created_at: datetime

class MovieResponse(Movie):
    id: int
    
    class Config:
        orm_mode = True



class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponce(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    