"""Module that contains the tests for the SendAudioSchema class"""

from unittest import TestCase

from pydantic import ValidationError

from src.whatsapp_provider.chat_api_request_schemas import SendAudioSchema
from src.utils import help_functions, file_examples


NUMBER = "5" * 13


class TestSendAudioSchema(TestCase):
    """Test class that contains tests for SendAudioSchema class"""

    def test_success(self):
        """Test function that checks that several examples work as expected"""

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio="\
    https://filesamples.com/samples/audio/opus/Symphony%20No.6%20(1st%20movement).opus\
    ",
                    phone=NUMBER
                )
            )
        )

        self.assertFalse(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_audio,
                    phone=NUMBER
                )
            )
        )

    def test_bad_audio(self):
        """Test function that checks that the class throws an exception
        at the time of being passed a bad audio value"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=f"{file_examples.base64_audio}111",
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio="",
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio="\
    httpslesamples.com/samples/audio/opus/Symphony%20No.6%20(1smovement).opus",
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_image,
                    phone=NUMBER
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_video,
                    phone=NUMBER
                )
            )
        )

    def test_bad_phone(self):
        """Test function that checks that the class throws an exception
        at the time of being passed a bad phone value"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_audio,
                    phone=""
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_audio,
                    phone="sss"
                )
            )
        )

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: SendAudioSchema(
                    audio=file_examples.base64_audio,
                    phone="1"
                )
            )
        )
