from pydantic import BaseModel

from app.domain.enums.permission_enum import PermissionEnum


class PermissionModel(BaseModel):
    id: str
    name: PermissionEnum
