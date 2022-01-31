"""Module that contains helper functions"""

from typing import Callable, Optional, Type, Any, Coroutine, TypeVar


TBaseException = TypeVar("TBaseException", bound=BaseException)


def get_exception(
    exc_class: Type[TBaseException], func: Callable[..., Any]
) -> Optional[TBaseException]:
    """Helper function that catches an exception at the time
    of calling a callable and returns that exception"""

    exception = None

    try:
        func()

    except exc_class as exc:
        exception = exc

    return exception


async def get_exception_async(
    exc_class: Type[TBaseException],
    func: Callable[..., Coroutine[None, None, None]]
) -> Optional[TBaseException]:
    """Helper coroutine that is the async version of get_exception"""

    exception = None

    try:
        await func()

    except exc_class as exc:
        exception = exc

    return exception
