from pydantic import BaseModel, Field, EmailStr
# Create ToDo Schema (Pydantic Model)
class ToDoCreate(BaseModel):
    task: str

# Complete ToDo Schema (Pydantic Model)
class ToDo(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    fullname: str 
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@doe.com",
                "password": "12345"
            }
        }
        orm_mode = True
        
            
class UserCreateSchema(BaseModel):
    fullname: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@doe.com",
                "password": "12345"
            }
        }

class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john@doe.com",
                "password": "12345"
            }
        }

class UserActionsSchema(BaseModel):
    actions: str
    user_id: int