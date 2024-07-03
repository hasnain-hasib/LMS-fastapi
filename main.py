from fastapi import FastAPI
from pydantic import BaseModel
from  typing import Optional , List, Dict
from fastapi import Path, Query
from api import users, courses, sections


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

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)

