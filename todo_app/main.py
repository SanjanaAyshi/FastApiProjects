from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import Optional
from contextlib import asynccontextmanager

from database import create_db, get_session
from models import Todo, Priority, Status
from schemas import TodoCreate, TodoUpdate, TodoResponse
from dependencies import get_todo_or_404, pagination
from exceptions import (
    NotFoundException,
    DuplicateException,
    BadRequestException,
    ServerException
)
from error_handlers import register_error_handlers


# ==========================================
# APP STARTUP
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    print("Database created!")
    yield
    print("App shutting down!")


app = FastAPI(
    title="Todo API",
    version="2.0.0",
    lifespan=lifespan
)

# Register our custom error handlers
register_error_handlers(app)


# ==========================================
# ROUTES
# ==========================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Welcome to Todo API v2!"
    }


# CREATE
@app.post("/todos", status_code=201)
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session)
):
    try:
        # Check for duplicate title
        existing = session.exec(
            select(Todo).where(Todo.title == todo_data.title)
        ).first()

        if existing:
            raise DuplicateException("Todo with this title")

        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            status=todo_data.status
        )

        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)

        return {
            "success": True,
            "message": "Todo created!",
            "data": new_todo
        }

    except DuplicateException:
        raise
    except Exception as e:
        raise ServerException(f"Failed to create todo: {str(e)}")


# READ ALL
@app.get("/todos")
def get_todos(
    session: Session = Depends(get_session),
    pages: dict = Depends(pagination)
):
    try:
        statement = select(Todo).offset(pages["skip"]).limit(pages["limit"])
        todos = session.exec(statement).all()
        total = len(session.exec(select(Todo)).all())

        return {
            "success": True,
            "total": total,
            "skip": pages["skip"],
            "limit": pages["limit"],
            "data": todos
        }

    except Exception as e:
        raise ServerException(f"Failed to fetch todos: {str(e)}")


# SEARCH
@app.get("/todos/search/")
def search_todos(
    session: Session = Depends(get_session),
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    pages: dict = Depends(pagination)
):
    try:
        statement = select(Todo)

        if status is not None:
            statement = statement.where(Todo.status == status)

        if priority is not None:
            statement = statement.where(Todo.priority == priority)

        statement = statement.offset(pages["skip"]).limit(pages["limit"])
        todos = session.exec(statement).all()

        return {
            "success": True,
            "total": len(todos),
            "filters": {"status": status, "priority": priority},
            "data": todos
        }

    except Exception as e:
        raise ServerException(f"Failed to search todos: {str(e)}")


# READ ONE
@app.get("/todos/{todo_id}")
def get_todo(todo: Todo = Depends(get_todo_or_404)):
    return {
        "success": True,
        "data": todo
    }


# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(
    todo_data: TodoUpdate,
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
    try:
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.priority is not None:
            todo.priority = todo_data.priority
        if todo_data.status is not None:
            todo.status = todo_data.status

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return {
            "success": True,
            "message": "Todo updated!",
            "data": todo
        }

    except Exception as e:
        raise ServerException(f"Failed to update todo: {str(e)}")


# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
    try:
        session.delete(todo)
        session.commit()

        return {
            "success": True,
            "message": f"Todo '{todo.title}' deleted!"
        }

    except Exception as e:
        raise ServerException(f"Failed to delete todo: {str(e)}")