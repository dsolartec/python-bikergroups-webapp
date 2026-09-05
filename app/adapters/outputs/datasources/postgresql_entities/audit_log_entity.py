from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.models.audit_log_model import AuditLogModel


class AuditLogEntity(BaseEntity):
    __tablename__ = "audits_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    action_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.current_timestamp())

    @staticmethod
    def from_model(audit_log: AuditLogModel) -> AuditLogEntity:
        args = audit_log.model_dump(exclude=["action", "metadata"], exclude_none=True)
        if audit_log.id is not None:
            args["id"] = UUID(audit_log.id)

        if audit_log.actor_id is not None:
            args["actor_id"] = UUID(audit_log.actor_id)

        return AuditLogEntity(
            action=audit_log.action.value,
            action_metadata=audit_log.metadata,
            **args,
        )

    def to_model(self) -> AuditLogModel:
        return AuditLogModel(
            id=str(self.id),
            actor_id=str(self.actor_id),
            action=AuditLogActionEnum(self.action),
            metadata=self.action_metadata,
            created_at=self.created_at,
        )
