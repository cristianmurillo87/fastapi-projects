from typing import Union

from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    id: Union[int, None] = Field(title="Id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=0)

    class Config:
        # Example of the request visible in the Swagger documentation
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Coding with Cris",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2022,
            }
        }
