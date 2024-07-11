import fastapi

router = fastapi.APIRouter()


@router.get("/sections/{id}")
def read_section():
    return {"courses": []}


@router.get("/sections/{id}/content-blocks")
def read_section_content_blocks():
    return {"courses": []}


@router.get("/content-blocks/{id}")
def read_content_block():
    return {"courses": []}
