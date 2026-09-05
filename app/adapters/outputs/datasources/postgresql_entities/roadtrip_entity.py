from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.outputs.datasources.postgresql_entities.base_entity import BaseEntity
from app.domain.models.coordinates_model import CoordinatesModel
from app.domain.models.roadtrip_model import RoadTripModel


class RoadTripEntity(BaseEntity):
    __tablename__ = "roadtrips"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    display_name: Mapped[str] = mapped_column(String(120))

    start_at: Mapped[datetime]
    start_coordinates: Mapped[dict[str, float]] = mapped_column(JSON)

    end_coordinates: Mapped[dict[str, float]] = mapped_column(JSON)

    # System columns

    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.current_timestamp,
        server_default=func.current_timestamp(),
    )
    updated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    @staticmethod
    def from_model(roadtrip: RoadTripModel) -> RoadTripEntity:
        args = roadtrip.model_dump(exclude_none=True)
        if roadtrip.id is not None:
            args["id"] = UUID(roadtrip.id)

        if roadtrip.created_by is not None:
            args["created_by"] = UUID(roadtrip.created_by)

        if roadtrip.updated_by is not None:
            args["updated_by"] = UUID(roadtrip.updated_by)

        return RoadTripEntity(**args)

    def to_model(self) -> RoadTripModel:
        return RoadTripModel(
            id=str(self.id),
            display_name=self.display_name,

            start_at=self.start_at,
            start_coordinates=CoordinatesModel.model_validate(self.start_coordinates),

            end_coordinates=CoordinatesModel.model_validate(self.end_coordinates),

            # System columns
            created_at=self.created_at,
            created_by=str(self.created_by),

            updated_at=self.updated_at,
            updated_by=str(self.updated_by),
        )
