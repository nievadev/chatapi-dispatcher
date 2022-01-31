"""Module that contains a correctly parsed and validated object
of environment variables

Usage:
    from env_variables import env_variables

    if env_variables.PROD:
        # Code here

        pass
"""

import os
from pathlib import Path
from typing import Mapping

import dotenv
from pydantic import ValidationError

from src.schemas.env import EnvSchema


dotenv.load_dotenv()

MESSAGES = {
    "MAIN_ERROR": "Error in environment variables! Possible reasons:",
    "REASON_NO_ENV_FILE":
        "* .env file is not present, therefore no values set?",
    "REASON_BAD_TYPING":
        "* types are not correct in the file? (some values might being None)",
}


def get_reasons():
    """Function that elaborates a string based on the reasons of
    why the environment variables were invalid"""

    total_string = f"{MESSAGES['MAIN_ERROR']}\n"

    reasons = []

    reasons.append(MESSAGES["REASON_BAD_TYPING"])

    dotenv_file = Path("./.env")

    if not dotenv_file.exists():
        reasons.append(MESSAGES["REASON_NO_ENV_FILE"])

    if len(reasons) > 0:
        for reason in reasons:
            total_string = f"{total_string}  {reason}\n"

    return total_string


def get_env_variables(env_dict: Mapping[str, str]):
    """Function that validates the environment variables
    got from a os.environ-like dict"""

    try:
        parsed_env_variables = EnvSchema(**env_dict)

    except ValidationError as validation_error:
        print(get_reasons())

        raise validation_error

    return parsed_env_variables


env_variables = get_env_variables(os.environ)
