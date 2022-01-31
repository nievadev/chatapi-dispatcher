"""Module that contains the devutils router and configures it

The dev_utils API serves the purpose of providing the information required
for development operations
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.schemas.dispatcher_responses import HealthSchema


devutils = APIRouter(tags=["dev_utils"])


@devutils.get("/management/health")
async def health():
    """Endpoint function that handles GET requests to
    /management/health"""

    health_data = HealthSchema(status="UP").dict()

    return JSONResponse(health_data, status.HTTP_200_OK)
