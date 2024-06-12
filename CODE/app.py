#Main file
from fastapi import FastAPI
from ApiTaskManager.router.router import router
from ApiTaskManager.router.auth import auth
import uvicorn


app = FastAPI()
app.include_router(router)
app.include_router(auth)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)