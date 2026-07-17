from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional

from app.database import get_session
from app.models.todo import Todo, Priority, Status
from app.schemas.schemas import TodoCreate, TodoUpdate
from app.dependencies.dependencies import get_todo_or_404, pagination
# ==========================================
# CREATE ROUTER
# ==========================================

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)
# prefix="/todos" → All routes here start with /todos automatically
# tags=["Todos"]  → Grouped under "Todos" in /docs page


# ==========================================
# CREATE
# ==========================================

@router.post("/", status_code=201)
#       ^^^^^ ^^^
#    router    "/" because prefix already adds "/todos"
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session)
):
    try:
        new_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            status=todo_data.status
        )
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)

        return {"message": "Todo created!", "todo": new_todo}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")


# ==========================================
# READ ALL
# ==========================================

@router.get("/")
def get_todos(
    session: Session = Depends(get_session),
    pages: dict = Depends(pagination)
):
    statement = select(Todo).offset(pages["skip"]).limit(pages["limit"])
    todos = session.exec(statement).all()
    total = len(session.exec(select(Todo)).all())

    return {
        "total": total,
        "skip": pages["skip"],
        "limit": pages["limit"],
        "todos": todos
    }


# ==========================================
# SEARCH
# ==========================================

@router.get("/search/")
def search_todos(
    session: Session = Depends(get_session),
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    pages: dict = Depends(pagination)
):
    statement = select(Todo)

    if status is not None:
        statement = statement.where(Todo.status == status)
    if priority is not None:
        statement = statement.where(Todo.priority == priority)

    statement = statement.offset(pages["skip"]).limit(pages["limit"])
    todos = session.exec(statement).all()

    return {
        "total": len(todos),
        "filters": {"status": status, "priority": priority},
        "todos": todos
    }


# ==========================================
# READ ONE
# ==========================================

@router.get("/{todo_id}")
def get_todo(todo: Todo = Depends(get_todo_or_404)):
    return {"todo": todo}


# ==========================================
# UPDATE
# ==========================================

@router.put("/{todo_id}")
def update_todo(
    todo_data: TodoUpdate,
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
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

    return {"message": "Todo updated!", "todo": todo}


# ==========================================
# DELETE
# ==========================================

@router.delete("/{todo_id}")
def delete_todo(
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
    session.delete(todo)
    session.commit()
    return {"message": f"Todo '{todo.title}' deleted!"}