from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from .. import schemas, models, database,oauth2
from sqlalchemy import select, func

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)
sessionDep = Annotated[Session, Depends(database.get_db)]

#-----------------------------------------------------------------------------------------------------------------------
# Creates Movies List
#-----------------------------------------------------------------------------------------------------------------------
@router.post("/")
def create(movies: list[schemas.Movie], db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):

    list_movies = []

    for movie in movies:
        obj = models.Movie(**movie.model_dump(), user_id = get_current_user.id)
        db.add(obj)
        list_movies.append(obj)

    db.commit()
    for mov in list_movies: db.refresh(mov)

    return list_movies
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Movies
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.MovieWithLikes])
def listAll(genre: str | None = None, search: str = "", watched: bool | None = None, limit: int = 10, offset: int = 0, sort: str | None = None, db: sessionDep = None, get_current_user: int = Depends(oauth2.get_current_user)):
    statement = select(
        models.Movie,
          func.count(models.Vote.movie_id).label("likeCount")
          ).where(
              models.Movie.title.contains(search)
              ).outerjoin(
              models.Vote, models.Movie.id == models.Vote.movie_id
              ).group_by(
                  models.Movie.id
                  )
    
    if genre:
        statement = statement.where(models.Movie.genre == genre)

    if watched is not None:
        statement = statement.where(models.Movie.watched == watched)


    if limit < 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="limit should be greater than or equal to 0")
    statement = statement.limit(limit)


    if offset < 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="offset should be greater than or equal to 0")
    statement = statement.offset(offset)


    if sort == "rating":
        statement = statement.order_by(models.Movie.rating)
    elif sort == "year":
        statement = statement.order_by(models.Movie.release_year)
    elif sort == "title":
        statement = statement.order_by(models.Movie.title)

    movies = db.execute(statement).all()
    return movies
#-----------------------------------------------------------------------------------------------------------------------
# Searching a Movie By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/{id}", response_model=schemas.MovieWithLikes)
def search(id: int, db: sessionDep):
    statement = select(
            models.Movie,
              func.count(models.Vote.movie_id).label("likeCount")
              ).where(
                  models.Movie.id == id
                  ).outerjoin(
                    models.Vote, models.Movie.id == models.Vote.movie_id
                    ).group_by(
                        models.Movie.id
                        )
    movie = db.execute(statement).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    return movie
#-----------------------------------------------------------------------------------------------------------------------
# Updates Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.put("/{id}")
def updateVal(id: int, movies: schemas.Movie, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):

    movie = db.execute(select(models.Movie).where(models.Movie.id == id)).scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")

    if movie.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    statement = update(models.Movie).where(models.Movie.id == id).values(**movies.model_dump())
    db.execute(statement)
    db.commit()
    return {"success!": "values updated"}
#-----------------------------------------------------------------------------------------------------------------------
# Deletes Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteVal(id: int, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):


    movie = db.execute(select(models.Movie).where(models.Movie.id == id)).scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")

    if movie.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    
    statement = delete(models.Movie).where(models.Movie.id == id)
    db.execute(statement)
    db.commit()

    return

# @router.patch("/like/{id}")
# def likeCount(id: int, like: bool, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):
#     movie = db.execute(select(models.Movie).where(models.Movie.id == id)).scalar_one_or_none()
#     exists = db.execute(select(models.Likes).where(models.Likes.user_id == get_current_user.id, models.Likes.movie_id == id)).scalar_one_or_none()

#     if movie is None :

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     if like:
#         if exists is None:
#             like = models.Likes(user_id = get_current_user.id, movie_id = movie.id)
#             db.add(like)
#             db.commit()
#             db.refresh(like)
#     else:
#         db.execute(delete(models.Likes).where(models.Likes.user_id == get_current_user.id, models.Likes.movie_id == id))
#         db.commit()

#     return like