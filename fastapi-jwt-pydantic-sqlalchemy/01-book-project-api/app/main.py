import os

import uvicorn
from app.routers import books
from fastapi import FastAPI

app = FastAPI()


app.include_router(books.router)

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", port=3000, log_level="info", reload=True)
