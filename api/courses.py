from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter()

@router.get("/courses/")
async def read_courses():
    return {"courses": []}

@router.post("/courses")
async def create_course_api():
    return {"courses": []}

@router.get("/courses/{id}")
async def read_course(id: int):
    return {"courses": []}

@router.patch("/courses/{id}")
async def update_course(id: int):
    return {"courses": []}

@router.delete("/courses/{id}")
async def delete_course(id: int):
    return {"courses": []}

@router.get("/courses/{id}/sections")
async def read_course_sections(id: int):
    return {"courses": []}

app.include_router(router)
