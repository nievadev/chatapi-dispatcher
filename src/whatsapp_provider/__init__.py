"""Module that contains the provider constructed from WhatsappProvider"""

from src.env_variables import env_variables
from .whatsapp_provider import WhatsappProvider


provider = WhatsappProvider(api_url=env_variables.API_URL)
