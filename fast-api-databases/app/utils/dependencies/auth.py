from typing import Annotated

from app.utils.security.jwt import decode_access_token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from passlib.context import CryptContext
from starlette import status

_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
auth_token_dependency = Annotated[str, Depends(_oauth2_bearer)]


async def _get_current_user(token: auth_token_dependency):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return dict(username=username, id=user_id, role=role)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )


user_dependency = Annotated[dict, Depends(_get_current_user)]


def _get_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


context_dependency = Annotated[CryptContext, Depends(_get_context)]
