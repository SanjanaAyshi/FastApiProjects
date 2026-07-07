#Why separate from models.py?

#models.py  = What the DATABASE looks like
#schemas.py = What the CLIENT sends/receives

from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Optional
from models import Priority,Status

class TodoCreate(BaseModel):
    title:str=Field(
        ...,
        min_length=3,
        max_length=100,
        description="Title of the todo"
    )
    description:Optional[str]=Field(
        None,
        max_length=500,
        description="detailed description"
    )
    priority:Priority=Field(
        default=Priority.medium,
        description="Priority Level"
    )
    status:Status=Field(
        default=Status.pending,
        description="Current status"
    )

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty_spaces(cls,v):
        if v.strip()=="":
            raise ValueError("title cant be just spaces")
        return v.strip()
    
    @field_validator('title')
    @classmethod
    def title_must_start_with_capital(cls,v):
        if v[0].islower():
            return v.capitalize()
        return v
    @model_validator(mode='after')
    def check_completed_priority(self):
        if self.status == Status.completed and self.priority==Priority.high:
            raise ValueError("Completed todos should not have high priority.")
        return self

# What client SENDS to update a todo
class TodoUpdate(BaseModel):
    title:Optional[str] =Field(None, min_length=3, max_length=100)
    description:Optional[str]=Field(None, max_length=500)
    priority:Optional[Priority]=None
    status:Optional[Status]=None

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty_spaces(cls,v):
        if v is not None and v.strip()=='':
            raise ValueError("Title cannot be just spaces")
        if v is not None:
            return v.strip()
        return v
    
# What client RECEIVES (response)
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority
    status: Status
    created_at: str    

