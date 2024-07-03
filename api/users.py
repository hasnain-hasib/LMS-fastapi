from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from  typing import Optional , List, Dict
from fastapi import Path, Query

router = APIRouter()


users = []

class User(BaseModel):
    email :str
    is_active: bool
    bio : Optional[str]
    

@router.get("/users" ,response_model= List[User])
async def root():
    return users 



@router.post("/users")
async def create_user(user: User):
    users.append(user)
    return "Success"


@router.get("/user/{id}")
async def get_user(id:int):
    return {"user": users[id]}
