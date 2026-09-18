from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from . import models, config, oauth2
from .database import engine, get_db
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from .routers import movie, user, auth, vote
import redis.asyncio as aioredis


sessionDep = Annotated[AsyncSession, Depends(get_db)]

app = FastAPI()

redis_client = aioredis.Redis(host=config.settings.redis_hostname, port=config.settings.redis_port, decode_responses=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in config.settings.cors_origins.split(",") if origin.strip()],
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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    cache_key = "view:home"

    try:
        cache_html = await redis_client.get(cache_key)
    except Exception:
        cache_html = None
    if cache_html:
        return HTMLResponse(content=cache_html)

    response = templates.TemplateResponse(request, "index.html")
    cache = response.body.decode("utf-8")

    try:
        await redis_client.setex(cache_key, 1800, cache)
    except Exception:
        pass
    
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    cache_key = f"view:dashboard"

    try:
        cache_html = await redis_client.get(cache_key)
    except Exception:
        cache_html = None
    if cache_html:
        return HTMLResponse(cache_html)

    response = templates.TemplateResponse(request, "dashboard.html")
    cache = response.body.decode("utf-8")

    try:
        await redis_client.set(cache_key, cache, 30)
    except Exception:
        pass
    return response

@app.get("/api")
def root():
    return {"Message": "Hello, I'm Raghav", "Instructions": "Explore my API at www.raghav-art.me/docs"}