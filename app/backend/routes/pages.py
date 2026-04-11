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


@router.get("/login-page")
def login_page(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@router.get("/signup-page")
def signup_page(request: Request):
    return templates.TemplateResponse("signup_page.html", {"request": request})


@router.get("/orders/market")
def market_order_page(request: Request):
    return templates.TemplateResponse("/orders/market.html", {"request": request})


@router.get("/orders/limit")
def limit_order_page(request: Request):
    return template.TemplateResponse("/orders/limit.html", {"request": request})


@router.get("/orders/stop")
def stop_order_page(request: Request):
    return templates.TemplateResponse("/orders/stop.html", {"request": request})
