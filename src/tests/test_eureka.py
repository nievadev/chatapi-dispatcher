"""Module that contains the tests for eureka module"""

import unittest
from unittest import mock

from src import eureka
from src.schemas import env


class TestEureka(unittest.TestCase):
    """Test class for eureka module"""

    @staticmethod
    @mock.patch("py_eureka_client.eureka_client.init")
    def test_setup(eureka_client_init):
        """Function that tests that eureka client initializes
        properly basing on mocked env_variables"""

        env_variables = env.EnvSchema(**env.prod_template)

        eureka.setup(env_variables)

        eureka_client_init.assert_called_once_with(
            **eureka.get_eureka_kwargs(env_variables)
        )
