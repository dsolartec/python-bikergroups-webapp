from typing import Callable

from app.domain.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.domain.ports.libraries.abstract_authenticator import AbstractAuthenticator
from app.domain.ports.libraries.abstract_encription import AbstractEncription


class AbstractContainer:
    unit_of_work: Callable[[], AbstractUnitOfWork]

    # Libraries
    authenticator: Callable[[], AbstractAuthenticator]
    encription: Callable[[], AbstractEncription]
