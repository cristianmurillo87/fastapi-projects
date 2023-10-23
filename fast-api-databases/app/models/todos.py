from pydantic import BaseModel


class Todo(BaseModel):
    name: str
    description: str
    complete: bool
    author: int


class CreateTodoRequest(BaseModel):
    name: str
    description: str
    complete: bool
