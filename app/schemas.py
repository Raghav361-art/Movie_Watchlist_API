from datetime import datetime
from pydantic import BaseModel, EmailStr

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

