from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field




class UserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponce(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Movie(BaseModel):
    title: str
    director: str 
    genre: str
    release_year: int = Field(ge=1888, le=2100)
    watched: bool = False
    rating: int | None = Field(default=None, ge=0, le=10)
    



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
    

    model_config = ConfigDict(from_attributes=True)

class MovieWithLikes(BaseModel):
    Movie: MovieResponse
    likeCount: int
    liked: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    movie_id: int
    dir: bool

