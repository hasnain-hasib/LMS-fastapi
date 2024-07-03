from fastapi import FastAPI
from pydantic import BaseModel
from  typing import Optional , List, Dict
from fastapi import Path, Query



app = FastAPI(
    title="Fast API LMS",
    description="LMS for student",
    version="0.0.1",
   
    contact={
        "name": "Hasnain Hasib",
        
        "email": "hasibjoy332@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


users = []

class User(BaseModel):
    email :str
    is_active: bool
    bio : Optional[str]
    


@app.get("/users" ,response_model= List[User])
async def root():
    return users 



@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return "Success"


@app.get("/user/{id}")
async def get_user(
        id:int = Path(..., description = "The id of the user you want to get" ,gt=2),
        q:str = Query(None,max_length= 5)             
                    
        ):
    return {"user": users[id], "query": q}

