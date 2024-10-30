from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from PIL import Image
import os
from math import log


from config import settings


class Authorization:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # создание токена
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    # проверка пароля на корректность
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # получение хэша пароля
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)


class PictureActions:
    def __init__(self, file_name: str, image: Image.Image):
        self.file_name = file_name
        self.image = image
        self.images_to_save: dict[str, Image.Image] = {}

    # Преобразует размер в байтах в более удобные единицы (КБ или МБ)
    @staticmethod
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0 Bytes"
        size_name = ("Bytes", "KB", "MB", "GB")
        i = int(log(size_bytes, 1024))
        p = round(size_bytes / (1024 ** i), 2)
        return f"{p} {size_name[i]}"

    def get_metadata(self) -> dict:
        metadata_dict = dict()

        # Получаем разрешение (ширина и высота)
        width, height = self.image.size

        # Формируем словарь с информацией
        metadata_dict = {
            "resolution": {
                "width": width,
                "height": height
            }
        }

        return metadata_dict

    def change_size(self, width: int = 100, height: int = 100):
        resized_img = self.image.resize([width, height])
        self.images_to_save[f"resized_{width}to{height}"] = resized_img

    def conversion_to_gray_shade(self):
        gray_img = self.image.convert("L")
        self.images_to_save["gray_shade"] = gray_img

    def save_images(self) -> list[str]:
        output_dirs = list()
        for key, value in self.images_to_save.items():
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Путь до корня проекта
            data_folder = os.path.join(base_dir, "data")  # Путь к папке 'data'

            # Создаем папку, если она не существует
            os.makedirs(data_folder, exist_ok=True)

            # Полный путь для сохранения изображения
            file_path = os.path.join(data_folder, f"{key}_{self.file_name}")
            value.save(file_path)

            output_dirs.append(os.path.join("data", f"{key}_{self.file_name}"))

        return output_dirs
