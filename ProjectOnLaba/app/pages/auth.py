from fastapi import  Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
import os
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# # def get_token(request: Request):
# #     token = request.cookies.get('users_access_token')
# #     if not token:
# #         raise TokenNoFound
# #     return token
#
# def encode_jwt(payload):
#     expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#     payload["exp"] = expire
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token
#
#
# def decode_jwt(token):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     return payload
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     get_token = decode_jwt(token)
#     return {get_token}
#     # credentials_exception = HTTPException(
#     #     status_code=status.HTTP_401_UNAUTHORIZED,
#     #     detail="Could not validate credentials",
#     #     headers={"WWW-Authenticate": "Bearer"},
#     # )
#     # try:
#     #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     #     user_id: str = payload.get("user_id")
#     #     if user_id is None:
#     #         raise credentials_exception
#     #     return int(user_id)
#     # except JWTError as e:
#     #     raise credentials_exception


def encode_jwt(payload: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id