"""Module that contains the Provider abstract base class"""

from abc import ABC, abstractmethod

from src.utils.type_aliases import JsonDict
from src.schemas.message_dto import MessageDTO


# This is an abstract base class, the dispatcher only uses a send method
# of whatever provider there is, and that's what it should only know!
# Every provider must inherit from this interface
# pylint: disable-next=too-few-public-methods
class Provider(ABC):
    """Abstract base class that tells Provider children
    what methods there must be in them"""

    @abstractmethod
    async def send(self, msg: MessageDTO) -> JsonDict:
        """Class method that makes a POST request to whatever service
        the provider is implemented for"""
