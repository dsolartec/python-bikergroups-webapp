from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.models.permission_model import PermissionModel


class PermissionEntity(BaseEntity):
    __tablename__ = "permissions"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    name: Mapped[str] = mapped_column(unique=True)

    @staticmethod
    def from_model(permission: PermissionModel) -> PermissionEntity:
        return PermissionEntity(
            id=UUID(permission.id),
            name=permission.name.value,
        )

    def to_model(self) -> PermissionModel:
        return PermissionModel(
            id=str(self.id),
            name=PermissionEnum(self.name),
        )
