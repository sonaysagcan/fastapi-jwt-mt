from typing import List
from fastapi import FastAPI, Body, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.model import TodoSchema,UserSchema,UserActionSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from database import  SessionLocal
import schemas

app = FastAPI()


async def get_session():
    """db session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def verify_hash_password(plain_password, hashed_password):
    """Verifies that the user password is compatible with the hash."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Generate password hash"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


@app.get("/", tags=["root"])
async def read_root():
    """Root message"""
    return {"message": "Welcome to the ToDo app.Test at http://localhost:8000/docs"}


@app.post("/user/register", tags=["user"])
async def create_user(user: schemas.UserCreateSchema,session: Session = Depends(get_session)):
    """authenticates the user. It records the login."""
    user_db_data = session.query(UserSchema).filter(UserSchema.email==user.email).first()
    if user_db_data:
        return {'success':False, 'detail':"user already registered!"}
    try:
        tododb = UserSchema(fullname = user.fullname, email = user.email, \
            password = get_password_hash(user.password))
        session.add(tododb)
        session.commit()
        session.refresh(tododb)
    except:
        return {'success':False, 'detail':"user register failed!"}
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: schemas.UserLoginSchema = Body(...), \
    session: Session = Depends(get_session)):
    """authenticates the user. It records the login."""
    user_db_data = session.query(UserSchema).filter(UserSchema.email==user.email).first()

    try:
        verify_password = CryptContext(schemes=["bcrypt"], deprecated="auto"). \
            verify(user.password, user_db_data.password)
        if verify_password:
            # insert user action
            tododb = UserActionSchema(actions = "LOGIN", user_id = user_db_data.id)
            session.add(tododb)
            session.commit()
            session.refresh(tododb)
            return signJWT(user.email)
    except:
        return {'success':False, 'detail': "Wrong login details!"}


@app.post("/todo/create", response_model=schemas.ToDo,tags=["todo"], \
    dependencies=[Depends(JWTBearer())])
async def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):
    """create_todo"""
    try:
        tododb = TodoSchema(task = todo.task)
        session.add(tododb)
        session.commit()
        session.refresh(tododb)
    except:
        return {'success':False, 'detail':"todo item not created!"}
    return tododb


@app.get("/todo/fetchall", response_model = List[schemas.ToDo], \
    dependencies=[Depends(JWTBearer())],tags=["todo"])
async def list_all_todos(session: Session = Depends(get_session)):
    """list_all_todos"""
    todo_list = session.query(TodoSchema).all()
    return todo_list


@app.get("/todo/fetchone/{id}", response_model=schemas.ToDo, \
    tags=["todo"],dependencies=[Depends(JWTBearer())])
async def read_specific_todo(id: int, session: Session = Depends(get_session)):
    """read_specific_todo"""
    todo = session.query(TodoSchema).get(id)
    return todo


@app.put("/todo/update/{id}", response_model=schemas.ToDo,tags=["todo"], \
    dependencies=[Depends(JWTBearer())])
async def update_todo(id: int, task: str, session: Session = Depends(get_session)):
    """update_todo"""
    try:
        todo = session.query(TodoSchema).get(id)
        todo.task = task
        session.commit()
    except:
        return {'success':False, 'detail':f"todo item with id {id} not found"}
    return todo

@app.delete("/todo/delete/{id}",tags=["todo"],dependencies=[Depends(JWTBearer())])
async def delete_todo(id: int, session: Session = Depends(get_session)):
    """delete_todo"""
    try:
        todo = session.query(TodoSchema).get(id)
        session.delete(todo)
        session.commit()
    except:
        return {'success':False, 'detail':f"todo item with id {id} not found"}
    return {"success": True, "detail": f"todo item with id {id} deleted"}