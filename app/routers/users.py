from fastapi import APIRouter, HTTPException
from datetime import timedelta

from app.schemas import User, UserInDB
from app.services import Authorization
from config import settings

users_router = APIRouter(prefix="/users")
authorization = Authorization()


# TODO: заменить на таблицу пользователей в бд
fake_users_db = {}


# эндпоинт для регистрации пользователей
@users_router.post("/register")
async def post_register_new_user(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = authorization.get_password_hash(user.password)
    fake_users_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
    return {"msg": "User registered successfully"}


# эндпоинт для авторизации пользователей
@users_router.post("/login")
async def post_login_user(user: User):
    db_user = fake_users_db.get(user.username)
    if not db_user or not authorization.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorization.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
