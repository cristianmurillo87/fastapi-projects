from app.models.auth import ChangePasswordRequest, User
from app.utils.dependencies import context_dependency, db_dependency, user_dependency
from app.utils.security.jwt import decode_access_token
from fastapi import APIRouter, HTTPException
from starlette import status

router = APIRouter(prefix="/users", tags=["Users"])


def assert_user(user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    user: user_dependency,
    db: db_dependency,
):
    assert_user(user)
    authenticated_user = db.query(User).filter(User.id == user.get("id")).first()
    return authenticated_user


@router.patch("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    context: context_dependency,
    request: ChangePasswordRequest,
):
    assert_user(user)
    request_dict = request.model_dump()
    authenticated_user = db.query(User).filter(User.id == user.get("id")).first()
    current_password = request_dict.get("current_password")
    new_password = request_dict.get("new_password")
    if not context.verify(current_password, authenticated_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    setattr(authenticated_user, "hashed_password", context.hash(new_password))
    db.add(authenticated_user)
    db.commit()
