"""Module that contains tests for logger"""

import unittest
import logging
from logging import config
from unittest import mock
from typing import Dict, Any

import click

from src.utils import logger
from src.schemas import env


logger_mock_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": logger.Formatter,
            "fmt": "%(asctime)s; %(levelname)s%(message)s",
            "use_colors": True,
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    },
    "loggers": {"test": {"handlers": ["default"], "level": "DEBUG"}},
}


class TestLogger(unittest.TestCase):
    """Test class for logger"""

    @staticmethod
    @mock.patch("src.utils.logger.color_level_name")
    def test_color_level_name_is_called_properly(
        color_level_name: mock.MagicMock
    ):
        """Test function that checks that the
        src.utils.logger.Formatter.color_level_name is being called
        accordingly with the logger methods"""

        config.dictConfig(logger_mock_config)

        mock_logger = logging.getLogger("test")

        with mock.patch.object(mock_logger.handlers[0], "stream"):
            color_level_name.return_value = click.style("DEBUG", fg="cyan")

            mock_logger.debug("Hello!")

            color_level_name.assert_called_once()

        logger_mock_config_no_colors = {
            **logger_mock_config,
            "formatters": {
                "default": {
                    **logger_mock_config["formatters"]["default"],
                    "use_colors": False,
                }
            },
        }

        config.dictConfig(logger_mock_config_no_colors)

        with mock.patch.object(mock_logger.handlers[0], "stream"):
            mock_logger.debug("Hello!")

            # color_level_name was not called, then it's still
            # been called once
            color_level_name.assert_called_once()

    def test_color_level_name_gives_correct_color(self):
        """Test function that checks that the
        src.utils.logger.Formatter.color_level_name method is giving
        the correct colors"""

        colored_level = logger.color_level_name("DEBUG", logging.DEBUG)

        self.assertEqual(colored_level, click.style("DEBUG", fg="cyan"))

        colored_level = logger.color_level_name("INFO", logging.INFO)

        self.assertEqual(colored_level, click.style("INFO", fg="green"))

        colored_level = logger.color_level_name("WARNING", logging.WARNING)

        self.assertEqual(colored_level, click.style("WARNING", fg="yellow"))

        colored_level = logger.color_level_name(
            "CRITICAL", logging.CRITICAL
        )

        self.assertEqual(colored_level, click.style(
            "CRITICAL", fg="bright_red"
        ))

        colored_level = logger.color_level_name("ERROR", logging.ERROR)

        self.assertEqual(colored_level, click.style("ERROR", fg="red"))

    def test_make_logger_config(self):
        """Test function that checks logger.make_logger_config
        gives correct config based on the EnvSchema instance passed in
        which acts as mocked environment variables"""

        config_made = logger.make_logger_config(
            env.EnvSchema(**env.dev_template)
        )

        self.assertEqual(
            config_made["loggers"]["dispatcher"]["handlers"],
            ["default"]
        )

        self.assertEqual(
            config_made["loggers"]["dispatcher"]["level"], "DEBUG"
        )

        config_made = logger.make_logger_config(
            env.EnvSchema(**env.prod_template)
        )

        self.assertEqual(
            config_made["loggers"]["dispatcher"]["handlers"],
            ["default", "file"]
        )

        self.assertEqual(config_made["loggers"]["dispatcher"]["level"], "INFO")
