from fastapi import FastAPI,Depends,Query
from sqlmodel import Session, select
from typing import Optional
from contextlib import asynccontextmanager

from database import create_db,get_session
from models import Todo,Priority,Status
from schemas import TodoCreate,TodoUpdate,TodoResponse
from dependencies import get_todo_or_404,pagination

# ==========================================
# APP STARTUP
# ==========================================
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db()
    print("database created!")
    yield
    print("app shutting down!")

app=FastAPI(
    title="todo API",
    version="2.0.0",
    lifespan=lifespan
)
# ==========================================
# ROUTES
# ==========================================

@app.get("/")
def home():
    return {"message":"Welcome to Todo API v2 with Database!"}

# CREATE
@app.post("/todos", status_code=201)
def create_todo(
    todo_data:TodoCreate,
    session:Session=Depends(get_session)
):
    # Convert Pydantic model to Database model
    new_todo=Todo(
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
        status=todo_data.status
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return{"message":"todo is created!","todo":new_todo}

# READ ALL
@app.get("/todos")
def get_todo(
    session:Session=Depends(get_session),
    pages:dict=Depends(pagination)
):
    statement=select(Todo).offset(pages['skip']).limit(pages['limit'])
    todos=session.exec(statement).all()
    total=len(session.exec(select(Todo)).all())

    return{
        "total":total,
        "skip":pages["skip"],
        "limit":pages["limit"],
        "todo":todos
    }

# SEARCH
@app.get("/todos/search/")
def search_todo(
    session: Session=Depends(get_session),
    status:Optional[Status]=None,
    priority:Optional[Priority]=None,
    pages:dict=Depends(pagination)
):
    statement=select(Todo)

    if status is not None:
        statement= statement.where(Todo.status ==status)

    if priority is not None:
        statement=statement.where(Todo.priority==priority)

    statement=statement.offset(pages['skip']).limit(pages['limit'])
    todos= session.exec(statement).all()

    return{
        "total":len(todos),
        "filters":{"status":status,"priority":priority},
        "todos":todos
    }

# READ ONE
@app.get("/todos/{todo_id}")
def get_todo(todo: Todo=Depends(get_todo_or_404)):
    return{"todo":todo}

# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(
    todo_data:TodoUpdate,
    todo:Todo=Depends(get_todo_or_404),
    session:Session=Depends(get_session)
):
    if todo_data.title is not None:
        todo.title =todo_data.title
    if todo_data.description is not None:
        todo.description=todo_data.description
    if todo_data.priority is not None:
        todo.priority=todo_data.priority
    if todo_data.status is not None:
        todo.status=todo_data.status
    
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {"message": "todo updated!", "todo":todo}

# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo:Todo=Depends(get_todo_or_404),
    session: Session=Depends(get_session)
):
    session.delete(todo)
    session.commit()

    return{"message": f"todo '{todo.title}' delete!"}

