"""Module that contains the tests for the env variables module"""

from __future__ import annotations

import unittest
from unittest import mock
from pathlib import Path
from typing import Tuple, Any

from pydantic import ValidationError

from src import env_variables
from src.schemas.env import EnvSchema, dev_template, prod_template
from src.utils import help_functions
from src.utils.type_aliases import JsonDict


TRUE = str(True)
FALSE = str(False)


def attr_not_values_test(
    self: TestEnvVariables, attr: str, values: Tuple[Any], *dicts: JsonDict
):
    """Helper function that gets an attr, a tuple of values, and dictionaries,
    to test that the EnvShema class throws an error if passed each dictionary
    with an attr set to each of those values in the tuple"""

    for bad_val in values:
        for dict_val in dicts:
            # create_fun was created in order to silence a justified pylint
            # warning, which in otherwise not to be silenced, there wouldn't be
            # any problem, but it's a good practice to not trust a non-pure
            # loop-redefined function

            def create_fun(dict_val, bad_val, attr):
                def _():
                    EnvSchema(**{**dict_val, attr: bad_val})

                return _

            self.assertTrue(
                help_functions.get_exception(
                    ValidationError,
                    create_fun(dict_val, bad_val, attr)
                )
            )


class TestEnvVariables(unittest.TestCase):
    """Test class that contains tests for the env variables module"""

    def test_get_env_variables(self):
        """Test function that checks that the get_env_variables function
        returns the schema instance with the proper variables passing a
        a os.environ-like object"""

        proper_environ = env_variables.get_env_variables(dev_template)

        self.assertEqual(proper_environ.PROD, dev_template["PROD"] == TRUE)
        self.assertEqual(proper_environ.API_URL, dev_template["API_URL"])
        self.assertEqual(
            proper_environ.TEST_INSTANCE,
            dev_template["TEST_INSTANCE"]
        )
        self.assertEqual(proper_environ.TEST_TOKEN, dev_template["TEST_TOKEN"])

        proper_environ = env_variables.get_env_variables(prod_template)

        self.assertEqual(proper_environ.PROD, prod_template["PROD"] == TRUE)
        self.assertEqual(proper_environ.API_URL, prod_template["API_URL"])
        self.assertEqual(
            proper_environ.TEST_INSTANCE,
            prod_template["TEST_INSTANCE"]
        )
        self.assertEqual(
            proper_environ.TEST_TOKEN,
            prod_template["TEST_TOKEN"]
        )
        self.assertEqual(
            proper_environ.EUREKA_SERVER,
            prod_template["EUREKA_SERVER"]
        )
        self.assertEqual(
            proper_environ.INSTANCE_PORT,
            prod_template["INSTANCE_PORT"]
        )

        self.assertEqual(
            proper_environ.EUREKA_AUTH_USER,
            prod_template["EUREKA_AUTH_USER"]
        )

        self.assertEqual(
            proper_environ.EUREKA_AUTH_PASSWORD,
            prod_template["EUREKA_AUTH_PASSWORD"]
        )

        self.assertEqual(
            proper_environ.EUREKA_CONTEXT,
            prod_template["EUREKA_CONTEXT"]
        )
        self.assertEqual(
            proper_environ.INSTANCE_ID,
            prod_template["INSTANCE_ID"]
        )

    @mock.patch("builtins.print")
    def test_get_env_variables_validation_error(self, builtins_print):
        """Test function that checks that an exception is thrown if
        the production variables are not there when PROD=True"""

        self.assertTrue(
            help_functions.get_exception(
                ValidationError,
                lambda: env_variables.get_env_variables({
                    **dev_template,
                    "PROD": True
                }),
            )
        )

        builtins_print.assert_called_once()

    def test_env_schema_bad_prod(self):
        """Test function that checks that an exception is thrown if the PROD
        variable equals bad values"""

        attr_not_values_test(
            self,
            "PROD",
            ("", "asd", 2),
            prod_template,
            dev_template
        )

    def test_env_schema_bad_api_url(self):
        """Test function that checks that an exception is thrown if the API_URL
        variable equals bad values"""

        attr_not_values_test(
            self, "API_URL", ("", "asd", True, 2), dev_template, prod_template
        )

    def test_env_schema_bad_instance(self):
        """Test function that checks that an exception is thrown if the
        TEST_INSTANCE variable equals bad values"""

        attr_not_values_test(
            self, "TEST_INSTANCE", ("", True, 2), dev_template, prod_template
        )

    def test_env_schema_bad_token(self):
        """Test function that checks that an exception is thrown if the
        TEST_TOKEN variable equals bad values"""

        attr_not_values_test(
            self, "TEST_TOKEN", ("", True, 2), dev_template, prod_template
        )

    def test_env_schema_bad_eureka_server(self):
        """Test function that checks that an exception is thrown if the
        EUREKA_SERVER variable equals bad values"""

        attr_not_values_test(
            self,
            "EUREKA_SERVER",
            ("", True, 2),
            prod_template
        )

    def test_env_schema_bad_instance_id(self):
        """Test function that checks that an exception is thrown if the
        INSTANCE_ID variable equals bad values"""

        attr_not_values_test(self, "INSTANCE_ID", ("", True, 2), prod_template)

    def test_env_schema_bad_instance_port(self):
        """Test function that checks that an exception is thrown if the
        INSTANCE_PORT variable equals bad values"""

        attr_not_values_test(self, "INSTANCE_PORT", ("", "asd"), prod_template)

    def test_env_schema_bad_eureka_auth_user(self):
        """Test function that checks that an exception is thrown if the
        EUREKA_AUTH_USER variable equals bad values"""

        attr_not_values_test(
            self,
            "EUREKA_AUTH_USER",
            ("", True, 2),
            prod_template
        )

    def test_env_schema_bad_eureka_auth_password(self):
        """Test function that checks that an exception is thrown if the
        EUREKA_AUTH_PASSWORD variable equals bad values"""

        attr_not_values_test(
            self,
            "EUREKA_AUTH_PASSWORD",
            ("", True, 2),
            prod_template
        )

    def test_env_schema_bad_eureka_context(self):
        """Test function that checks that an exception is thrown if the
        EUREKA_CONTEXT variable equals bad values"""

        attr_not_values_test(
            self,
            "EUREKA_CONTEXT",
            ("", True, 2),
            prod_template
        )

    def test_get_reasons(self):
        """Test function that checks that the get_reasons function returns
        the proper string basing on certain conditions like if the .env
        variable exists or not, etc"""

        with mock.patch.object(Path, "exists", return_value=True):
            message = env_variables.get_reasons()

        self.assertEqual(
            message,
            f"""\
{env_variables.MESSAGES['MAIN_ERROR']}
  {env_variables.MESSAGES['REASON_BAD_TYPING']}
""",
        )

        with mock.patch.object(Path, "exists", return_value=False):
            message = env_variables.get_reasons()

        self.assertEqual(
            message,
            f"""\
{env_variables.MESSAGES['MAIN_ERROR']}
  {env_variables.MESSAGES['REASON_BAD_TYPING']}
  {env_variables.MESSAGES['REASON_NO_ENV_FILE']}
""",
        )
