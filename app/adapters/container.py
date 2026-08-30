from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.adapters.outputs.datasources.unit_of_work import UnitOfWork
from app.adapters.outputs.libraries.authenticator import Authenticator
from app.adapters.outputs.libraries.encription import Encription


class Container(DeclarativeContainer):
    unit_of_work = providers.Singleton(UnitOfWork)

    # Libraries
    authenticator = providers.Factory(Authenticator, "secret_key_1", "secret_key_2")
    encription = providers.Factory(Encription)
