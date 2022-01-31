"""Module that contains the tests for the api_v1 API"""

from __future__ import annotations

import json
from typing import Tuple
from unittest import TestCase
from unittest import mock

import pydantic
from fastapi.testclient import TestClient
from pydantic import ValidationError
from httpx import Response
from requests import models
from src.schemas import message_dto

from src.utils import (
    help_functions,
    type_aliases,
    errors
)
from src.main import app
from src.schemas.dispatcher_responses import SentMessageResponseSchema


client = TestClient(app)


def post_validate_response(
    self: TestApiV1,
    url: str,
    json_data: type_aliases.JsonDict,
    expected_status_code: int
) -> Tuple[models.Response, type_aliases.JsonDict]:
    """Helper function that takes an URL and data to make the POST request
    with, and makes a POST request to validate the response complies
    SentMessageResponseSchema class"""

    response = client.post(url, json=json_data)

    def func():
        SentMessageResponseSchema(**response.json())

    # I test that I'm receiving it as the SentMessageResponseSchema
    self.assertFalse(
        help_functions.get_exception(
            ValidationError,
            func
        )
    )

    self.assertEqual(response.status_code, expected_status_code)

    return json.loads(response.content)


class TestApiV1(TestCase):
    """Test class that contains tests for the first version of the API"""

    # This just patches httpx internally,
    # the written logic is what's only being tested out
    @mock.patch("logging.Logger.info")
    @mock.patch("httpx.AsyncClient.post")
    def test_v1_messages(
        self,
        post: mock.MagicMock,
        logger_info: mock.MagicMock
    ):
        """Test function that makes plenty of POST requests
        to the API and checks their responeses are what is expected for
        them to be"""

        logger_info.return_value = None

        post.return_value = Response(200, json={"sent": True})

        post_validate_response(
            self, "/v1/messages", message_dto.text_template, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.image_template, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.video_template, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.audio_template, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.video_template_base64, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.image_template_base64, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.audio_template_base64, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.document_template_base64_odt, 200
        )

        post_validate_response(
            self,
            "/v1/messages",
            message_dto.document_template_base64_docx,
            200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.document_template_base64_pdf, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.document_template_docx, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.document_template_pdf, 200
        )

        post_validate_response(
            self, "/v1/messages", message_dto.document_template_odt, 200
        )

    def test_v1_messages_bad_phone(self):
        # pylint: disable=c-extension-no-member

        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad phone value
        in the POST parameters"""

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.text_template, "phone": "asd"},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'phone')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.Phone.min_length
                            )
                        ),
                    )
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.text_template, "phone": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'phone')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.Phone.min_length
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.text_template,
                "phone": "d" * type_aliases.Phone.min_length
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'phone')",
                        str(
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Phone.regex.pattern
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.text_template,
                "phone": "1" * 14
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'phone')",
                        str(pydantic.errors.AnyStrMaxLengthError(
                            limit_value=type_aliases.Phone.max_length
                        )),
                    ),
                ]
            ),
        )

    def test_v1_messages_bad_text(self):
        # pylint: disable=c-extension-no-member

        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad text value
        in the POST parameters"""

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.text_template, "text": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'text')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.MessageBody.min_length
                            )
                        ),
                    )
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.text_template, "text": "d" * 20001},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'text')",
                        str(
                            pydantic.errors.AnyStrMaxLengthError(
                                limit_value=type_aliases.MessageBody.max_length
                            )
                        ),
                    )
                ]
            ),
        )

    def test_v1_messages_bad_image(self):
        # pylint: disable=c-extension-no-member

        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad image value
        in the POST parameters"""

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.image_template, "image": "https://s"},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'image')",
                        str(
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Image.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'image')",
                        str(pydantic.errors.UrlHostTldError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.image_template, "image": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'image')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.Base64Image.min_length
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'image')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.min_length
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.image_template_base64,
                "image": "asdasdasdasd"
            },
            422
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.image_template,
                "image": "d" * 2084,
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'image')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Image.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'image')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            # pylint: disable=no-member
                            limit_value=pydantic.HttpUrl.max_length
                        ))
                    ),
                ]
            ),
        )

    def test_v1_messages_bad_video(self):
        # pylint: disable=c-extension-no-member

        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad video value
        in the POST parameters"""

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.video_template, "video": "http://techslides."},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'video')",
                        str(
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Video.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'video')",
                        str(pydantic.errors.UrlHostTldError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.video_template, "video": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'video')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.Base64Video.min_length
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'video')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.min_length
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.video_template_base64,
                "video": "asdasdasdasd",
            },
            422
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.video_template,
                "video": "d" * 2084,
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'video')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Video.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'video')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            # pylint: disable=no-member
                            limit_value=pydantic.HttpUrl.max_length
                        ))
                    ),
                ]
            ),
        )

    def test_v1_messages_bad_audio(self):
        # pylint: disable=c-extension-no-member

        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad audio value
        in the POST parameters"""

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.audio_template, "audio": "https://"},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'audio')",
                        str(
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Audio.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'audio')",
                        str(pydantic.errors.UrlHostError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.audio_template, "audio": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'audio')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=type_aliases.Base64Audio.min_length
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'audio')",
                        str(
                            pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.min_length
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.audio_template_base64,
                "audio": "asdasdasdasd",
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'audio')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Audio.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'audio')",
                        str(pydantic.errors.UrlSchemeError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.audio_template,
                "audio": "d" * 2084,
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'audio')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=type_aliases.Base64Audio.regex.pattern
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'audio')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            # pylint: disable=no-member
                            limit_value=pydantic.HttpUrl.max_length
                        ))
                    ),
                ]
            ),
        )

    def test_v1_messages_bad_document(self):
        """Test function that checks that a 422 is returned
        at the time of sending a bad request with a bad document value
        in the POST parameters"""

        pattern_base64 = type_aliases.Base64Document.regex.pattern
        min_length_base64 = type_aliases.Base64Document.min_length

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.document_template_docx,
                "document": "http://techslides."
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'document')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=pattern_base64
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'document')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.UrlHostTldError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {**message_dto.document_template_docx, "document": ""},
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'document')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.AnyStrMinLengthError(
                                limit_value=min_length_base64
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'document')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.AnyStrMinLengthError(
                                # pylint: disable-next=no-member
                                limit_value=pydantic.HttpUrl.min_length
                            )
                        ),
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.document_template_base64_docx,
                "document": "asd12fdasdasd",
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'document')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=pattern_base64
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'document')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.UrlSchemeError())
                    ),
                ]
            ),
        )

        content = post_validate_response(
            self,
            "/v1/messages",
            {
                **message_dto.document_template_base64_docx,
                "document": "d" * 2084,
            },
            422
        )

        self.assertEqual(
            content["errorMessage"],
            errors.ErrorFormatter.format_list(
                [
                    errors.Error(
                        "('body', 'document')",
                        str(
                            # pylint: disable=c-extension-no-member
                            pydantic.errors.StrRegexError(
                                pattern=pattern_base64
                            )
                        ),
                    ),
                    errors.Error(
                        "('body', 'document')",
                        # pylint: disable=c-extension-no-member
                        str(pydantic.errors.AnyStrMaxLengthError(
                            # pylint: disable=no-member
                            limit_value=pydantic.HttpUrl.max_length
                        ))
                    ),
                ]
            ),
        )
