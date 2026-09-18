from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database, oauth2
from typing import Annotated
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

sessionDep = Annotated[AsyncSession, Depends(database.get_db)]

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/")
async def vote(vote: schemas.Vote, db: sessionDep, get_user: int = Depends(oauth2.get_current_user)):
    
    movie_data  = await db.execute(select(models.Movie).where(models.Movie.id == vote.movie_id, models.Movie.user_id == get_user.id))
    movie = movie_data.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    statement = select(models.Vote).where(models.Vote.movie_id == vote.movie_id, models.Vote.user_id == get_user.id)
    exist_check = await db.execute(statement)
    exist = exist_check.scalar_one_or_none()
    
    if vote.dir:
        if exist is None:
            like = models.Vote(user_id = get_user.id, movie_id = vote.movie_id)
            db.add(like)
            await db.commit()
            await db.refresh(like)
            return JSONResponse(status_code=201, content={"vote": "added"})
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already liked")
    else:
        if exist is not None:
            await db.execute(delete(models.Vote).where(models.Vote.movie_id == vote.movie_id, models.Vote.user_id == get_user.id))
            await db.commit()

            return JSONResponse(status_code=200, content={"vote": "removed"})
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="like does not exist")
            
