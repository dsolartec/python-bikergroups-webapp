from sqlalchemy.orm import Session

from app.adapters.outputs.datasources.postgresql_entities.audit_log_entity import AuditLogEntity
from app.domain.models.audit_log_model import AuditLogModel
from app.domain.ports.repositories.audit_log_repository import AuditLogRepository


class PostgreSQLAuditLogRepository(AuditLogRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def save(self, audit_log: AuditLogModel) -> AuditLogModel | None:
        try:
            audit_log_entity = AuditLogEntity.from_model(audit_log)

            self._session.add(audit_log_entity)
            self._session.commit()
            self._session.refresh(audit_log_entity)

            return audit_log_entity.to_model()
        except:
            return None
