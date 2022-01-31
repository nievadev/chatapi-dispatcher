"""Module that contains the api /v1 router and configures it"""

from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse

from src.whatsapp_provider import provider as whatsapp_provider
from src.schemas.message_dto import MessageDTO
from src.schemas.dispatcher_responses import SentMessageResponseSchema
from src.utils.logger import logger
from . import examples


api = APIRouter(prefix="/v1", tags=["api_v1"])


@api.post("/messages")
async def messages(
    message: MessageDTO = Body(..., examples=examples.examples_message_dto)
) -> JSONResponse:
    """Endpoint function that handles POST requests to /messages validating
    each one's parameters with the MessageDTO schema class"""

    response = await whatsapp_provider.send(message)

    SentMessageResponseSchema(**response)

    # I prefer to use [] to access the value because
    # this way I know immediately something is wrong
    status_code = (
        status.HTTP_422_UNPROCESSABLE_ENTITY
        if not response["success"]
        else status.HTTP_200_OK
    )

    json_response = JSONResponse(response, status_code)

    logger.info(
        "final response from dispatcher: %s",
        {"content": response, "status_code": status_code}
    )

    return json_response
