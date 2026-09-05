from abc import ABC, abstractmethod

from app.domain.models.audit_log_model import AuditLogModel


class AuditLogRepository(ABC):
    @abstractmethod
    def save(self, audit_log: AuditLogModel) -> AuditLogModel | None:
        raise NotImplementedError
