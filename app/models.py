from sqlalchemy import Integer, String, Float, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import date, datetime

from config import settings


engine = create_async_engine(settings.get_db_url())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class PictureInfo(Base):
    __tablename__ = "pictures_info"

    picture_title: Mapped[str] = mapped_column(String, nullable=False)  # название картинки
    path_to_file: Mapped[str] = mapped_column(String, nullable=False)  # путь к файлу из корня проекта
    upload_date: Mapped[date] = mapped_column(Date, nullable=False, default=datetime.now().date())  # дата загрузки
    resolution: Mapped[str] = mapped_column(String, nullable=False)  # разрешение картинки
    size: Mapped[float] = mapped_column(Float, nullable=False)  # размеры картинки в МБ


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True)  # логин пользователя
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)  # хэш пароля пользователя
    created_at: Mapped[date] = mapped_column(Date, default=datetime.now().date())  # дата регистрации
