from typing import Callable

from app.config import Config
from app.domain.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.domain.ports.libraries.abstract_encription import AbstractEncription


class AbstractContainer:
    config: Callable[[], Config]
    unit_of_work: Callable[[], AbstractUnitOfWork]

    # Libraries
    encription: Callable[[], AbstractEncription]
