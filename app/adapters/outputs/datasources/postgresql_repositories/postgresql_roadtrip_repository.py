from sqlalchemy.orm import Session

from app.adapters.outputs.datasources.postgresql_entities.roadtrip_entity import RoadTripEntity
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.ports.repositories.roadtrip_repository import RoadTripRepository


class PostgreSQLRoadTripRepository(RoadTripRepository):
    _session: Session
        
    def __init__(self, session: Session):
        self._session = session

    def save(self, roadtrip: RoadTripModel) -> RoadTripModel:
        roadtrip_entity = RoadTripEntity.from_model(roadtrip)

        self._session.add(roadtrip_entity)
        self._session.commit()
        self._session.refresh(roadtrip_entity)

        return roadtrip_entity.to_model()
