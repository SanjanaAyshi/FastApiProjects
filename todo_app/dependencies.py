from fastapi import HTTPException, Depends, Query
from sqlmodel import Session, select
from database import get_session
from models import Todo

def get_todo_or_404(
        todo_id:int,
        session:Session= Depends(get_session)
):
    todo=session.get(Todo,todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo

def pagination(
        skip:int=Query(default=0,ge=0),
        limit:int=Query(default=10,gt=0,le=100)
):
    return{"skip":skip,"limit":limit}