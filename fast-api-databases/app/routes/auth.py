from app.models.auth import CreateUserRequest, User
from app.utils.dependencies import auth_form_dependency, db_dependency
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from starlette import status

router = APIRouter(prefix="/auth")

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _authenticate_user(username: str, password: str, db) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return context.verify(password, user.hashed_password)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
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


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: auth_form_dependency, db: db_dependency):
    user = _authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed authentication. Invalid credentials",
        )
    return "Successful authentication"
