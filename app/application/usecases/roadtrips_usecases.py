from flask import request

from app.adapters.outputs.libraries.utils import Utils
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.models.roadtrip_model import RoadTripModel
from app.domain.ports.abstract_container import AbstractContainer
from app.domain.ports.abstract_message_bus import AbstractMessageBus


class RoadTripsUseCases:
    @staticmethod
    def create_one(
            cmd: CreateOneRoadTripCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> RoadTripModel:
        with container.unit_of_work() as uow:
            return uow.roadtrip_repository.save(RoadTripModel(
                display_name=cmd.display_name,

                start_at=cmd.start_at,
                start_coordinates=cmd.start_coordinates,

                end_coordinates=cmd.end_coordinates,

                # System properties
                created_by=cmd.actor_id,
                updated_by=cmd.actor_id,
            ))

    @staticmethod
    def update_photo(
            cmd: UpdateRoadTripPhotoCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> None:
        if "file" not in request.files:
            raise BadRequestException("You're not uploading a valid image")

        file = request.files["file"]
        if file.filename == "" or not Utils.is_allowed_image_extension(file.filename):
            raise BadRequestException("You're not uploading a valid image")

        with container.unit_of_work() as uow:
            roadtrip = uow.roadtrip_repository.get_by_id(cmd.roadtrip_id)

            file.save(f"./public/roadtrips/{cmd.roadtrip_id}.jpeg")

            roadtrip.updated_by = cmd.actor_id
            uow.roadtrip_repository.update(roadtrip)
