from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domain.enums.audit_log_action_enum import AuditLogActionEnum


class AuditLogModel(BaseModel):
    id: str | None = Field(default=None)
    actor_id: str
    action: AuditLogActionEnum
    metadata: dict[str, Any] | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
