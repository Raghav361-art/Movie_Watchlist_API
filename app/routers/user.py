from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import schemas, models, database, utils

# , get_current_user: int = Depends(oauth2.get_current_user)

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)
sessionDep = Annotated[Session, Depends(database.get_db)]

#-----------------------------------------------------------------------------------------------------------------------
# Creates New User
#-----------------------------------------------------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponce)
def createUser(user: schemas.UserRequest, db: sessionDep):
    try:
        user.password = utils.createHash(user.password)
        statement = models.Users(**user.model_dump())
        db.add(statement)
        db.commit()
        db.refresh(statement)
        return statement
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Users
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.UserResponce])
def listUses(db: sessionDep):
    statement = select(models.Users)

    users = db.execute(statement).scalars().all()
    return users
#-----------------------------------------------------------------------------------------------------------------------
# Searching a User By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/{id}", response_model=schemas.UserResponce)
def search(id: int, db: sessionDep):
    statement = select(models.Users).where(models.Users.id == id)
    user = db.execute(statement).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    return user