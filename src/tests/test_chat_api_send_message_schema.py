"""Module that contains the tests for the SendMessageSchema class"""

from unittest import TestCase

from pydantic import ValidationError

from src.whatsapp_provider.chat_api_request_schemas import SendMessageSchema
from src.utils import help_functions


NUMBER = "5" * 13


class TestSendMessageSchema(TestCase):
    """Test class that contains tests for SendMessageSchema class"""

    def test_success(self):
        """Test function that checks that SendMessageSchema doesn't throw
        an exception while being passed correct values"""

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendMessageSchema(body="asd", phone=NUMBER)
            )
        )

    def test_bad_body(self):
        """Test function that checks that SendMessageSchema throws
        an exception while being passed a bad body"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendMessageSchema(body="", phone=NUMBER)
            )
        )

    def test_bad_phone(self):
        """Test function that checks that SendMessageSchema throws
        an exception while being passed a bad phone"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendMessageSchema(body="asd", phone="asd")
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendMessageSchema(body="asd", phone="")
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendMessageSchema(body="asd", phone="1")
            )
        )
