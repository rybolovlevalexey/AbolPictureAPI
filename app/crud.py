from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
import asyncio

from app.schemas import PictureInfoDB
from app.models import User, PictureInfo, async_session_maker


class CrudPictureActions:
    def __init__(self):
        pass

    @staticmethod
    async def check_picture_id_in_db(picture_id) -> bool:
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(PictureInfo).where(PictureInfo.id == picture_id)
            query_res = await session.execute(query)
            pictures_list = query_res.scalars().all()
            if len(pictures_list) == 0:
                return False
            return True

    @staticmethod
    async def get_all_pictures_info():
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(PictureInfo)
            query_res = await session.execute(query)
            pictures_list = query_res.scalars().all()
            if len(pictures_list) == 0:
                return None
            return [PictureInfoDB.model_validate(elem) for elem in pictures_list]

    @staticmethod
    async def get_info_by_id(picture_id: int) -> None | PictureInfoDB:
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(PictureInfo).where(PictureInfo.id == picture_id)
            query_res = await session.execute(query)
            cur_picture = query_res.scalar_one_or_none()
            if cur_picture is None:
                return None
            return PictureInfoDB.model_validate(cur_picture)

    @staticmethod
    async def add_new_picture(picture_title: str, path_to_file: str, resolution: tuple[int, int], size: float):
        session: AsyncSession
        async with async_session_maker() as session:
            new_picture = PictureInfo(picture_title=picture_title, path_to_file=path_to_file,
                                      resolution=f"{resolution[0]}-{resolution[1]}", size=size)
            session.add(new_picture)
            await session.commit()

    @staticmethod
    async def delete_picture(picture_id: int) -> bool:
        try:
            session: AsyncSession
            async with async_session_maker() as session:
                query = delete(PictureInfo).where(PictureInfo.id == picture_id)
                await session.execute(query)
                await session.commit()
        except Exception:
            return False
        return True

    @staticmethod
    async def get_picture_path_by_id(picture_id: int) -> str | None:
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(PictureInfo.path_to_file).where(PictureInfo.id == picture_id)
            query_res = await session.execute(query)
            query_res = query_res.scalar_one_or_none()
            return query_res


class CrudUserActions:
    def __init__(self):
        pass

    # добавление нового пользователя
    @staticmethod
    async def add_new_user(username: str, hashed_password: str):
        session: AsyncSession
        async with async_session_maker() as session:
            new_user = User(username=username, hashed_password=hashed_password)
            session.add(new_user)
            await session.commit()

    # проверка на наличие в базе данных пользователя с переданным логином
    @staticmethod
    async def check_user_name_in_db(username: str) -> bool:
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(User).where(User.username == username)
            query_res = await session.execute(query)
            if len(query_res.scalars().all()) > 0:
                return True
            return False

    # получение пользователя по его логину
    @staticmethod
    async def get_user_by_name(username: str) -> User | None:
        session: AsyncSession
        async with async_session_maker() as session:
            query = select(User).where(User.username == username)
            query_res = await session.execute(query)
            query_res = query_res.scalars().all()
            if len(query_res) == 0:
                return None
            db_user = query_res[0]
            return db_user


from pprint import pprint
# print([elem.model_dump_json() for elem in asyncio.run(CrudPictureActions.get_all_pictures_info())])