from typing import Union
import uvicorn
from fastapi import FastAPI
import sys
from api import users, sections, courses
import fastapi
from db.db_setup import engine
from db.models import user, course

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API LMS",
    description="LMS for managing students and courses.",
    version="0.0.1",
    contact={
        "name": "hasib",
        "email": "hasibjoy332@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)


app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

