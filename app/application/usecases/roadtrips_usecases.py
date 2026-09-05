from flask import request

from app.adapters.outputs.libraries.utils import Utils
from app.domain.commands.create_one_roadtrip_command import CreateOneRoadTripCommand
from app.domain.commands.get_all_roadtrips_paginated_command import GetAllRoadtripsPaginatedCommand
from app.domain.commands.update_roadtrip_photo_command import UpdateRoadTripPhotoCommand
from app.domain.enums.audit_log_action_enum import AuditLogActionEnum
from app.domain.exceptions.bad_request_exception import BadRequestException
from app.domain.models.audit_log_model import AuditLogModel
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
            roadtrip = uow.roadtrip_repository.save(RoadTripModel(
                display_name=cmd.display_name,

                start_at=cmd.start_at,
                start_coordinates=cmd.start_coordinates,

                end_coordinates=cmd.end_coordinates,

                # System properties
                created_by=cmd.actor_id,
                updated_by=cmd.actor_id,
            ))

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=cmd.actor_id,
                action=AuditLogActionEnum.ROADTRIP_CREATED,
                metadata=roadtrip.model_dump(exclude=["created_at", "created_by", "updated_at", "updated_by"]),
            ))

            return roadtrip

    @staticmethod
    def get_all_paginated(
            cmd: GetAllRoadtripsPaginatedCommand,
            message_bus: AbstractMessageBus,
            container: AbstractContainer,
    ) -> tuple[list[RoadTripModel], int, int]:
        with container.unit_of_work() as uow:
            total_count = uow.roadtrip_repository.count()

            max_pages = total_count // cmd.limit
            if total_count % cmd.limit != 0:
                max_pages += 1

            if cmd.current_page > max_pages:
                raise BadRequestException("Current page is higher than max pages")

            roadtrips = uow.roadtrip_repository.get_many(
                limit=cmd.limit,
                offset=cmd.current_page * cmd.limit,
            )

            return roadtrips, total_count, max_pages

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

            file.save(f"./app/static/images/roadtrips/{cmd.roadtrip_id}.jpeg")

            roadtrip.updated_by = cmd.actor_id
            uow.roadtrip_repository.update(roadtrip)

            uow.audit_log_repository.save(AuditLogModel(
                actor_id=cmd.actor_id,
                action=AuditLogActionEnum.ROADTRIP_PHOTO_UPDATED,
                metadata={"id": roadtrip.id},
            ))
