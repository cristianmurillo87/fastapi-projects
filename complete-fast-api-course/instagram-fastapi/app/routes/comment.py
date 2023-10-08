from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import comment
from app.database.database import get_db
from app.schemas.comment import CommentBase
from app.schemas.user import UserAuth

router = APIRouter(prefix="/comment", tags=["comments"])


@router.get("/all/{post_id}")
def comments(post_id: int, db: Session = Depends(get_db)):
    return comment.get_all(db, post_id)


@router.post("/")
def create(
    request: CommentBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return comment.create(db, request)
