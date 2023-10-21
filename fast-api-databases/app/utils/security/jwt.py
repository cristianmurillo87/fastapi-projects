import os
from datetime import datetime, timedelta

from jose import jwt

_JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
_JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = dict(sub=username, id=user_id)
    expires = datetime.utcnow() + expires_delta
    encode.update(dict(exp=expires))
    return jwt.encode(encode, key=_JWT_SECRET_KEY, algorithm=_JWT_ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, key=_JWT_SECRET_KEY, algorithms=[_JWT_ALGORITHM])
