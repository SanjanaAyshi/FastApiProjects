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

# ==========================================
# FAKE DATABASE
# ==========================================
fake_db=[]
id_count=0

# ==========================================
# Helper Function
# ==========================================
def find_todo(todo_id:int):
    for todo in fake_db:
        if todo[id]==todo_id:
            return todo
        return None

# ==========================================
# ROUTES
# ==========================================
@app.get("/")
def home():
    return{
        "message":"Welcome to Todo API"
    }

@app.post("/todos", status_code=201)
def create_todo(todo:TodoCreate):
    global id_count
    id_count=1

    new_todo={
        "id": id_count,
        "title":todo.title,
        "description":todo.description,
        "priority":todo.priority,
        "status":todo.status,
        "created_at":datetime.now().isoformat()
    }
    fake_db.append(new_todo)

    return{ "message":"todo is created successfully.", "todo":new_todo }

@app.get("/todos")
def getTodos():
    return{"total":len(fake_db), "todos":fake_db}

@app.get("/todos/search/")
def search_todo(
    status:Optional[Status]=None,
    priority:Optional[Priority]=None,
    limit: int=Field(default=10,gt=0,le=100)
):
    results=fake_db

    if status is not None:
        results=[t for t in results if t["status"]==status]
    
    if priority is not None:
        results=[t for t in results if t['priority']==priority]

    results=results[:limit]

    return{
        "total": len(results),
        "filters":{"status": status,"priority":priority,"limit":limit},
        "todos":results
    }

@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    todo=find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404,detail="todo not found")
    return{"todo":todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, todo_date:TodoUpdate):
    todo=find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="todo is not found")
    
    if todo_date.title is not None:
        todo["title"]= todo_date.title
    if todo_date.description is not None:
        todo['description']=todo_date.description
    if todo_date.priority is not None:
        todo['priority']=todo_date.priority
    if todo_date.status is not None:
        todo["status"]=todo_date.status
    
    return {
        "message": "todo updated Successfully!!",
        "todo":todo
    }


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    fake_db.remove(todo)
    return {"message": f"Todo '{todo['title']}' deleted successfully!"}