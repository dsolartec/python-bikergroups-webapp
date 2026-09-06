from dataclasses import dataclass
from typing import Generic

from app.domain.types import T


@dataclass
class BaseCommand(Generic[T]):
    pass
