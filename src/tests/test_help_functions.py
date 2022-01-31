"""Module that contains the tests for help_functions module"""

import unittest
from typing import NoReturn

from src.utils import help_functions


class TestHelpFunctions(unittest.IsolatedAsyncioTestCase):
    """Test class that contains the tests for help_functions module"""

    async def test_get_exception(self):
        """Test function that checks that help_function.get_exception
        throws an exception accordingly to the function passed in"""

        def _() -> NoReturn:
            raise ValueError()

        self.assertTrue(help_functions.get_exception(ValueError, _))

        def __() -> NoReturn:
            raise TypeError()

        self.assertTrue(help_functions.get_exception(TypeError, __))

    async def test_get_exception_async(self):
        """Test function that checks that help_function.get_exception_async
        throws an exception accordingly to the function passed in"""

        async def _() -> NoReturn:
            raise ValueError()

        self.assertTrue(
            await help_functions.get_exception_async(ValueError, _)
        )

        async def __() -> NoReturn:
            raise TypeError()

        self.assertTrue(
            await help_functions.get_exception_async(TypeError, __)
        )
