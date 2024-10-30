from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import User, PictureInfo, async_session_maker


class CrudPictureActions:
    def __init__(self):
        pass

    @staticmethod
    async def add_new_picture(picture_title: str, path_to_file: str, resolution: tuple[int, int], size: float):
        session: AsyncSession
        async with async_session_maker() as session:
            new_picture = PictureInfo(picture_title=picture_title, path_to_file=path_to_file,
                                      resolution=f"{resolution[0]}-{resolution[1]}", size=size)
            session.add(new_picture)
            await session.commit()


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
