from bson import ObjectId
from fastapi import APIRouter

from app.config.databases.mongodb import collection
from app.models.todos import Todo
from app.schemas.schemas import list_serial, individual_serial

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/")
async def get_todos():
    todos = collection.find()
    serialized_data = list_serial(todos)
    return serialized_data


@router.post("/")
async def create_todo(todo: Todo):
    result = collection.insert_one(dict(todo))
    new_todo = collection.find_one({"_id": ObjectId(result.inserted_id)})
    return individual_serial(new_todo)


@router.put("/{id}")
async def update_todo(id: str, todo: Todo):
    collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})
    updated = collection.find_one({"_id": ObjectId(id)})
    return individual_serial(updated)


@router.delete("/{id}")
async def delete_todo(id: str):
    deleted_items = collection.find_one_and_delete({"_id": ObjectId(id)})
    return len(deleted_items.values()) > 0
