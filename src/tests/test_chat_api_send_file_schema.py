"""Module that contains the tests for the SendFileSchema class"""

from unittest import TestCase

from pydantic import ValidationError

from src.whatsapp_provider.chat_api_request_schemas import SendFileSchema
from src.utils import help_functions, file_examples


NUMBER = "5" * 13


class TestSendFileSchema(TestCase):
    """Test class that contains tests for SendFileSchema class"""

    def test_success(self):
        """Test function that checks that SendFileSchema doesn't throw
        an exception while being passed correct values"""

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body="\
https://www.applecoredesigns.co.uk/wp-content/uploads/2018/08/button-ok.png",
                    phone=NUMBER
                )
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body=file_examples.base64_image,
                    phone=NUMBER
                )
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="video",
                    body=file_examples.base64_video,
                    phone=NUMBER
                )
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="audio",
                    body=file_examples.base64_audio,
                    phone=NUMBER
                )
            )
        )

    def test_bad_filename(self):
        """Test function that checks that SendMessageSchema throws
        an exception while being passed a bad filename"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="",
                    body="\
https://www.applecoredesigns.co.uk/wp-content/uploads/2018/08/button-ok.png",
                    phone=NUMBER
                )
            )
        )

    def test_bad_body(self):
        """Test function that checks that SendMessageSchema throws
        an exception while being passed a bad body"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body="https/www.applecoredesigns.co.uk/wp-c",
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body=f"{file_examples.base64_image}111",
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body="",
                    phone=NUMBER
                )
            )
        )

    def test_bad_phone(self):
        """Test function that checks that SendMessageSchema throws
        an exception while being passed a bad phone value"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body=file_examples.base64_image,
                    phone="s"
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body=file_examples.base64_image,
                    phone=""
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendFileSchema(
                    filename="image",
                    body=file_examples.base64_image,
                    phone="1"
                )
            )
        )
