from app.models.todos import CreateTodoRequest, Todo
from app.schemas.schemas import individual_serial, list_serial
from app.utils.dependencies.auth import user_dependency
from app.utils.dependencies.database import mongo_dependency
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path
from starlette import status

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, collection: mongo_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!."
        )

    todos = collection.find({"author": int(user.get("id"))})
    serialized_data = list_serial(todos)
    return serialized_data


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, collection: mongo_dependency, todo_id: str):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!."
        )
    todo_model = collection.find_one(
        {"author": int(user.get("id")), "_id": ObjectId(todo_id)}
    )

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} was not found",
        )
    return individual_serial(todo_model)


@router.post("/")
async def create_todo(
    user: user_dependency, collection: mongo_dependency, todo_request: CreateTodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!."
        )
    todo_model = Todo(**todo_request.model_dump(), author=user.get("id"))
    result = collection.insert_one(todo_model.model_dump())
    inserted_todo = collection.find_one({"_id": result.inserted_id})
    return inserted_todo


@router.put("/{id}")
async def update_todo(
    user: user_dependency, collection: mongo_dependency, id: str, todo: Todo
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!."
        )
    collection.find_one_and_update(
        {"_id": ObjectId(id), "author": int(user.get("id"))}, {"$set": dict(todo)}
    )
    updated = collection.find_one({"_id": ObjectId(id), "author": int(user.get("id"))})
    return individual_serial(updated)


@router.delete("/{id}")
async def delete_todo(user: user_dependency, collection: mongo_dependency, id: str):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!."
        )
    deleted_items = collection.find_one_and_delete(
        {"_id": ObjectId(id), "author": int(user.get("id"))}
    )
    return len(deleted_items.values()) > 0
