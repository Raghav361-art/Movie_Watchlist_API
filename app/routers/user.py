from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import select
from .. import schemas, models, database, utils
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
    try:
        user.password = utils.createHash(user.password)
        statement = models.Users(**user.model_dump())
        db.add(statement)
        await db.commit()
        await db.refresh(statement)
        return statement
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
#-----------------------------------------------------------------------------------------------------------------------
# Lists All The Users
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.UserResponce])
async def listUses(db: sessionDep):
    statement = select(models.Users)

    users_data = await db.execute(statement)

    return users_data.scalars().all()
#-----------------------------------------------------------------------------------------------------------------------
# Searching a User By ID
#-----------------------------------------------------------------------------------------------------------------------
@router.get("/{id}", response_model=schemas.UserResponce)
async def search(id: int, db: sessionDep):
    statement = select(models.Users).where(models.Users.id == id)
    user_data = await db.execute(statement)
    user = user_data.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    return user

