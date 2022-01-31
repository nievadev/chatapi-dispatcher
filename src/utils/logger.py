"""Module that holds the logger of the program and also configures it"""

import sys
import logging
from logging import config as logging_config
from copy import copy
from typing import Optional, Callable, Dict, Any, Union, Literal
from pathlib import Path

import click

from src.env_variables import env_variables
from src.schemas.env import EnvSchema


LEVEL_NAME_COLORS: Dict[int, Callable[[str], str]] = {
    logging.DEBUG:
        lambda level_name: click.style(str(level_name), fg="cyan"),
    logging.INFO:
        lambda level_name: click.style(str(level_name), fg="green"),
    logging.WARNING:
        lambda level_name: click.style(str(level_name), fg="yellow"),
    logging.ERROR:
        lambda level_name: click.style(str(level_name), fg="red"),
    logging.CRITICAL:
        lambda level_name: click.style(
            str(level_name), fg="bright_red"
        ),
}


def color_level_name(level_name: str, level_no: int) -> str:
    """Function that takes a level name and a level number in order
    to return a colored string. It retrieves the coloring function
    from a dictionary"""

    func = LEVEL_NAME_COLORS.get(level_no, lambda msg: msg)

    return func(level_name)


class Formatter(logging.Formatter):
    """Class that is the formatter responsible for formatting
    the message from each record obtained"""

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Union[Literal['%'], Literal['{'], Literal['$']] = "%",
        use_colors: Optional[bool] = None,
    ):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)

        levelname = recordcopy.levelname
        date = recordcopy.asctime

        seperator = " " * (34 - len(levelname) - len(date))

        if self.use_colors:
            levelname = color_level_name(levelname, recordcopy.levelno)
            date = click.style(date, fg="cyan")

        recordcopy.levelname = levelname + ":" + seperator
        recordcopy.asctime = date

        return super().formatMessage(recordcopy)


def make_logger_config(env_variables_instance: EnvSchema) -> Dict[str, Any]:
    """Function that elaborates a logger config basing from the received
    EnvSchema instance, in order to turn off/on logging to files, etc"""

    handlers = ["default"]

    if env_variables_instance.PROD:
        handlers.append("file")
        level = "INFO"

    else:
        level = "DEBUG"

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": Formatter,
                "fmt": "%(asctime)s; %(levelname)s%(message)s",
            },
            "file": {
                "()": Formatter,
                "fmt": "%(asctime)s; %(levelname)s%(message)s",
                "use_colors": False,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "file": {
                "formatter": "file",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": Path("info.log"),
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 0,
            },
        },
        "loggers": {"dispatcher": {"handlers": handlers, "level": level}},
    }

    return logger_config


logging_config.dictConfig(make_logger_config(env_variables))

logger = logging.getLogger("dispatcher")
