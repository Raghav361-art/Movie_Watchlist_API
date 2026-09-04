from fastapi import FastAPI, Depends
from . import models, config
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .routers import movie, user, auth
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)

# Creates Sessions
sessionDep = Annotated[Session, Depends(get_db)]

# FastApi Instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.google.com/",
        'https://roadmap.sh'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(movie.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "hello"}
