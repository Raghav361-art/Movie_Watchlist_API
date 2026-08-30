import stat

from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import select, update, delete

models.Base.metadata.create_all(bind=engine)

sessionDep = Annotated[Session, Depends(get_db)]

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}

@app.post("/movies")
def create(movies: list[schemas.Movie], db: sessionDep):

    list_movies = []

    for movie in movies:
        obj = models.Movie(**movie.model_dump())
        db.add(obj)
        list_movies.append(obj)

    db.commit()
    for mov in list_movies: db.refresh(mov)

    return list_movies
    

@app.get("/movies", response_model=list[schemas.MovieResponse])
def listAll(genre: str | None = None, watched: bool | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None, db: sessionDep = None):
    statement = select(models.Movie)
    if genre:
        statement = statement.where(models.Movie.genre == genre)

    if watched is not None:
        statement = statement.where(models.Movie.watched == watched)

    if limit:
        statement = statement.limit(limit)

    if offset:
        statement = statement.limit(offset)

    if sort == "rating":
        statement = statement.order_by(models.Movie.rating)
    elif sort == "year":
        statement = statement.order_by(models.Movie.release_year)
    elif sort == "title":
        statement = statement.order_by(models.Movie.title)

    movies = db.execute(statement).scalars().all()
    return movies

@app.get("/movies/{id}")
def search(id: int, db: sessionDep):
    statement = select(models.Movie).where(models.Movie.id == id)
    movie = db.execute(statement).scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    return movie

@app.put("/movies/{id}")
def updateVal(id: int, movie: schemas.Movie, db: sessionDep):
    statement = update(models.Movie).where(models.Movie.id == id).values(**movie.model_dump())
    movie = db.execute(statement)

    if movie.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    db.commit()
    return {"success!": "values updated"}



@app.delete("/movies/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteVal(id: int, db: sessionDep):
    statement = delete(models.Movie).where(models.Movie.id == id)
    movie = db.execute(statement)

    if movie.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    db.commit()
    return


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponce)
def createUser(user: schemas.User, db: sessionDep):
    statement = models.Users(**user.model_dump())
    db.add(statement)
    db.commit()
    db.refresh(statement)
    return statement

@app.get("/user", response_model=list[schemas.UserResponce])
def listUses(db: sessionDep):
    statement = select(models.Users)

    users = db.execute(statement).scalars().all()
    return users