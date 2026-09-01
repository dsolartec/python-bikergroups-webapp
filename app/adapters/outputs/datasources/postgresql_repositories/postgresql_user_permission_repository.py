from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.outputs.datasources.postgresql_entities.user_permission_entity import UserPermissionEntity
from app.domain.models.user_permission_model import UserPermissionModel
from app.domain.ports.repositories.user_permission_repository import UserPermissionRepository


class PostgreSQLUserPermissionRepository(UserPermissionRepository):
    _session: Session
    
    def __init__(self, session: Session):
        self._session = session

    def get_by_user_id(self, user_id: str) -> list[UserPermissionModel]:
        user_permissions_entities = self._session.execute(
            select(UserPermissionEntity)
                .where(UserPermissionEntity.user_id == user_id),
        ).scalars().all()

        return [entity.to_model() for entity in user_permissions_entities]

    def save(self, user_permission: UserPermissionModel) -> bool:
        user_permission_entity = UserPermissionEntity.from_model(user_permission)

        self._session.add(user_permission_entity)
        self._session.commit()

        return True
