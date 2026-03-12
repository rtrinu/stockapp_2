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
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
init_db()

templates = Jinja2Templates(directory="frontend/templates")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    status_code = 500
    error_message = "An unexpected internal server error occurred."
    error_title = "Internal Server Error"

    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        error_message = exc.detail
        error_title = f"{exc.status_code} Error"

    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_code": status_code,
            "error_title": error_title,
            "error_message": error_message,
        },
        status_code=status_code,
    )


# return JSONResponse(
#     status_code=500, content={"detail": "An unexpected internal error occurred"}
# )


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
