from fastapi import APIRouter, File, UploadFile, Depends

from app.get_current_user import get_current_user

pictures_router = APIRouter(prefix="/pictures")


@pictures_router.post("/upload")
async def post_new_picture(file: UploadFile = File(...),
                           current_user: str = Depends(get_current_user)):
    return "ok"


@pictures_router.get("/list")
async def get_all_pictures_list():
    pass


@pictures_router.get("/info/{picture_id}")
async def get_picture_info_by_id(picture_id: int):
    pass


@pictures_router.put("/info/{picture_id}")
async def update_full_picture_info_by_id(picture_id: int):
    pass


@pictures_router.patch("/info/{picture_id}")
async def update_part_picture_info_by_id(picture_id: int):
    pass


@pictures_router.delete("/{picture_id}")
async def delete_picture_by_id(picture_id: int):
    pass
