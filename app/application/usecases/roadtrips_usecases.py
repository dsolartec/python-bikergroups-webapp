from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class RoadTripsUseCases:
    @staticmethod
    def create_one(
        cmd: CreateOneRoadTripCommand,
        message_bus: AbstractMessageBus,
        container: AbstractContainer,
    ) -> None:
        with container.unit_of_work() as uow:
            uow.roadtrip_repository.save(RoadTripModel(
                id=None,
                display_name=cmd.display_name,

                start_at=cmd.start_at,
                start_coordinates=cmd.start_coordinates,

                end_coordinates=cmd.end_coordinates,

                # System properties
                created_at=None,
                created_by=cmd.actor_id,

                updated_at=None,
                updated_by=cmd.actor_id,
            ))
