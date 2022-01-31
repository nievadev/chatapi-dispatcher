"""Module that contains the tests for WhatsappProvider class"""

from __future__ import annotations

import unittest
from unittest import mock

from httpx import Response, ConnectTimeout

# pylint: disable-next=no-name-in-module
from pydantic import ValidationError
from fastapi.exceptions import HTTPException

from src.whatsapp_provider import provider
from src.schemas import message_dto
from src.schemas.dispatcher_responses import SentMessageResponseSchema
from src.utils.type_aliases import JsonDict
from src.utils import help_functions
from src.utils import errors
from src.whatsapp_provider.whatsapp_provider import ERROR_CONTACT_DEVELOPERS


async def response_test(
    self: TestWhatsappProvider,
    message_dto_body: JsonDict,
    must_be_response: JsonDict,
):
    """Helper function that gets a json-like dict of the data to send
    to the provider, and a json-like dict of the data that is expected
    to be responded. Based on that, it checks that the provider is responding
    as expected"""

    def func():
        SentMessageResponseSchema(**must_be_response)

    response = await provider.send(message_dto.MessageDTO(**message_dto_body))

    self.assertFalse(
        help_functions.get_exception(
            ValidationError,
            func
        )
    )

    self.assertEqual(response, must_be_response)


class TestWhatsappProvider(unittest.IsolatedAsyncioTestCase):
    """Test class that contains the tests for WhatsappProvider class"""

    @mock.patch("logging.Logger.info")
    @mock.patch("httpx.AsyncClient.post")
    async def test_send_messages(
        self,
        async_client_post: mock.MagicMock,
        logger_info: mock.MagicMock
    ):
        """Test function that checks the provider responded as expected"""

        logger_info.return_value = None

        mock_id = "false_28472921498@c.us_DF58E6AB5B433N8CCE570C40F"

        async_client_post.return_value = Response(
            status_code=200,
            json={"sent": True, "id": mock_id}
        )

        await response_test(
            self, message_dto.text_template, {
                "success": True,
                "errorMessage": None,
                "id": mock_id
            }
        )

        await response_test(
            self, message_dto.image_template, {
                "success": True,
                "errorMessage": None,
                "id": mock_id
            }
        )

        await response_test(
            self, message_dto.video_template, {
                "success": True,
                "errorMessage": None,
                "id": mock_id
            }
        )

        await response_test(
            self, message_dto.audio_template, {
                "success": True,
                "errorMessage": None,
                "id": mock_id
            }
        )

    @mock.patch("logging.Logger.info")
    @mock.patch("logging.Logger.error")
    @mock.patch("httpx.AsyncClient.post")
    async def test_chat_api_errors(
        self,
        async_client_post: mock.MagicMock,
        logger_error: mock.MagicMock,
        logger_info: mock.MagicMock
    ):
        """Test function that checks that the provider sends 422
        accordingly based on what Chat API unexpectedly responded,
        and that also checks if the logger logged it properly"""

        logger_info_times_called_per_send = 3

        async_client_post.return_value = Response(
            status_code=422, json={"error": "Error!"}
        )

        await response_test(
            self,
            message_dto.text_template,
            {"success": False, "id": None, "errorMessage": "Error!"},
        )

        self.assertEqual(
            logger_info.call_count,
            logger_info_times_called_per_send
        )

        async_client_post.return_value = Response(status_code=422, json={})

        await response_test(
            self,
            message_dto.text_template,
            {
                "success": False,
                "errorMessage": ERROR_CONTACT_DEVELOPERS,
                "id": None
            },
        )

        self.assertEqual(logger_error.call_count, 1)

        self.assertEqual(
            logger_info.call_count,
            logger_info_times_called_per_send * 2
        )

        async_client_post.return_value = Response(
            status_code=422, json={"error": ""}
        )

        await response_test(
            self,
            message_dto.text_template,
            {
                "success": False,
                "errorMessage": ERROR_CONTACT_DEVELOPERS,
                "id": None
            },
        )

        self.assertEqual(logger_error.call_count, 2)

        self.assertEqual(
            logger_info.call_count,
            logger_info_times_called_per_send * 3
        )

        async_client_post.return_value = Response(
            status_code=422, json={"error": None}
        )

        await response_test(
            self,
            message_dto.text_template,
            {
                "success": False,
                "errorMessage": ERROR_CONTACT_DEVELOPERS,
                "id": None
            },
        )

        self.assertEqual(logger_error.call_count, 3)

        self.assertEqual(
            logger_info.call_count,
            logger_info_times_called_per_send * 4
        )

    @mock.patch("logging.Logger.info")
    @mock.patch("httpx.AsyncClient.post")
    async def test_connection_timeout_raises_http(
        self,
        async_client_post: mock.MagicMock,
        logger_info: mock.MagicMock
    ):
        """Test function that checks that the provider raises an HTTPException
        in the case of httpx raising a ConnectTimeout exception"""

        def side_effect_post(*args, **kwargs):
            raise ConnectTimeout("")

        async_client_post.side_effect = side_effect_post

        async def get_exception_func():
            await provider.send(message_dto.MessageDTO(
                **message_dto.text_template
            ))

        exc = await help_functions.get_exception_async(
            HTTPException,
            get_exception_func
        )

        # 'if:' statement to silence mypy on Optional[HTTPException]
        if exc:
            self.assertEqual(exc.detail, errors.ConnectionTimeoutError.detail)
            self.assertEqual(
                exc.status_code, errors.ConnectionTimeoutError.status_code
            )
            self.assertEqual(logger_info.call_count, 1)

        # If I write 'else:' statement, pytest coverage asks for tests
        # in this module
        # In the case there is no exception, an assertion error is thrown
        self.assertTrue(exc)
