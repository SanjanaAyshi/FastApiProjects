from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def register_error_handlers(app: FastAPI):

    # Handle Pydantic validation errors (422)
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):

        errors = []
        for error in exc.errors():
            errors.append({
                "field": " → ".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "status_code": 422,
                "message": "Validation failed",
                "error_type": "validation_error",
                "errors": errors
            }
        )

    # Handle ALL unexpected errors (500)
    @app.exception_handler(Exception)
    async def general_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status_code": 500,
                "message": "Something went wrong on the server",
                "error_type": "server_error"
            }
        )