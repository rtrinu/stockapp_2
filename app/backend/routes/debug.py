from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await render_error(request, exc)


async def render_error(request: Request, exc: Exception):
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
