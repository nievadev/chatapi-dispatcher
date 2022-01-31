# pylint: disable=too-few-public-methods

"""Module that contains the schema classes to elaborate
requests for Chat API"""

from typing import Union

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel, HttpUrl

from src.utils.type_aliases import (
    Base64Audio, Phone, MessageBody, Filename, Base64
)


class BaseMessage(BaseModel):
    """Schema class that acts as parent for message schema classes"""

    phone: Phone


class SendMessageSchema(BaseMessage):
    """Schema class that elaborates a validated /sendMessage request"""

    body: MessageBody


class SendFileSchema(BaseMessage):
    """Schema class that elaborates a validated /sendFile request"""

    filename: Filename

    body: Union[HttpUrl, Base64]


class SendAudioSchema(BaseMessage):
    """Schema class that elaborates a validated /sendPPT request"""

    audio: Union[Base64Audio, HttpUrl]
