from fastapi import APIRouter


pictures_router = APIRouter(prefix="/pictures")


@pictures_router.post("/new")
async def post_new_picture():
    pass


@pictures_router.get("/list")
async def get_all_pictures_list():
    pass


@pictures_router.get("/info/{picture_id}")
async def get_picture_info_by_id(picture_id: int):
    pass


@pictures_router.put("/info/{picture_id}")
async def update_picture_info_by_id(picture_id: int):
    pass


@pictures_router.delete("/{picture_id}")
async def delete_picture_by_id(picture_id: int):
    pass
