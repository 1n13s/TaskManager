from fastapi import APIRouter, Request
from starlette import status
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
front = APIRouter(
    prefix="/taskmanager",
    tags=["taskmanager"]
)

#front.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

@front.get("/")
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@front.get("/login")
async def test(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@front.get("/main_page")
async def test(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@front.get("/update_task")
async def test(request: Request):
    return templates.TemplateResponse("update_task.html", {"request": request})

@front.get("/add_user")
async def test(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})
    
