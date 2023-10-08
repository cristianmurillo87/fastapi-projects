import random
import shutil
import string
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app.auth.oauth2 import get_current_user
from app.database import post
from app.database.database import get_db
from app.schemas.post import PostBase, PostDisplay
from app.schemas.user import UserAuth

router = APIRouter(prefix="/post", tags=["post"])

image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    if not request.image_url_type in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type only accepts 'absolute' or 'relative' as values ",
        )
    return post.create(db, request)


@router.get("/all", response_model=List[PostDisplay])
def get_all(db: Session = Depends(get_db)):
    return post.get_all(db)


@router.post("/image")
def upload_image(
    image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)
):
    letters = string.ascii_letters
    random_string = "".join(random.choice(letters) for i in range(10))
    new = f"_{random_string}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"filename": path}


@router.delete("/delete/{id}")
def delete(
    id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)
):
    return post.delete(db, id, current_user.id)
