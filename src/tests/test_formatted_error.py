"""Module that contains the tests for FormattedError class"""

import unittest
from typing import NoReturn

from src.utils import errors
from src.utils import help_functions


# pylint: disable-next=missing-class-docstring
class ExampleError(errors.FormattedError):
    msg_template = "Hello {world}"


# pylint: disable-next=missing-class-docstring
class ExampleError2(errors.FormattedError):
    msg_template = "Hello {world}, you are {age} years old"


class TestFormattedError(unittest.TestCase):
    """Test class that contains tests for the FormattedError class"""

    def test_formats_error(self):
        """Test function that checks that the children of FormattedError
        class which behave as exceptions format properly based on the kwargs"""

        self.assertEqual(str(ExampleError(world="martin")), "Hello martin")

        self.assertEqual(
            str(ExampleError2(world="martin", age=18)),
            "Hello martin, you are 18 years old",
        )

    def test_error_raises_properly(self):
        """Test function that checks that the children of FormattedError
        class, which behave as exceptions, raise, get catched
        and get formatted properly"""

        def _() -> NoReturn:
            raise ExampleError(world="world")

        exc = help_functions.get_exception(ExampleError, _)

        self.assertTrue(exc)
        self.assertEqual(str(exc), "Hello world")
