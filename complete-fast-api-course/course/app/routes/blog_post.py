from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = ({"key": "value1"},)
    image: Optional[Image] = None


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"id": id, "data": blog, "version": version}


@router.post("/new/{id}/comment")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: int = Query(
        None,
        alias="commentId",
        title="Id of the comment",
        description="Some description for comment_id",
    ),
    content: str = Body(..., min_length=10, max_length=12, regex="^[a-z\s]*$"),
    v: Optional[List[str]] = Query(None),
    comment_id: int = Path(gt=5, le=10),
):
    return {
        "body": blog,
        "id": id,
        "comment_title": comment_title,
        "comment_id": comment_id,
        "content": content,
    }
