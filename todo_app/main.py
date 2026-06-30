from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field, field_validator,model_validator
from typing import Optional
from enum import Enum
from datetime import datetime

app= FastAPI(
    title="todo Api",
    version="1.0.0"
)

# ==========================================
# ENUMS
# ==========================================

class Priority(str,Enum):
    low="low"
    medium="medium"
    high="high"

class Status(str,Enum):
    pending="pending"
    in_process="in_Process"
    completed="completed"

# ==========================================
# PYDANTIC MODELS
# ==========================================

class TodoCreate(BaseModel):
    title: str=Field(
        ...,
        min_length=3,
        max_length=100,
        description="Title here"
    )
    description: Optional[str]=Field(
        None,
        max_length=500,
        description="Todo Details here"
    )
    priority:Priority=Field(
        default=Priority.medium,
        description="Set priority level"
    )
    status:Status=Field(
        default=Status.pending,
        description="Set current Status"
    )


    @field_validator('title')
    @classmethod
    def titleMustNotBeEmpty(cls,v):
        if v.strip()==" ":
            raise HTTPException("Title Cant be just space")
        return v.strip()

    @field_validator("title")
    @classmethod
    def titleMustStartWithCapital(cls,v):
        if v[0].islower():
            return v.capitalize()
        return v


    @model_validator(mode='after')
    def checkCompletedPriority(self):
        if self.status==Status.completed and self.priority== Priority.high:
            raise ValueError("Completed status cant have higher priority"
            )
        return self

class TodoUpdate(BaseModel):
    title:Optional[str]=Field(None,min_length=3,max_length=100)
    description:Optional[str]=Field(None,max_length=500)
    priority:Optional[str]=None
    status:Optional[str]=None

    @field_validator('title')
    @classmethod
    def titleMustNotBeEmptySpace(cls,v):
        if v is not None and v.strip()=='':
            raise ValueError ('title Cannot be just spaces')
        if  v is not None:
            return v.strip()
        return v

class TodoResponse(BaseModel):
    id:int
    title:str
    description: Optional[str]=None
    priority:Priority
    status:Status
    created_at:str