from datetime import datetime

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentBase


def create(db: Session, request: CommentBase):
    new_comment = Comment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.id == post_id)
