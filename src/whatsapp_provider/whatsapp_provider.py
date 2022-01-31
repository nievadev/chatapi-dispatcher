"""Module that contains the WhatsappProvider class

The WhatsappProvider class is a class that inherits from an abstract
base class Provider whose instance sends a request to the Chat API
provider basing from a MessageDTO instance
"""

from typing import NewType, Dict, Type, cast, Tuple
from urllib.parse import unquote

import httpx

# pylint: disable-next=no-name-in-module
from pydantic import BaseModel

from src.utils.type_aliases import JsonDict
from src.schemas.message_dto import MessageDTO
from src.utils.provider import Provider
from src.utils.logger import logger
from src.utils import errors
from .chat_api_request_schemas import (
    SendFileSchema, SendMessageSchema, SendAudioSchema
)


Action = NewType("Action", str)

SEND_MESSAGE = Action("sendMessage")
SEND_FILE = Action("sendFile")
SEND_AUDIO = Action("sendPTT")


ERROR_CONTACT_DEVELOPERS = "\
Error! Details in the microservice's logs. Must fix"


def get_schema_name(schema: Type[BaseModel]) -> str:
    """Helper function that gets the name of a schema
    from a schema class"""

    return cast(str, schema.schema()["title"])


SCHEMA_ACTION_MAP: Dict[str, Action] = {
    get_schema_name(SendFileSchema): SEND_FILE,
    get_schema_name(SendMessageSchema): SEND_MESSAGE,
    get_schema_name(SendAudioSchema): SEND_AUDIO,
}


def get_action_from_schema(schema: Type[BaseModel]) -> Action:
    """Helper function that gets an action basing on the
    schema class passed in"""

    return SCHEMA_ACTION_MAP[get_schema_name(schema)]


def get_chat_api_schema(message: MessageDTO) -> BaseModel:
    """Helper function that gets a Chat API proper schema
    basing on a MessageDTO schema instance"""

    media_source = (
        message.image or
        message.video or
        message.document
    )

    if media_source:
        return SendFileSchema(
            phone=message.phone,
            body=media_source,
            filename=message.filename,
        )

    if message.text:
        return SendMessageSchema(phone=message.phone, body=message.text)

    return SendAudioSchema(phone=message.phone, audio=message.audio)


def shorten_values(
    dict_data: JsonDict,
    values: Tuple[str, ...],
    no_chars: int = 25
):
    """Function that shortens the values of the keys put in the
    'values' tuple only if they are there in the first place, if so,
    they are shorten to 'no_chars' (default: 25). It mutates the passed dict
    and returns it"""

    for msg_body in values:
        if dict_data.get(msg_body) is None:
            continue

        if len(dict_data[msg_body]) <= no_chars:
            continue

        dict_data[msg_body] = f"{dict_data[msg_body][:no_chars]}[...]"

    return dict_data


# pylint: disable-next=too-few-public-methods
class WhatsappProvider(Provider):
    """Class that acts as a provider that represents Chat API"""

    def __init__(self, api_url: str):
        # Exception is thrown if not unquoted
        self.api_url = unquote(api_url, "utf-8")

    def _make_url(self, action: Action, instance: str, token: str) -> str:
        url = f"{self.api_url}/{instance}/{action}?token={token}"

        return url

    async def send(self, msg: MessageDTO) -> JsonDict:
        """Class method that sends a POST request to Chat API
        basing from a MessageDTO schema instance"""

        schema = get_chat_api_schema(msg)

        action = get_action_from_schema(type(schema))

        url = self._make_url(action, msg.instance, msg.token)

        json_data = schema.dict()

        logger.info(
            "sending message: %s",
            shorten_values({**json_data}, ("body", "audio"))
        )

        async with httpx.AsyncClient() as client:
            try:
                response = (await client.post(url=url, json=json_data)).json()

            except httpx.ConnectTimeout as exception:
                raise errors.ConnectionTimeoutError from exception

        logger.info(
            "response got from Chat API: %s",
            response
        )

        schema_compliant_data = {
            "success": response.get("sent", False),
            "errorMessage": response.get("error") or response.get("message"),
            "id": response.get("id")
        }

        if schema_compliant_data["success"]:
            schema_compliant_data["errorMessage"] = None

        if (
            not schema_compliant_data["success"]
            and not schema_compliant_data["errorMessage"]
        ):
            logger.error(
                """\
'success' in response is {schema_compliant_data['success']} and 'errorMessage'\
 in response is {schema_compliant_data['errorMessage']}.
Data in response: {response}.
Contact the developers!\
"""
            )

            schema_compliant_data["errorMessage"] = ERROR_CONTACT_DEVELOPERS

        logger.info(
            "final response from dispatcher before schema validation: %s",
            schema_compliant_data
        )

        return schema_compliant_data
