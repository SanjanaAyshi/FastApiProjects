from fastapi import Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.models.todo import Todo
from app.exceptions import NotFoundException


def get_todo_or_404(
    todo_id: int,
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise NotFoundException("Todo", todo_id)
        #     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #     Using our custom exception now!
        #     Instead of: raise HTTPException(404, "Todo not found")
    return todo


def pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, gt=0, le=100)
):
    return {"skip": skip, "limit": limit}