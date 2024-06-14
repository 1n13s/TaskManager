#Main app file
from fastapi import FastAPI
from ApiTaskManager.router.router import router
from ApiTaskManager.router.tasks import task
from ApiTaskManager.router.users import user
from ApiTaskManager.router.auth import auth
import uvicorn


app = FastAPI()
app.include_router(task)
app.include_router(user)
app.include_router(auth)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)