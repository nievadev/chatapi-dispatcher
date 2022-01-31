"""Module that contains the schemas that represent the
responses of the dispatcher"""

from typing import Optional

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel, StrictStr, validator

from src.utils.errors import BadStatusValueError


# pylint: disable-next=too-few-public-methods
class SentMessageResponseSchema(BaseModel):
    """Schema class of the response from /messages endpoint to a POST
    request

    errorMessage becomes null if there's a success
    errorMessages becomes str if there's not a success

    Cases where there is no errorMessage and no success are strange
    and should be looked up. In those cases, Chat API responded something
    unexpected
    """

    errorMessage: Optional[StrictStr] = None
    success: bool
    id: Optional[str] = None


# pylint: disable-next=too-few-public-methods
class HealthSchema(BaseModel):
    """Schema class of the response from /management/health endpoint to a
    GET request"""

    status: str

    @validator("status")
    def check_up_or_down(cls, value):
        # pylint: disable=no-self-argument
        # pylint: disable=no-self-use

        """Validator function which checks that the status field
        is one of the allowed values"""

        if value not in ("UP", "DOWN"):
            raise BadStatusValueError(status_value=value)

        return value
