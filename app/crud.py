from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import User, PictureInfo, async_session_maker


class UserActions:
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
