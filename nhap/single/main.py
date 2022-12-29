from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
from uuid import UUID
from fastapi import FastAPI, HTTPException, Request


# from fastapi_login import LoginManager

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=2)
    author: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100, title='Book desc')
    rating: float = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "11f4c2ea-1340-41f4-89f7-2852347bb0d1",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75
            }
        }


class BookOut(Book):
    # id: UUID
    title: str = Field(min_length=2)
    author: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100, title='Book desc')
    # rating: float = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                # "id": "11f4c2ea-1340-41f4-89f7-2852347bb0d1",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                # "rating": 75
            }
        }

BOOKS = []


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return  # ??? what the fuck is this logic


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return} "
                            f"books? You need to read more!"}
    )


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# @app.get("/", response_class=HTMLResponse)
@app.get("/")
async def read_all_books(books_to_return: int | None = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS
    # return generate_html_response()


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header_Error":
                                  "Nothing to be seen at the UUID"})


# @app.get("/book/{book_id}", response_model=BookOut)
@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/book/search/{book_id}")
async def search_book(part: str):
    for x in BOOKS:
        if part in str(x.id):
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="71f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="21f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="31f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="41f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
