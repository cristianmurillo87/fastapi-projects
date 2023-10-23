from app.config.databases.postgres import engine
from app.models.questions import Base
from app.routes import admin, auth, questions, todos, users
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(questions.router)
app.include_router(users.router)
