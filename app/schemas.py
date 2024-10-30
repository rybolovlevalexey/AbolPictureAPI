from datetime import date
from pydantic import BaseModel, ConfigDict


# модули для данных поступающих в api
class User(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    hashed_password: str


# модели для результатов отправляемых из api эндпоинт
class PictureInfoDB(BaseModel):
    picture_title: str
    path_to_file: str
    upload_date: date
    resolution: str
    size: float

    model_config = ConfigDict(from_attributes=True)