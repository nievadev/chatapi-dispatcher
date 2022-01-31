"""Module that contains utils to connect to eureka servers"""

from py_eureka_client.eureka_client import EurekaClient
from py_eureka_client import eureka_client

from src.schemas.env import EnvSchema


def get_eureka_kwargs(env_variables: EnvSchema):
    """Function that elaborates kwargs for eureka init function
    basing from an EnvSchema class instance"""

    return {
        "eureka_protocol": "http",
        "app_name": "chat api dispatcher",
        "eureka_server": env_variables.EUREKA_SERVER,
        "eureka_basic_auth_user": env_variables.EUREKA_AUTH_USER,
        "eureka_basic_auth_password": env_variables.EUREKA_AUTH_PASSWORD,
        "eureka_context": env_variables.EUREKA_CONTEXT,
        "instance_port": env_variables.INSTANCE_PORT,
        "instance_id": env_variables.INSTANCE_ID
    }


def setup(env_variables: EnvSchema) -> EurekaClient:
    """Function that sets up the connection to the eureka server"""

    eureka_client.init(**get_eureka_kwargs(env_variables))
