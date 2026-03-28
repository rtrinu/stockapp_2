from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.db.database import engine
from backend.models.models import User
from backend.db.database import init_db
from backend.auth.routes import router as auth_router
from backend.routes import user
from backend.routes import pages

from pathlib import Path

app = FastAPI(
    version="0.1.3",
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
static_path = Path(__file__).parent / "frontend/static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(pages.router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user.router, prefix="/client")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
