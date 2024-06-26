#Main file
from fastapi import FastAPI, Request
from ApiTaskManager.router.router import router
from ApiTaskManager.router.tasks import task
from ApiTaskManager.router.users import user
from ApiTaskManager.router.auth import auth
from front import front
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


import uvicorn
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

app.include_router(router)
app.include_router(auth)
app.include_router(task)
app.include_router(user)
app.include_router(front)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)