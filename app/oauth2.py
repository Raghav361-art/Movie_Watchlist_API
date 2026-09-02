from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy import select
from . import schemas, database, models, config
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#ALGORITHM
#EXPIRATION TIME

# Use "openssl rand -hex 32" to get the below string
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str, credential_exception):
    try: 
        pay_load = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = pay_load.get("user_id")

        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.execute(select(models.Users).where(models.Users.id == token.id)).scalar_one_or_none()
    
    return user


# token = create_access_token({"id": 20})

# print(token)
# print(decode(token))

# exp = decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTksImV4cCI6MTc4ODEwNDEwMH0.bgyuWKdQhklTQ8M8ZCNyiKZGQDOyFsCosH1LTHbtF70")["exp"]

# print(datetime.fromtimestamp(exp, timezone.utc) - datetime.now(timezone.utc))

## token calculated at different time
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTksImV4cCI6MTc4ODEwNDEwMH0.bgyuWKdQhklTQ8M8ZCNyiKZGQDOyFsCosH1LTHbtF70
# 0:29:59.573507 - diff seen here

## token calculated at different time                                                                                                            
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTksImV4cCI6MTc4ODEwNDEwMH0.bgyuWKdQhklTQ8M8ZCNyiKZGQDOyFsCosH1LTHbtF70
# 0:27:30.924114 - diff seen here