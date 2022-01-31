"""Entry point for the program that sets the whole thing up"""

from fastapi import FastAPI

from src import eureka
from src.apiv1 import api, exception_handlers
from src.devutils import devutils
from src.env_variables import env_variables
from src.schemas.env import EnvSchema


def setup_eureka(env_variables_instance: EnvSchema):
    """Function that sets up eureka basing on the env_variables"""

    if env_variables_instance.PROD:
        eureka.setup(env_variables_instance)


setup_eureka(env_variables)

app = FastAPI(
    title="Beplic Python Core",
    description="\
Python integration with ChatAPI and Beplic Core, developed and being\
maintained by Facundo Padilla and Martin Nieva\
",
    version="Version 0.1",
)

exception_handlers.configure(app)

app.include_router(api)
app.include_router(devutils)
