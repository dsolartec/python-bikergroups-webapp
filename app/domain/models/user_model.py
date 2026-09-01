from datetime import datetime

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    # Common properties

    id: str | None
    username: str
    password: str | None = Field(exclude=True)

    # Profile properties

    display_name: str

    # System properties

    created_at: datetime | None
    updated_at: datetime | None
