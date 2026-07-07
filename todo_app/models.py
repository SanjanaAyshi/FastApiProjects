from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# ==========================================
# ENUMS
# ==========================================

class Priority(str,Enum):
    low="low"
    medium="medium"
    high="high"

class Status(str, Enum):
    pending="pending"
    in_progress="in_progress"
    completed="completed"

# ==========================================
# DATABASE MODEL
# ==========================================
class Todo(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    title:str=Field(min_length=3,max_length=100)
    description:Optional[str]=Field(default=None,max_length=500)
    status:Status=Field(default=Status.pending)
    priority:Priority=Field(default=Priority.medium)
    created_at:str=Field(default_factory=lambda:datetime.now().isoformat())