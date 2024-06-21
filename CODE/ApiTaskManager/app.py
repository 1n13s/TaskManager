#Main file
from fastapi import FastAPI
from .router.router import router
from .router.tasks import task
from .router.users import user
from .router.auth import auth
import uvicorn

app = FastAPI()
app.include_router(router)
app.include_router(auth)
app.include_router(task)
app.include_router(user)

"""if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)"""
