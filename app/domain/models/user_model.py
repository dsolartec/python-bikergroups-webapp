from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.models.permission_model import PermissionModel


class UserModel(BaseModel):
    # Common properties

    id: str | None = Field(default=None)
    phone: str
    password: str | None = Field(default=None, exclude=True)

    # Profile properties

    display_name: str

    # System properties

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    # Relationships

    permissions: list[PermissionModel] = Field(default=[], exclude=True)
