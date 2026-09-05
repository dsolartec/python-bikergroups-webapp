from abc import ABC, abstractmethod

from app.domain.models.roadtrip_model import RoadTripModel


class RoadTripRepository(ABC):
    @abstractmethod
    def save(self, roadtrip: RoadTripModel) -> RoadTripModel:
        raise NotImplementedError
