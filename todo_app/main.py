from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
app=FastAPI(
    title="ToDo Api",
    description="A simple Todo API build with fastApi",
    version="1.0.0"
)
# For CREATING a todo (what client sends)
class TodoCreate(BaseModel):
    title: str
    description: Optional[str]=None
    completed: bool=False
    priority: str ="medium"

# For UPDATING a todo (all fields optional)
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str]=None
    completed: Optional[bool]=False
    priority: Optional[str] ="medium"

# ==========================================
# FAKE DATABASE (list for now)
# ==========================================
fake_db=[]
id_count=0

# ==========================================
# HELPER FUNCTION
# ==========================================
def find_todo(todo_id: int):
    for todo in fake_db:
        if todo["id"] == todo_id:
            return todo
    return None
# ==========================================
# ROUTES / ENDPOINTS
# ==========================================
@app.get("/")
def home():
    return {"message": "Welcome to Todo API"}

# CREATE a todo (POST)
@app.post("/todos",status_code=201)
def create_todo(todo: TodoCreate):
    global id_count
    id_count +=1

    new_todo={
        "id" : id_count,
        "title" : todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "priority": todo.priority
        }
    fake_db.append(new_todo)

    return{
        "message": "Todo is created successfully!",
        "todo": new_todo
    }

# READ all todos (GET)

# READ all todos (GET)
@app.get("/todos")
def get_all_todos():
    return {
        "total": len(fake_db),
        "todos": fake_db
    }

# READ single todo (GET)
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = find_todo(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"todo": todo}

# UPDATE a todo (PUT)
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, todo_data: TodoUpdate):
    todo=find_todo(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found..")
    
    if todo_data.title is not None:
        todo["title"]= todo_data.title
    
    if todo_data.description is not None:
        todo['description']=todo_data.description
    
    if todo_data.completed is not None:
        todo['complete'] =todo_data.completed

    if todo_data.priority is not None:
        todo['priority']= todo_data.priority
    
    return{
        "message": "Todo updated Successfully!!",
        "todo": todo
    }
# DELETE a todo (DELETE)
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    fake_db.remove(todo)

    return {"message": f"Todo '{todo['title']}' deleted successfully!"}