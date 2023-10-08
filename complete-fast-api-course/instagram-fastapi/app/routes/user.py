from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.database import user
from app.database.database import get_db
from app.schemas.user import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return user.create_user(request, db)
