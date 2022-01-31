"""Module that contains the tests for dispatcher_responses module"""

import unittest

from pydantic import ValidationError

from src.utils.help_functions import get_exception
from src.utils.errors import BadStatusValueError, ErrorFormatter, Error
from src.schemas.dispatcher_responses import HealthSchema


class TestHealthSchema(unittest.TestCase):
    """Test class that contains tests for HealthSchema class"""

    def test_status(self):
        """Test function that checks that the status field validator
        works as expected"""

        self.assertIs(
            get_exception(ValidationError, lambda: HealthSchema(status="UP")),
            None
        )

        self.assertIs(
            get_exception(
                ValidationError,
                lambda: HealthSchema(status="DOWN")
            ),
            None
        )

        exc = get_exception(ValidationError, lambda: HealthSchema(status=""))

        self.assertTrue(exc)
        self.assertEqual(
            ErrorFormatter.format_list_from_pydantic_errors(exc.errors()),
            ErrorFormatter.format_list(
                (
                    Error("('status',)", BadStatusValueError(status_value="")),
                )
            )
        )

        exc = get_exception(
            ValidationError,
            lambda: HealthSchema(status="asd")
        )

        self.assertTrue(exc)
        self.assertEqual(
            ErrorFormatter.format_list_from_pydantic_errors(exc.errors()),
            ErrorFormatter.format_list(
                (
                    Error(
                        "('status',)",
                        BadStatusValueError(status_value="asd")
                    ),
                )
            )
        )
