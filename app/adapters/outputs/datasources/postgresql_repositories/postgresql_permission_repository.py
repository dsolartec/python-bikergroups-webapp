from sqlalchemy.orm import Session

from app.adapters.outputs.datasources.postgresql_entities.permission_entity import PermissionEntity
from app.domain.models.permission_model import PermissionModel
from app.domain.ports.repositories.permission_repository import PermissionRepository


class PostgreSQLPermissionRepository(PermissionRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def save(self, permission: PermissionModel) -> PermissionModel:
        permission_entity = PermissionEntity.from_model(permission)

        self._session.add(permission_entity)
        self._session.commit()
        self._session.refresh(permission_entity)

        return permission_entity.to_model()
