from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from .. import schemas, models, database, utils, oauth2
from sqlalchemy.ext.asyncio import AsyncSession

# , get_current_user: int = Depends(oauth2.get_current_user)

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)
sessionDep = Annotated[AsyncSession, Depends(database.get_db)]

#-----------------------------------------------------------------------------------------------------------------------
# Creates New User
#-----------------------------------------------------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponce)
async def createUser(user: schemas.UserRequest, db: sessionDep):
    user_data = user.model_dump()
    user_data["password"] = utils.createHash(user_data["password"])
    statement = models.Users(**user_data)
    db.add(statement)
    try:
        await db.commit()
        await db.refresh(statement)
        return statement
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Users
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.UserResponce])
async def listUses(db: sessionDep, get_current_user = Depends(oauth2.get_current_user)):
    statement = select(models.Users).where(models.Users.id == get_current_user.id)

    users_data = await db.execute(statement)

    return users_data.scalars().all()
#-----------------------------------------------------------------------------------------------------------------------
# Searching a User By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/{id}", response_model=schemas.UserResponce)
async def search(id: int, db: sessionDep, get_current_user = Depends(oauth2.get_current_user)):
    if id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    statement = select(models.Users).where(models.Users.id == id)
    user_data = await db.execute(statement)
    user = user_data.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    return user

