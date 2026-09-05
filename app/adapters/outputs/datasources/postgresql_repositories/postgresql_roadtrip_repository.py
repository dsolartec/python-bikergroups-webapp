from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.adapters.outputs.datasources.postgresql_entities.roadtrip_entity import RoadTripEntity
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.exceptions.not_found_exception import NotFoundException
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.ports.repositories.roadtrip_repository import RoadTripRepository


class PostgreSQLRoadTripRepository(RoadTripRepository):
    _session: Session
        
    def __init__(self, session: Session):
        self._session = session

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(RoadTripEntity)) or 0

    def get_by_id(self, roadtrip_id: str) -> RoadTripModel:
        roadtrip_entity = self._session.scalar(select(RoadTripEntity).where(RoadTripEntity.id == UUID(roadtrip_id)))
        if roadtrip_entity is None:
            raise NotFoundException("Roadtrip not found")

        return roadtrip_entity.to_model()

    def get_many(self, limit: int, offset: int) -> list[RoadTripModel]:
        roadtrips_entities = self._session.scalars(
            select(RoadTripEntity) \
                .limit(limit) \
                    .offset(offset) \
                        .order_by(RoadTripEntity.start_at),
        ).all()

        return [roadtrip_entity.to_model() for roadtrip_entity in roadtrips_entities]

    def save(self, roadtrip: RoadTripModel) -> RoadTripModel:
        roadtrip_entity = RoadTripEntity.from_model(roadtrip)

        self._session.add(roadtrip_entity)
        self._session.commit()
        self._session.refresh(roadtrip_entity)

        return roadtrip_entity.to_model()

    def update(self, roadtrip: RoadTripModel) -> None:
        if roadtrip.id is None:
            raise NotFoundException("Roadtrip not found")

        if roadtrip.updated_by is None:
            raise BadRequestException("Roadtrip update requires an actor")

        roadtrip.updated_at = datetime.now()

        self._session.query(RoadTripEntity) \
            .filter(RoadTripEntity.id == UUID(roadtrip.id)) \
                .update(roadtrip.model_dump(exclude=["id"], exclude_none=True))

        self._session.commit()
