from fastapi import FastAPI, Depends, HTTPException
import models
from database_sql import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_current_user, get_user_exception

app = FastAPI()

# create DB
models.Base.metadata.create_all(bind=engine)


class Todo(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Todos part
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    # return {"Hello": "Hung"}
    return db.query(models.Todos).all()  # No data


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return successful_response(201)
