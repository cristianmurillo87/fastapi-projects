from app.config.databases.postgres import engine
from app.models.questions import Base
from app.routes import auth, questions, todos
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(questions.router)
