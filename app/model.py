from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String
from database import Base


        
class UserActionSchema(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, primary_key=True)
    actions = Column(String(10))
    user_id = Column(Integer)


class UserSchema(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@doe.com",
                "password": "12345"
            }
        }
 
class TodoSchema(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
