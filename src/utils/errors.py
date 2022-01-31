"""Module that contains exceptions to be raised and error-utility classes"""

import re
from typing import Iterable, Any, List
from dataclasses import dataclass

from fastapi import status
from fastapi.exceptions import HTTPException

from src.utils.type_aliases import JsonDict


DELIMITER = ",,, "

ERROR_REG = r"In ((\w+)|(\(\'\w+\'(\,+\s\'\w+\')*\))):\s(.*)"


class FormattedError(ValueError):
    """Class that lets you create a templated error that can be formatted
    at the time of being raised"""

    msg_template: str

    def __init__(self, **kwargs: Any):
        super().__init__()

        self.__dict__ = kwargs

    def __str__(self) -> str:
        return self.msg_template.format(**self.__dict__)


# pylint: disable-next=missing-class-docstring
class BadEurekaValuesError(FormattedError):
    msg_template = "Eureka values are not valid. {none_values}"


# pylint: disable-next=missing-class-docstring
class BadStatusValueError(FormattedError):
    msg_template = "Status value is not valid. status='{status_value}'"


# pylint: disable-next=missing-class-docstring
class BadMatchInvalidLocError(FormattedError):
    msg_template = "{error_str} does not match regex {ERROR_REG}"


# pylint: disable-next=missing-class-docstring
class OnlyOneOfThemError(FormattedError):
    msg_template = "\
Only ONE of these values {only_one} must be properly set, got: {values}"


# pylint: disable-next=missing-class-docstring
class AtLeastOneOfThemError(FormattedError):
    msg_template = "\
At least ONE of these values {at_least} must be properly set, got: {values}"


BadProdVariableError = ValueError(
    "PROD variable can only be either 'True' or 'False'"
)

BadFilenameNotRecognizedError = ValueError(
    "Filename extracted from base-64/http URL asset not recognized"
)

ConnectionTimeoutError = HTTPException(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="\
Tried to make POST request to Chat API, but received a connection time out",
)


@dataclass(frozen=True)
class Error:
    """Dataclass to represent what I need from a pydantic error"""

    loc: str
    msg: str


class ErrorFormatter:
    """Class whose methods format a list of different errors into a string"""

    @classmethod
    def format_list(cls, list_errors: Iterable[Error]) -> str:
        """Class method that formats a Iterable[Error] into a string"""

        new_list = [f"In {error.loc}: {error.msg}" for error in list_errors]

        return DELIMITER.join(new_list)

    @classmethod
    def format_list_from_pydantic_errors(cls, list_errors: Iterable[JsonDict]):
        """Class method that formats a Iterable[JsonDict] into a string

        The Iterable[JsonDict] must be a list of pydantic given errors"""

        new_list = [
            Error(pydantic_error["loc"], pydantic_error["msg"])
            for pydantic_error in list_errors
        ]

        return cls.format_list(new_list)


# pylint: disable-next=too-few-public-methods
class ErrorParser:
    """Class whose methods parse a string in shape of a list of different
    errors into a list"""

    @classmethod
    def parse_list(cls, list_: str) -> List[Error]:
        """Class method that parses a string that represents an Iterable[Error]
        into a List[Error] object"""

        new_list = []

        for error_str in list_.split(DELIMITER):
            match = re.match(ERROR_REG, error_str)

            if not match:
                raise BadMatchInvalidLocError(
                    error_str=error_str,
                    ERROR_REG=ERROR_REG
                )

            new_list.append(
                Error(match.group(2) or match.group(3), match.group(5))
            )

        return new_list
