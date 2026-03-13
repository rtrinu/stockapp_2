from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.db.database import engine
from backend.models.models import User
from backend.db.database import init_db
from backend.routes import auth, pages, user
from backend.routes.auth import logout_endpoint

app = FastAPI(
    version="0.1.1",
    docs_url="/docs",
    redoc_url="/redoc",
)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/client")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
