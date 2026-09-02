from fastapi import FastAPI, Depends
from . import models, config
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .routers import movie, user, auth


models.Base.metadata.create_all(bind=engine)

# Creates Sessions
sessionDep = Annotated[Session, Depends(get_db)]

# FastApi Instance
app = FastAPI()

# Routers
app.include_router(movie.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "hello"}
