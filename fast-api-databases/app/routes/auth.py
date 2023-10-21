from app.models.auth import CreateUserRequest, User
from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter(prefix="/auth")

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=context.hash(create_user_request.password),
        is_active=True,
    )

    return create_user_model
