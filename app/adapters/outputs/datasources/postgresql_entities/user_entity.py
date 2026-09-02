from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import String, func, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.adapters.outputs.datasources.postgresql_entities.permission_entity import PermissionEntity
from app.domain.models.user_model import UserModel


class UserEntity(BaseEntity):
    __tablename__ = "users"

    # Common columns

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str]

    # Profile columns

    display_name: Mapped[str] = mapped_column(String(100))

    # System columns

    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp,
        server_default=func.current_timestamp(),
    )

    # Relationships

    permissions: Mapped[List["PermissionEntity"]] = relationship(lazy="raise", secondary="users_permissions")

    @staticmethod
    def from_model(user: UserModel) -> UserEntity:
        args = user.model_dump(exclude_none=True)
        if user.id is not None:
            args["id"] = UUID(user.id)

        if user.password is not None:
            args["password"] = user.password

        return UserEntity(**args)

    def to_model(self) -> UserModel:
        insp = inspect(self)
        permissions_loaded = "permissions" not in insp.unloaded

        return UserModel(
            # Common columns
            id=str(self.id),
            username=self.username,
            password=self.password,

            # Profile columns
            display_name=self.display_name,

            # System columns
            created_at=self.created_at,
            updated_at=self.updated_at,

            # Relationships
            permissions=[permission.to_model() for permission in self.permissions] if permissions_loaded else [],
        )
