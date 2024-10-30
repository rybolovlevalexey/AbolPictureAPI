import json
import shutil
import os
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO

from app.get_current_user import get_current_user
from app.services import PictureActions
from app.crud import CrudPictureActions
from app.schemas import PictureInfoDB

pictures_router = APIRouter(prefix="/pictures")


@pictures_router.post("/upload")
async def post_new_picture(file: UploadFile = File(...),
                           current_user: str = Depends(get_current_user)):
    file_name: str = str(file.filename)
    file_content = await file.read()
    # получение картинки по переданному контенту
    image = Image.open(BytesIO(file_content))
    pic_acts = PictureActions(file_name, image)
    # размер файла в байтах
    file_size_bytes = len(file_content)
    file_size = pic_acts.convert_size(file_size_bytes)

    # базовые операции при загрузке нового изображения, затем сохранение результатов
    pic_acts.change_size(100, 100)
    pic_acts.change_size(500, 500)
    pic_acts.conversion_to_gray_shade()
    pic_acts.save_images()

    pic_metadata = pic_acts.get_metadata()
    await CrudPictureActions.add_new_picture(
        file_name,
        pic_metadata.file_path,
        (pic_metadata.width, pic_metadata.height),
        float(file_size.split()[0]))

    return JSONResponse(status_code=201, content={"msg": "Новое изображение успешно сохранено"})


@pictures_router.get("/list", response_model=list[PictureInfoDB])
async def get_all_pictures_list():
    pictures_list = await CrudPictureActions.get_all_pictures_info()
    if len(pictures_list) == 0:
        return JSONResponse(status_code=204, content="Нет информации об изображениях")
    return JSONResponse(status_code=200, content=[elem.model_dump_json() for elem in pictures_list])


@pictures_router.get("/info/{picture_id}", response_model=PictureInfoDB)
async def get_picture_info_by_id(picture_id: int):
    cur_picture = await CrudPictureActions.get_info_by_id(picture_id)
    if cur_picture is None:
        return JSONResponse(status_code=204, content={"msg": f"Изображение с параметром id={picture_id} не найдено"})
    return JSONResponse(status_code=200, content=cur_picture.model_dump_json())


@pictures_router.put("/info/{picture_id}")
async def update_full_picture_info_by_id(picture_id: int):
    pass


@pictures_router.patch("/info/{picture_id}")
async def update_part_picture_info_by_id(picture_id: int):
    pass


@pictures_router.delete("/{picture_id}")
async def delete_picture_by_id(picture_id: int):
    if not await CrudPictureActions.check_picture_id_in_db(picture_id):
        return JSONResponse(status_code=204, content={
            "msg": f"Изображение с параметром id={picture_id} не найдено"
        })
    picture_path = await CrudPictureActions.get_picture_path_by_id(picture_id)
    # путь до картинки, которую надо удалить (будет удаляться вся её папка, чтобы удалить все производные картинки)
    path_to_picture = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), picture_path
    )
    shutil.rmtree(os.path.dirname(path_to_picture))
    await CrudPictureActions.delete_picture(picture_id)
    return JSONResponse(status_code=200, content={
        "msg": f"Изображение с параметром id={picture_id} удалено успешно"})