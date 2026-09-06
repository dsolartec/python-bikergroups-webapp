from typing import Iterable

from sqlalchemy import Engine, QueuePool, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.adapters.outputs.datasources.postgresql_entities.permission_entity import PermissionEntity
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_audit_log_repository import PostgreSQLAuditLogRepository
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_roadtrip_repository import PostgreSQLRoadTripRepository
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_permission_repository import PostgreSQLUserPermissionRepository
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository import PostgreSQLUserRepository
from app.domain.enums.permission_enum import PermissionEnum
from app.domain.ports.abstract_unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    _postgresql_engine: Engine
    _postgresql_session: Session

    def __init__(self, postgresql_connection_uri: str):
        self._postgresql_engine = create_engine(
            f"postgresql+psycopg2://{postgresql_connection_uri}",
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            pool_timeout=20,
            poolclass=QueuePool,
        )

        self._postgresql_session = scoped_session(sessionmaker(self._postgresql_engine))

    def __enter__(self):
        self._postgresql_session = self._postgresql_session

        self._audit_log_repository = PostgreSQLAuditLogRepository(self._postgresql_session)
        self._roadtrip_repository = PostgreSQLRoadTripRepository(self._postgresql_session)
        self._user_permission_repository = PostgreSQLUserPermissionRepository(self._postgresql_session)
        self._user_repository = PostgreSQLUserRepository(self._postgresql_session)

        return super().__enter__()

    def generate_initial_data(self) -> None:
        BaseEntity.metadata.create_all(self._postgresql_engine)

        self._postgresql_session.add_all([
            PermissionEntity(name=permission_name.value)
                for permission_name in list(PermissionEnum)
        ])
        self._postgresql_session.commit()

    def rollback(self) -> None:
        self._postgresql_session.rollback()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._postgresql_session.close()
