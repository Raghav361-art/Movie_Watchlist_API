from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from . import schemas

#SECRET_KEY
#ALGORITHM
#EXPIRATION TIME

# Use "openssl rand -hex 32" to get the below string
SECRET_KEY = "5ba6e9348791d2384a6ac3038e9ae2cdc1adb32f8b59ac90ba51157fc757c7e3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str, credential_exception):
    try: 
        pay_load = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = pay_load.get("users_id")

        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

# def get_current_user

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