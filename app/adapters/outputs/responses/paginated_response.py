from typing import Any

from pydantic import BaseModel, ConfigDict


class PaginatedResponse[T](BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    data: list[T]
    max_pages: int
    total_count: int
