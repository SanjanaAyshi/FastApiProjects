from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import create_db
from app.routes.todo import router as todo_router
from app.error_handlers import register_error_handlers


# ==========================================
# APP STARTUP
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    print("Database created!")
    yield
    print("App shutting down!")


# ==========================================
# CREATE APP
# ==========================================

app = FastAPI(
    title="Todo API",
    version="2.0.0",
    description="A professional Todo API built with FastAPI",
    lifespan=lifespan
)


# ==========================================
# REGISTER ERROR HANDLERS
# ==========================================

register_error_handlers(app)


# ==========================================
# CONNECT ROUTERS
# ==========================================

app.include_router(todo_router, prefix="/api")


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Todo API!",
        "docs": "/docs",
        "endpoints": {
            "all_todos": "/api/todos",
            "single_todo": "/api/todos/{id}",
            "search": "/api/todos/search/?priority=high",
            "create": "POST /api/todos",
            "update": "PUT /api/todos/{id}",
            "delete": "DELETE /api/todos/{id}"
        }
    }