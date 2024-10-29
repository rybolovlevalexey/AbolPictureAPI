from fastapi import FastAPI

from routers.pictures import pictures_router

app = FastAPI()
app.include_router(pictures_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, )