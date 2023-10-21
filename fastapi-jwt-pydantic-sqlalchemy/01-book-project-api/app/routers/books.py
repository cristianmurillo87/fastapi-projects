from typing import List, Optional, Union

from app.models.books import Book
from app.schemas.books import BookRequest
from fastapi import APIRouter, HTTPException, Path, Query, status

BOOKS = [
    Book(1, "Computer Science  Pro", "codingwithcris", "A very nice book!", 5, 2023),
    Book(2, "Be Fast with FastAPI", "codingwithcris", "A great book!", 5, 2021),
    Book(3, "Master Endpoints", "codingwithcris", "An awesome book!", 5, 2021),
    Book(4, "HP1", "Author 1", "Book description", 3, 2012),
    Book(5, "HP2", "Author 2", "Book description", 2, 2015),
    Book(6, "HP3", "Author 3", "Book description", 1, 2014),
]

router = APIRouter(prefix="/books")


@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# Validate book_id query param using the Path class.
# In the example below, book_id should be greater than 0
@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    found_books = list(filter(lambda x: x.id == book_id, BOOKS))
    if len(found_books) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID: {book_id} not found.",
        )
    return found_books[0]


# Validate query params using the Query class.
# It works exactly like the Path class explained above
@router.get("/", status_code=status.HTTP_200_OK)
async def find_books_by_params(
    rating: Union[int, None] = Query(ge=0, le=5, default=None),
    published_date: Union[int, None] = Query(ge=1999, default=None),
):
    filtered = [book for book in BOOKS]

    if rating is not None:
        filtered = list(filter(lambda book: book.rating == rating, filtered))
    if published_date is not None:
        filtered = list(
            filter(lambda book: book.published_date == published_date, filtered)
        )

    return filtered


@router.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)


@router.put("/update-book/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_request: BookRequest):
    books = list(filter(lambda x: x.id == book_id, BOOKS))
    found_book = books[0] if len(books) > 0 else None

    if found_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID: {book_id} not found.",
        )

    books_dict = book_request.model_dump()
    books_dict["id"] = book_id
    new_book = Book(**books_dict)

    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[index] = new_book
    return new_book


@router.delete("/delete-book/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)) -> bool:
    found = list(filter(lambda x: x.id == book_id, BOOKS))
    deleted = len(found)
    BOOKS = list(filter(lambda x: x.id != book_id, BOOKS))
    return dict(deleted=bool(deleted > 0), items=deleted)


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
