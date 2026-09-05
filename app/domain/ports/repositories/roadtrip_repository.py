from abc import ABC, abstractmethod

from app.domain.models.roadtrip_model import RoadTripModel


class RoadTripRepository(ABC):
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, roadtrip_id: str) -> RoadTripModel:
        raise NotImplementedError

    @abstractmethod
    def get_many(self, limit: int, offset: int) -> list[RoadTripModel]:
        raise NotImplementedError

    @abstractmethod
    def save(self, roadtrip: RoadTripModel) -> RoadTripModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, roadtrip: RoadTripModel) -> None:
        raise NotImplementedError
