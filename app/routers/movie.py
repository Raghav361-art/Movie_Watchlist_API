from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from .. import schemas, models, database

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)
sessionDep = Annotated[Session, Depends(database.get_db)]

#-----------------------------------------------------------------------------------------------------------------------
# Creates Movies List
#-----------------------------------------------------------------------------------------------------------------------
@router.post("/")
def create(movies: list[schemas.Movie], db: sessionDep):

    list_movies = []

    for movie in movies:
        obj = models.Movie(**movie.model_dump())
        db.add(obj)
        list_movies.routerend(obj)

    db.commit()
    for mov in list_movies: db.refresh(mov)

    return list_movies
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Movies
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.MovieResponse])
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
#-----------------------------------------------------------------------------------------------------------------------
# Searching a Movie By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/{id}")
def search(id: int, db: sessionDep):
    statement = select(models.Movie).where(models.Movie.id == id)
    movie = db.execute(statement).scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    return movie
#-----------------------------------------------------------------------------------------------------------------------
# Updates Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.put("/{id}")
def updateVal(id: int, movie: schemas.Movie, db: sessionDep):
    statement = update(models.Movie).where(models.Movie.id == id).values(**movie.model_dump())
    movie = db.execute(statement)

    if movie.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    db.commit()
    return {"success!": "values updated"}
#-----------------------------------------------------------------------------------------------------------------------
# Deletes Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteVal(id: int, db: sessionDep):
    statement = delete(models.Movie).where(models.Movie.id == id)
    movie = db.execute(statement)

    if movie.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    db.commit()
    return
