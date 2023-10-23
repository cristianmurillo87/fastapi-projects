from app.schemas.schemas import list_serial
from app.utils.dependencies.auth import user_dependency
from app.utils.dependencies.database import mongo_dependency
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from starlette import status

router = APIRouter(prefix="/admin", tags=["Admin"])


def assert_user(user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )


@router.get("/todo", status_code=status.HTTP_200_OK)
async def find_all(user: user_dependency, collection: mongo_dependency):
    assert_user(user)
    todos = collection.find()
    return list_serial(todos)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, collection: mongo_dependency, todo_id: str
):
    assert_user(user)
    todo_model = collection.find({"_id": ObjectId(todo_id)})
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    collection.find_one_and_delete({"_id": ObjectId(todo_id)})
