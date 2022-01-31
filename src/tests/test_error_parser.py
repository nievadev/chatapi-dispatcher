"""Module that contains the tests for ErrorParser class"""

from __future__ import annotations

import unittest

from src.utils import errors
from src.utils import help_functions


def assert_exception_when_lists_str(self: TestErrorParser, *args: str):
    """Helper function that gets the args to put each into
    ErrorParser.parse_list to check that it throws an exception"""

    for list_str in args:
        # create_fun was created in order to silence a justified pylint
        # warning, which in otherwise not to be silenced, there wouldn't be
        # any problem, but it's a good practice to not trust a non-pure
        # loop-redefined function

        def create_fun(list_str):
            def _():
                errors.ErrorParser.parse_list(list_str)

            return _

        self.assertTrue(
            help_functions.get_exception(
                errors.BadMatchInvalidLocError,
                create_fun(list_str)
            )
        )


class TestErrorParser(unittest.TestCase):
    """Test class that contains tests for ErrorParser class"""

    def test_parse_list(self):
        """Test function that checks that parse_list function
        parses a string list properly"""

        list_str = "In body: hello!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual([errors.Error("body", "hello!")], list_parsed)

        list_str = "In ('body'): hello!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual([errors.Error("('body')", "hello!")], list_parsed)

        list_str = "In ('body', 'image'): hello!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual(
            [
                errors.Error(
                    "('body', 'image')",
                    "hello!"
                )
            ],
            list_parsed
        )

        list_str = "In ('body', 'image', 'another'): hello!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual(
            [
                errors.Error("('body', 'image', 'another')", "hello!")
            ],
            list_parsed
        )

        list_str = f"\
In ('body', 'image', 'another'): hello!{errors.DELIMITER}\
In ('image', 'another'): another message!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual(
            [
                errors.Error("('body', 'image', 'another')", "hello!"),
                errors.Error("('image', 'another')", "another message!"),
            ],
            list_parsed,
        )

        list_str = f"\
In ('body', 'image', 'another'): hello!{errors.DELIMITER}\
In another: another message!"

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual(
            [
                errors.Error("('body', 'image', 'another')", "hello!"),
                errors.Error("another", "another message!"),
            ],
            list_parsed,
        )

        list_str = f"""\
In image: hello!{errors.DELIMITER}\
In ('image', 'another'): another message!{errors.DELIMITER}\
In ('image', 'test'): blaaa\
"""

        list_parsed = errors.ErrorParser.parse_list(list_str)

        self.assertEqual(
            [
                errors.Error("image", "hello!"),
                errors.Error("('image', 'another')", "another message!"),
                errors.Error("('image', 'test')", "blaaa"),
            ],
            list_parsed,
        )

    def test_parses_bad_list(self):
        """Test function that checks that parse_list function
        throws an exception when given a bad string"""

        assert_exception_when_lists_str(
            self,
            "In ('body', 'image', ): hello!",
            "In ('body', 'image', '):",
            "In ('body',): asd",
            "In image:",
            "In (): asd",
            "In ('body', ''): asd",
            "In ('body', 1d): asd",
            f"In image: asd{errors.DELIMITER}In another:",
        )
