import time
from ast import List
from enum import Enum

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket

from app.auth import authentication
from app.client import html
from app.db import models
from app.db.database import engine
from app.exceptions import StoryException
from app.routes import article, blog_get, blog_post, dependency, file, product, user

app = FastAPI()
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(dependency.router)


@app.get("/")
async def index():
    return HTMLResponse(html)


clients: List[WebSocket] = []


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    # status code 418: not real http code, only used for testing
    return JSONResponse(status_code=418, content=exc.name)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response


origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/files", StaticFiles(directory="app/files"), name="files")

models.Base.metadata.create_all(engine)
