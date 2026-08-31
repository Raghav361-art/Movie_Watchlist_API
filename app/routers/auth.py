from typing import Annotated
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from .. import oauth2, schemas, models, database, utils


router = APIRouter(tags=["Authentication"])
sessionDep = Annotated[Session, Depends(database.get_db)]

@router.get("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: sessionDep = None):
    user = db.execute(select(models.Users).where(models.Users.email == credentials.username)).scalar_one_or_none()
    
    if not user:
        # This ensures the endpoint takes roughly the same amount of time to respond whether the username is valid or not
        utils.verify(credentials.password, user.password) # To prevent timing attacks that could be used to enumerate existing usernames
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized Access! Wrong Credentials")
    
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access! Wrong Credentials")

    access_token = oauth2.create_access_token({"user_id": f"{user.id}"})
    
    return {"access token": access_token, "token_type": "bearer"}

     