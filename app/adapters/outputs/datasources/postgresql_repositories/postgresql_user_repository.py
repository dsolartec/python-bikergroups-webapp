from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.adapters.outputs.datasources.postgresql_entities.user_entity import UserEntity
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.exceptions.username_already_exists_exception import UsernameAlreadyExistsException
from app.domain.models.user_model import UserModel
from app.domain.ports.repositories.user_repository import UserRepository


class PostgreSQLUserRepository(UserRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def get_by_username(self, username: str, with_permissions: bool = False) -> UserModel:
        statement = select(UserEntity).where(UserEntity.username == username)
        if with_permissions:
            statement = statement.options(selectinload(UserEntity.permissions))

        user_entity = self._session.execute(statement).scalar_one_or_none()
        if user_entity is None:
            raise NotFoundException("User not found")

        return user_entity.to_model()

    def save(self, user: UserModel) -> UserModel:
        user_entity = UserEntity.from_model(user)

        self._session.add(user_entity)

        try:
            self._session.commit()
        except IntegrityError as ie:
            if isinstance(ie.orig, UniqueViolation):
                if ie.orig.pgcode == "23505" and ie.orig.diag.constraint_name == "users_username_key":
                    raise UsernameAlreadyExistsException() from ie

            raise

        self._session.refresh(user_entity)

        return user_entity.to_model()
