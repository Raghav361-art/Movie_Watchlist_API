from datetime import datetime
from pydantic import BaseModel, EmailStr

class Movie(BaseModel):
    title: str
    director: str 
    genre: str
    release_year: int
    watched: bool = False
    rating: int

class MovieResponse(Movie):
    id: int

    class Config:
        orm_mode = True



class User(BaseModel):
    id: int
    email: EmailStr
    password: str    
    created_at: datetime


class UserResponce(BaseModel):
    id: int 
    email: EmailStr

    class Config:
        orm_mode = True