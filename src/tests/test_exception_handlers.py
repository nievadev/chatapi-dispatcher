"""Module that contains the tests for exception_handlers module"""

import unittest
import json
from unittest import mock
from typing import cast, Callable

from pydantic import ValidationError
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from src.apiv1 import exception_handlers
from src.schemas.dispatcher_responses import SentMessageResponseSchema
from src.utils.help_functions import get_exception
from src.utils import errors


mock_app = FastAPI()

exception_handlers.configure(mock_app)


class TestExceptionHandlers(unittest.TestCase):
    """Test class that contains tests for exception_handlers module"""

    def test_pydantic_validation_error(self):
        """Test function that checks that the customized RequestValidationError
        exception behaves properly at the time of confuring the app and
        returning an expected response"""

        exception_handler = cast(
            Callable[[Request, Exception], JSONResponse],
            mock_app.exception_handlers.get(RequestValidationError)
        )

        self.assertTrue(exception_handler)

        exc = mock.Mock()

        exc.errors.return_value = (
            {"msg": str(errors.BadProdVariableError), "loc": "PROD"},
            {"msg": str(errors.BadFilenameNotRecognizedError), "loc": "image"},
        )

        response = exception_handler(Request(scope={"type": "http"}), exc)

        response_body = json.loads(response.body)

        def func():
            SentMessageResponseSchema(**response_body)

        self.assertFalse(
            get_exception(
                ValidationError,
                func
            )
        )

        errors_list = errors.ErrorParser.parse_list(
            response_body["errorMessage"]
        )

        self.assertIn(
            errors.Error(
                "PROD",
                str(errors.BadProdVariableError)
            ),
            errors_list
        )

        self.assertIn(
            errors.Error(
                "image",
                str(errors.BadFilenameNotRecognizedError)
            ),
            errors_list,
        )

    def test_http_exception_error(self):
        """Test function that checks that the customized HTTPException
        exception behaves properly at the time of confuring the app and
        returning an expected response"""

        exception_handler = cast(
            Callable[[Request, Exception], JSONResponse],
            mock_app.exception_handlers.get(HTTPException)
        )

        self.assertTrue(exception_handler)

        exc = mock.Mock()

        exc.detail = "asd"
        exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        response = exception_handler(Request(scope={"type": "http"}), exc)

        response_body = json.loads(response.body)

        def func():
            SentMessageResponseSchema(**response_body)

        self.assertFalse(
            get_exception(
                ValidationError,
                func
            )
        )
