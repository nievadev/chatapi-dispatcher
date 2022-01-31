"""Module that contains tests for main entry point of program"""

import unittest
from unittest import mock

from src.main import setup_eureka
from src.schemas.env import EnvSchema, prod_template, dev_template


class TestMain(unittest.TestCase):
    """Test class for main entry point of program"""

    @staticmethod
    def test_setup_eureka():
        """Function that checks if main.setup_eureka calls
        eureka.setup properly basing on the mocked env variables
        passed in"""

        with mock.patch("src.eureka.setup") as eureka_setup:
            setup_eureka(EnvSchema(**prod_template))

            eureka_setup.assert_called_once()

        with mock.patch("src.eureka.setup") as eureka_setup:
            setup_eureka(EnvSchema(**dev_template))

            eureka_setup.assert_not_called()
