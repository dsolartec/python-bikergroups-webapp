from dependency_injector import providers

from app.adapters.outputs.datasources.unit_of_work import UnitOfWork
from app.adapters.outputs.libraries.encription import Encription
from app.config import Config
from app.domain.ports.abstract_container import AbstractContainer


class Container(AbstractContainer):
    config = providers.Singleton(Config)
    unit_of_work = providers.Singleton(
        UnitOfWork,
        postgresql_connection_uri=config().postgresql_connection_uri,
    )

    # Libraries
    encription = providers.Factory(Encription)
