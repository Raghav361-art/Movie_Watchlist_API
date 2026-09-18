from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import select, update, delete, func
from .. import schemas, models, database, oauth2, config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import redis.asyncio as aioredis
from test import QueryMovie

redis_client = aioredis.Redis(host=config.settings.redis_hostname, port=config.settings.redis_port, decode_responses=True)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)
sessionDep = Annotated[AsyncSession, Depends(database.get_db)]

#-----------------------------------------------------------------------------------------------------------------------
# Creates Movies List
#-----------------------------------------------------------------------------------------------------------------------
@router.post("/")
async def create(movies: list[schemas.Movie], db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):

    list_movies = []

    for movie in movies:
        obj = models.Movie(**movie.model_dump(), user_id = get_current_user.id)
        db.add(obj)
        list_movies.append(obj)

    await db.commit()
    for mov in list_movies: await db.refresh(mov)

    return list_movies
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Movies
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.MovieWithLikes])
async def listAll(genre: str | None = None, search: str = "", watched: bool | None = None, limit: int = 10, offset: int = 0, sort: str | None = None, db: sessionDep = None, get_current_user: int = Depends(oauth2.get_current_user)):

    user_liked = (select(models.Vote.movie_id).where(models.Vote.movie_id == models.Movie.id,models.Vote.user_id == get_current_user.id).correlate(models.Movie).exists())
    
    statement = select(
        models.Movie,
          func.count(models.Vote.movie_id).label("likeCount"),
          user_liked.label("liked")
          ).where(
              models.Movie.user_id == get_current_user.id,
              models.Movie.title.contains(search)
              ).outerjoin(
              models.Vote, models.Movie.id == models.Vote.movie_id
              ).options(
                    selectinload(models.Movie.user)
                ).group_by(
                  models.Movie.id
                  )
    
    if genre:
        statement = statement.where(models.Movie.genre == genre)

    if watched is not None:
        statement = statement.where(models.Movie.watched == watched)


    if limit < 0 or limit > 100:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="limit must be between 0 and 100")
    statement = statement.limit(limit)


    if offset < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="offset should be greater than or equal to 0")
    statement = statement.offset(offset)


    if sort == "rating":
        statement = statement.order_by(models.Movie.rating.desc().nullslast(), models.Movie.id)
    elif sort == "year":
        statement = statement.order_by(models.Movie.release_year.desc(), models.Movie.id)
    elif sort == "title":
        statement = statement.order_by(models.Movie.title, models.Movie.id)
    else:
        statement = statement.order_by(models.Movie.created_at.desc(), models.Movie.id.desc())

    movies_data = await db.execute(statement)
    movies = movies_data.all()
    return movies
#-----------------------------------------------------------------------------------------------------------------------
# Searching a Movie By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/search")
async def search_movies(query: str):
    res = QueryMovie(query=query)

    return res.get_all()


@router.get("/{id}", response_model=schemas.MovieWithLikes)
async def search(id: int, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):
    user_liked = (select(models.Vote.movie_id).where(models.Vote.movie_id == models.Movie.id, models.Vote.user_id == get_current_user.id).correlate(models.Movie).exists())

    statement = select(
            models.Movie,
              func.count(models.Vote.movie_id).label("likeCount"),
              user_liked.label("liked")
              ).where(
                  models.Movie.id == id,
                  models.Movie.user_id == get_current_user.id
                  ).outerjoin(
                    models.Vote, models.Movie.id == models.Vote.movie_id
                    ).options(
                        selectinload(models.Movie.user)
                    ).group_by(
                        models.Movie.id
                        )
    movie_data = await db.execute(statement)
    movie = movie_data.first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")
    return movie
#-----------------------------------------------------------------------------------------------------------------------
# Updates Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.put("/{id}")
async def updateVal(id: int, movies: schemas.Movie, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):

    movie_data = await db.execute(select(models.Movie).where(models.Movie.id == id))
    movie = movie_data.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")

    if movie.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    statement = update(models.Movie).where(models.Movie.id == id).values(**movies.model_dump())
    await db.execute(statement)
    await db.commit()
    return {"success!": "values updated"}
#-----------------------------------------------------------------------------------------------------------------------
# Deletes Movies By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteVal(id: int, db: sessionDep, get_current_user: int = Depends(oauth2.get_current_user)):


    movie_data = await db.execute(select(models.Movie).where(models.Movie.id == id))
    movie = movie_data.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with id: {id} not found")

    if movie.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    
    statement = delete(models.Movie).where(models.Movie.id == id)
    await db.execute(statement)
    await db.commit()

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

