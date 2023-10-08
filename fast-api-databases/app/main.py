from fastapi import FastAPI

from app.config.databases.postgres import engine
from app.models.questions import Base
from app.routes import todos, questions

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(todos.router)
app.include_router(questions.router)
