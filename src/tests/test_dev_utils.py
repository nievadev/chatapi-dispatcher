"""Module that contains the tests for the dev_utils API"""

import unittest
import json

from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.main import app
from src.schemas.dispatcher_responses import HealthSchema
from src.utils.help_functions import get_exception


client = TestClient(app)


class TestDevUtils(unittest.TestCase):
    """Test class that contains tests for the dev_utils API"""

    def test_management_health(self):
        # pylint: disable=unnecessary-lambda

        """Test function that checks that the response provided by
        /management/health works as expected and complies HealthSchema class"""

        response = client.get("/management/health")

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["status"], "UP")

        self.assertIs(
            get_exception(ValidationError, lambda: HealthSchema(**content)),
            None
        )
