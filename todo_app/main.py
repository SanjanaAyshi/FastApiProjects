from fastapi import FastAPI
from typing import Optional
app=FastAPI(
    title="ToDo Api",
    description="A simple Todo API build with fastApi",
    version="1.0.0"
)
#home
@app.get("/")
def home():
    return {"message": "Welcome to Todo API!"}

#about
@app.get("/about")
def about():
    return{
        "app_name": "Todo API",
        "version": "1.0.0",
        "author": "Sanjana"
    }

# Health check endpoint (very common in production APIs)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ─── Fake data (we'll use database later) ───
fake_todos = [
    {"id": 1, "title": "Learn FastAPI", "completed": False, "priority": "high"},
    {"id": 2, "title": "Build Todo App", "completed": False, "priority": "high"},
    {"id": 3, "title": "Buy groceries", "completed": True, "priority": "low"},
    {"id": 4, "title": "Read a book", "completed": False, "priority": "medium"},
    {"id": 5, "title": "Exercise", "completed": True, "priority": "medium"},
]

# GET all todos
@app.get("/todos")
def get_all_todos():
    return {"total": len(fake_todos), "todos": fake_todos}


# Search with filters (Query Parameters)
@app.get("/todos/search/")
def search_todos(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: int = 10
):
    results = fake_todos

    if completed is not None:
        results = [t for t in results if t["completed"] == completed]

    if priority is not None:
        results = [t for t in results if t["priority"] == priority]

    results = results[:limit]

    return {
        "total": len(results),
        "filters": {"completed": completed, "priority": priority, "limit": limit},
        "todos": results
    }


# GET specific todo (Path Parameter)
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in fake_todos:
        if todo["id"] == todo_id:
            return {"todo": todo}
    return {"error": "Todo not found"}