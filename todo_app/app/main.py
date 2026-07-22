from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db
from app.routes.todo import router as todo_router
from app.error_handlers import register_error_handlers
from app.middleware import ProcessTimeMiddleware,LoggingMiddleWare

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
# MIDDLEWARE
# ==========================================

# Middleware 1: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Middleware 2: Process Time
app.add_middleware(ProcessTimeMiddleware)

# Middleware 3: Logging
app.add_middleware(LoggingMiddleWare)

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