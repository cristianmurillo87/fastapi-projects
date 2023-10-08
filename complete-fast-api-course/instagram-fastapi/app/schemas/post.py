from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.comment import Comment


class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: str


class PostUser(BaseModel):
    username: str

    class Config:
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: PostUser
    comments: List[Comment]

    class Config:
        orm_mode = True
