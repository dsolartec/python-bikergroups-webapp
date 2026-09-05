from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.domain.models.user_permission_model import UserPermissionModel


class UserPermissionEntity(BaseEntity):
    __tablename__ = "users_permissions"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    @staticmethod
    def from_model(user_permission: UserPermissionModel) -> UserPermissionEntity:
        args: dict[str, any] = {
            "permission_id": UUID(user_permission.permission_id),
            "user_id": UUID(user_permission.user_id),
        }

        if user_permission.id is not None:
            args["id"] = UUID(user_permission.id)

        return UserPermissionEntity(**args)

    def to_model(self) -> UserPermissionModel:
        return UserPermissionModel(
            id=str(self.id),
            permission_id=str(self.permission_id),
            user_id=str(self.user_id),
        )
