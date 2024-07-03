from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter()

@router.get("/sections/{id}")
async def read_section(id: int):
    return {"courses": []}

@router.get("/sections/{id}/content-blocks")
async def read_section_content_blocks(id: int):
    return {"courses": []}

@router.get("/content-blocks")
async def read_content_block():
    return {"courses": []}

app.include_router(router)
