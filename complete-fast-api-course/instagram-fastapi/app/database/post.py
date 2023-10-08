from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from app.models.post import Post
from app.schemas.post import PostBase


def create(db: Session, request: PostBase):
    new_post = Post(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.now(),
        user_id=request.creator_id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(Post).all()


def delete(db: Session, id: int, user_id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found."
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only the post creator is allowed to delete a post.",
        )

    db.delete(post)
    db.commit()
    return "ok"
