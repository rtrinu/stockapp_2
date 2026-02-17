from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/")
def root():
    return RedirectResponse(url="/home")


@router.get("/home")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
