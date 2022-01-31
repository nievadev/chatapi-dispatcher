"""Module that contains the EnvSchema and plenty of templates for it"""

from typing import Optional, Union, NoReturn

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel, validator, HttpUrl

from src.utils.type_aliases import JsonDict, NonEmpty, Phone
from src.utils import errors


prod_template = {
    "PROD": "True",
    "API_URL": "https://asd.com",
    "TEST_INSTANCE": "asd",
    "TEST_TOKEN": "asd",
    "EUREKA_SERVER": "asd",
    "INSTANCE_PORT": 1,
    "EUREKA_AUTH_USER": "asd",
    "EUREKA_AUTH_PASSWORD": "asd",
    "EUREKA_CONTEXT": "/asd",
    "INSTANCE_ID": "asd",
    "TEST_PHONE": "5492914141794",
}

dev_template = {
    "PROD": "False",
    "API_URL": "https://asd.com",
    "TEST_INSTANCE": "asd",
    "TEST_TOKEN": "asd",
    "TEST_PHONE": "5492914141794",
}


class EnvSchema(BaseModel):
    """Schema class that is responsible for parsing an os.environ-like
    object and validating the data of it to be accessed later as Python
    typed objects"""

    TEST_TOKEN: NonEmpty
    TEST_INSTANCE: NonEmpty
    TEST_PHONE: Phone
    API_URL: HttpUrl

    INSTANCE_ID: Optional[NonEmpty] = None
    EUREKA_SERVER: Optional[NonEmpty] = None
    INSTANCE_PORT: Optional[int] = None
    EUREKA_AUTH_USER: Optional[NonEmpty] = None
    EUREKA_AUTH_PASSWORD: Optional[NonEmpty] = None
    EUREKA_CONTEXT: Optional[NonEmpty] = None

    PROD: bool

    @validator("PROD", pre=True)
    def check_prod_strict(cls, value: str) -> Union[str, NoReturn]:
        # pylint: disable=no-self-use
        # pylint: disable=no-self-argument

        """Validator function that checks that the syntax
        of the boolean of PROD value follows Python's"""

        if value not in ("True", "False"):
            raise errors.BadProdVariableError

        return value

    @validator("PROD")
    def check_eureka_variables(
        cls, value: bool, values: JsonDict
    ) -> Union[bool, NoReturn]:
        # pylint: disable=no-self-argument
        # pylint: disable=no-self-use

        """Validator function that checks that the credentials
        to make a connection to an eureka server are valid"""

        if not value:
            return value

        eureka_values = {
            "INSTANCE_ID": values.get("INSTANCE_ID"),
            "EUREKA_SERVER": values.get("EUREKA_SERVER"),
            "INSTANCE_PORT": values.get("INSTANCE_PORT"),
            "EUREKA_AUTH_USER": values.get("EUREKA_AUTH_USER"),
            "EUREKA_AUTH_PASSWORD": values.get("EUREKA_AUTH_PASSWORD"),
            "EUREKA_CONTEXT": values.get("EUREKA_CONTEXT"),
        }

        if None in tuple(eureka_values.values()):
            none_values = {k: v for k, v in eureka_values.items() if v is None}

            raise errors.BadEurekaValuesError(none_values=none_values)

        return value
