from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.adapters.outputs.datasources.unit_of_work import UnitOfWork
from app.adapters.outputs.libraries.encription import Encription


class Container(DeclarativeContainer):
    unit_of_work = providers.Singleton(UnitOfWork)

    # Libraries
    encription = providers.Factory(Encription)
