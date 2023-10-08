from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    username: str
    text: str
    post_id: str


class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime

    class Config:
        orm_mode = True
