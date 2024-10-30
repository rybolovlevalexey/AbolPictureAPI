from fastapi import FastAPI, Depends, HTTPException, status

from app.routers.pictures import pictures_router
from app.routers.users import users_router
from config import settings


app = FastAPI()
app.include_router(users_router)
app.include_router(pictures_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
