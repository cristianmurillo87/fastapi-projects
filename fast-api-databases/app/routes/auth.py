from datetime import datetime, timedelta
from typing import Union

from app.models.auth import CreateUserRequest, Token, User
from app.utils.dependencies import (
    auth_form_dependency,
    context_dependency,
    db_dependency,
)
from app.utils.security.jwt import create_access_token
from fastapi import APIRouter, HTTPException
from starlette import status

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _authenticate_user(username: str, password: str, db, context) -> Union[None, User]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    context: context_dependency,
    create_user_request: CreateUserRequest,
):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: auth_form_dependency, db: db_dependency, context: context_dependency
):
    user = _authenticate_user(form_data.username, form_data.password, db, context)
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed authentication. Invalid credentials",
        )
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return dict(access_token=token, token_type="bearer")
