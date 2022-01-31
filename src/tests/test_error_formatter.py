"""Module that contains the the tests for the ErrorFormatter class"""

import unittest
from typing import Optional

import pydantic

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel, ValidationError, StrictBool

from src.utils.errors import ErrorFormatter, Error, DELIMITER


# pylint: disable-next=too-few-public-methods
class Whatever(BaseModel):
    """Schema class for testing purposes"""

    age: int
    strict_bool: Optional[StrictBool] = None


class TestErrorFormatter(unittest.TestCase):
    """Test class for ErrorFormatter"""

    def test_format_list(self):
        """Function that tests ErrorFormatter.format_list class method"""

        test_str = ErrorFormatter.format_list(
            [
                Error("asd", "dsa"),
                Error("asd1", "dsa2"),
            ]
        )

        self.assertEqual(test_str, f"In asd: dsa{DELIMITER}In asd1: dsa2")

        test_str = ErrorFormatter.format_list(
            [
                Error("asd", "dsa"),
            ]
        )

        self.assertEqual(test_str, "In asd: dsa")

        test_str = ErrorFormatter.format_list(
            [
                Error("asd", "dsa"),
                Error("asd1", "dsa2"),
                Error("('asd3',)", "dsa4"),
            ]
        )

        self.assertEqual(
            test_str,
            f"\
In asd: dsa{DELIMITER}In asd1: dsa2{DELIMITER}In ('asd3',): dsa4",
        )

    def test_format_list_from_pydantic_errors(self):
        """Function that tests
        ErrorFormatter.format_list_from_pydantic_errors class method"""

        testing_exc = None

        try:
            Whatever(age="asd")

        except ValidationError as exception:
            testing_exc = exception

        test_str = ErrorFormatter.format_list_from_pydantic_errors(
            testing_exc.errors()
        )

        # pylint: disable=c-extension-no-member

        self.assertEqual(
            test_str, f"In ('age',): {str(pydantic.errors.IntegerError())}"
        )

        try:
            Whatever(age="asd", strict_bool="True")

        except ValidationError as exception:
            testing_exc = exception

        test_str = ErrorFormatter.format_list_from_pydantic_errors(
            testing_exc.errors()
        )

        self.assertEqual(
            test_str,
            f"\
In ('age',): {str(pydantic.errors.IntegerError())}{DELIMITER}\
In ('strict_bool',): {str(pydantic.errors.StrictBoolError())}",
        )
