from typing import Iterable

from sqlalchemy import Engine, QueuePool, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_permission_repository import PostgreSQLPermissionRepository
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_permission_repository import PostgreSQLUserPermissionRepository
from app.adapters.outputs.datasources.postgresql_repositories.postgresql_user_repository import PostgreSQLUserRepository
from app.domain.ports.abstract_unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    _postgresql_engine: Engine
    _postgresql_session: Session

    def __init__(self):
        self._postgresql_engine = create_engine(
            "postgresql+psycopg2://dsolartec@localhost:5432/bikergroups",
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            pool_timeout=20,
            poolclass=QueuePool,
        )

        BaseEntity.metadata.create_all(self._postgresql_engine)

        self._postgresql_session = scoped_session(sessionmaker(self._postgresql_engine))

    def __enter__(self):
        self._postgresql_session = self._postgresql_session

        self._permission_repository = PostgreSQLPermissionRepository(self._postgresql_session)
        self._user_permission_repository = PostgreSQLUserPermissionRepository(self._postgresql_session)
        self._user_repository = PostgreSQLUserRepository(self._postgresql_session)

        return super().__enter__()

    def commit(self) -> None:
        self._postgresql_session.commit()

    def expose_data(self) -> None:
        self._postgresql_session.expunge_all()

    def refresh(self, instance: object, attribute_names: Iterable[str] | None = None) -> None:
        self._postgresql_session.refresh(instance, attribute_names)

    def rollback(self) -> None:
        self._postgresql_session.rollback()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._postgresql_session.close()
