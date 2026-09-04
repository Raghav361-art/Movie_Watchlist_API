from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base
from app.routers import movie





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
    



class MovieResponse(BaseModel):
    id: int
    title: str
    director: str 
    genre: str
    release_year: int
    watched: bool = False
    rating: int | None
    created_at: datetime
    user_id: int
    user: UserResponce
    

    class Config:
        from_attributes = True

class MovieWithLikes(BaseModel):
    Movie: MovieResponse
    likeCount: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    movie_id: int
    dir: bool

