"""Module that contains a configure function that adds the customized
exception handlers for several raised exceptions"""

from fastapi import Request, status
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from src.schemas.dispatcher_responses import SentMessageResponseSchema
from src.utils.errors import ErrorFormatter, Error


def configure(app: FastAPI):
    """Function that configures an app with several customized exception
    handlers"""

    @app.exception_handler(RequestValidationError)
    def return_proper_error_schema(
        _: Request,
        exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            content=SentMessageResponseSchema(
                success=False,
                errorMessage=ErrorFormatter.format_list(
                    [
                        Error(error["loc"], error["msg"])
                        for error in exc.errors()
                    ]
                ),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(HTTPException)
    def return_proper_error_http_exception(_: Request, exc: HTTPException):
        return JSONResponse(
            content=SentMessageResponseSchema(
                success=False,
                errorMessage=exc.detail,
            ).dict(),
            status_code=exc.status_code,
        )
