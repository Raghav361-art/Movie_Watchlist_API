from tkinter import NO

from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session, session
from typing import Annotated
from sqlalchemy import delete, select

sessionDep = Annotated[Session, Depends(database.get_db)]

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: sessionDep, get_user: int = Depends(oauth2.get_current_user)):
    
    movie = db.execute(select(models.Movie).where(models.Movie.id == vote.movie_id)).scalar_one_or_none()
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    statement = select(models.Vote).where(models.Vote.movie_id == vote.movie_id, models.Vote.user_id == get_user.id)
    exist = db.execute(statement).scalar_one_or_none()
    
    if vote.dir == True:
        if exist is None:
            like = models.Vote(user_id = get_user.id, movie_id = vote.movie_id)
            db.add(like)
            db.commit()
            db.refresh(like)
            return like
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already liked")
    else:
        if exist is not None:
            db.execute(delete(models.Vote).where(models.Vote.movie_id == vote.movie_id, models.Vote.user_id == get_user.id))
            db.commit()

            return {"vote": "removed"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="like does not exist")
            