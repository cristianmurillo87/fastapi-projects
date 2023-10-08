from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Response, status


class BlogType(str, Enum):
    SHORT = "short"
    STORY = "story"
    HOWTO = "howto"


def required_functionality():
    return {"message": "Learning FastAPI is important"}


router = APIRouter(prefix="/blog", tags=["blog"])


@router.get(
    "/all",
    summary="Retrieve all blogs",
    description="The list of available blogs",
)
def get_blogs(
    page=1, page_size: Optional[int] = None, req_parameters: dict = Depends(required_functionality)
):
    return {"message": f"All {page_size} blogs on page {page}", "req": req_parameters}


@router.get("/{id}/comments/{comment_id}", tags=["comment"])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """Simmulates retrieving a comment of a blog

    Args:
        id (int): ID of the blog the comment is to be retrieved from
        comment_id (int): ID of the comment to be retrieved
        valid (bool, optional): Search only among valid comments. Defaults to True.
        username (Optional[str], optional): The username of the persone who made the comment. Defaults to None.

    Returns:
        JSON: a message containing the comment
    """
    return {
        "message": f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"
    }


@router.get("/type/{blog_type}")
def get_blog_type(type: BlogType, req_parameters: dict = Depends(required_functionality)):
    return {"message": f"Blog type: {type}", "req": req_parameters}


@router.get("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def get_blog(id: int, response: Response, req_parameters: dict = Depends(required_functionality)):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id: {id}", "req": req_parameters}
