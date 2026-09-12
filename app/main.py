from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import models, config
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware
from .routers import movie, user, auth, vote

sessionDep = Annotated[Session, Depends(get_db)]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Frontend wiring ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(movie.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")

@app.get("/api")
def root():
    return {"Message": "Hello, I'm Raghav", "Instructions": "Explore my API at www.raghav-art.me/docs"}