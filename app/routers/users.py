from fastapi import APIRouter, HTTPException
from datetime import timedelta

from app.schemas import User, UserInDB
from app.services import Authorization
from app.crud import UserActions
from config import settings

users_router = APIRouter(prefix="/users")
authorization = Authorization()


# эндпоинт для регистрации пользователей
@users_router.post("/register")
async def post_register_new_user(user: User):
    check_user_res = await UserActions.check_user_name_in_db(user.username)
    if check_user_res:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = authorization.get_password_hash(user.password)
    db_user = UserInDB(username=user.username, hashed_password=hashed_password)
    await UserActions.add_new_user(**db_user.model_dump())
    return {"msg": "User registered successfully"}


# эндпоинт для авторизации пользователей
@users_router.post("/login")
async def post_login_user(user: User):
    db_user = await UserActions.get_user_by_name(user.username)
    if db_user is None or not authorization.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorization.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
